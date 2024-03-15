from fastapi import status

from .utils import *
from ..routers.users import get_current_user, get_db


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'evaristofm'
    assert response.json()['email'] == 'evatest@gmail.com'
    assert response.json()['first_name'] == 'Evaristo'
    assert response.json()['last_name'] == 'Neto'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '(111)-111-111'


def test_change_password_success(test_user):
    response = client.put("/users/",
                          json={"password": "password", "change_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put("/users/",
                          json={"password": "wrong_password", "change_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change'}

