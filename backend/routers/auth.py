from datetime import timezone, timedelta, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import LocalSession
from backend.models import Users

router = APIRouter(prefix='/auth', tags=['auth'])

# encrypt the password
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# From creating the access token
ALGORTHM = "HS256"
SECRET_KEY = "gtwV7kr0PTtv1yY9tchydyym9wmhSD67"


class CreateUserRequest(BaseModel):
    email: str
    username: str
    password: str
    first_name: str
    last_name: str
    is_active: bool = True
    phone_number: str


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


db_dependence = Annotated[Session, Depends(get_db)]


def create_access_token(user: Users, expire_time: timedelta):
    expire = datetime.now(timezone.utc) + expire_time
    encode = {'sub': user.username, 'id': user.id, 'exp': expire}
    return jwt.encode(encode, key=SECRET_KEY, algorithm=ALGORTHM)


def authenticate_user(db, form_data):
    user_model: Users = db.query(Users).filter(
        Users.username == form_data.username).first()
    if not user_model:
        return None
    if bcrypt_context.verify(form_data.password, user_model.hashed_password):
        return user_model
    return None


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependence,
                      create_user_request: CreateUserRequest):
    """
    create new user according tp the user_request and add it to the Users db
    with default id.
    """
    user_model = Users(email=create_user_request.email,
                       username=create_user_request.username,
                       first_name=create_user_request.first_name,
                       last_name=create_user_request.last_name,
                       hashed_password=bcrypt_context.hash(
                           create_user_request.password),
                       is_active=True,
                       phone_number=create_user_request.phone_number
                       )
    db.add(user_model)
    db.commit()


@router.post("/token", status_code=status.HTTP_201_CREATED)
async def login_for_access_token(db: db_dependence, form_data: Annotated[
    OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(db, form_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="username or password is invalid.")
    expire_time = timedelta(seconds=20)
    access_token = create_access_token(user, expire_time)
    return {"access_token": access_token, "token_type": "bearer"}
