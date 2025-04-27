import pytest

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from ..main import app
from ..database import Base
from ..models import Users
from ..routers.auth import bcrypt_context

SQLALCHEMY_TEST_DB_URL = "sqlite:///./testdb.db"

engine = create_engine(SQLALCHEMY_TEST_DB_URL, connect_args={
    "check_same_thread": False})

TestSession = sessionmaker(engine, autoflush=False, autocommit=False)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)


@pytest.fixture
def test_user():
    try:
        user = Users(id=1, username="Shay660test",
                     email="shay660test@gmail.com",
                     first_name="Shay", last_name="Itzhaki",
                     hashed_password=bcrypt_context.hash("test123"),
                     phone_number="054-5841875")
        db = TestSession()
        db.add(user)
        db.commit()
    finally:
        yield
        with engine.connect() as connection:
            connection.execute(text("DELETE FROM users;"))
            connection.commit()
