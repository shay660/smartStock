from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import LocalSession
from ..models import Users

router = APIRouter(prefix='/auth', tags=['auth'])


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
                       hashed_password=create_user_request.password,
                       is_active=True,
                       phone_number=create_user_request.phone_number
                       )
    db.add(user_model)
    db.commit()


