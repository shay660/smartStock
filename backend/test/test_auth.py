import sys
import os

# sys.path.append(os.path.dirname(__file__))
# print(sys.path)

from .utils import *
from fastapi import status

from ..routers.auth import get_db

app.dependency_overrides[get_db] = override_get_db


def test_create_user(test_user):
    request = {"email": "testUser1", "username": "testUser",
               "password": "test123",
               "first_name": "Test1", "last_name": "User1",
               "phone_number": "000-000-0000"}
    response = client.post("/auth", json=request)
    assert response.status_code == status.HTTP_201_CREATED
    db = TestSession()
    new_user = db.query(Users).filter(Users.id == 2).first()
    assert new_user is not None
    assert new_user.email == request.get("email")
    assert new_user.username == request.get("username")
    assert new_user.first_name == request.get("first_name")
    assert new_user.last_name == request.get("last_name")
    assert new_user.phone_number == request.get("phone_number")

