import pytest
from jose import jwt
from datetime import timedelta
from fastapi import HTTPException, status

from .utils import *

from ..routers.auth import authenticate_user
from ..auth import get_db, create_acess_token, SECRET_KEY, ALGORITHM, get_current_user


app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, 'password', db)

    assert authenticated_user is not False
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user("WrongUserName", 'testpassword', db)
    assert non_existent_user is False

    wrong_password = authenticate_user(test_user.username, "Wrongpassword", db)
    assert non_existent_user is False


def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)

    token = create_acess_token(username, user_id, role, expires_delta)
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],
                               options={'verify_signature': False})

    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'sub': 'testuser', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {'username': 'testuser', 'id': 1, 'user_role': 'admin'}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role': 'user'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == status.HTTP_404_NOT_FOUND
    assert excinfo.value.detail == 'Could not validate user.'
