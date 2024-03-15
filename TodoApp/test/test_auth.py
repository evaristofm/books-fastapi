from .utils import *

from ..routers.auth import authenticate_user
from ..auth import get_db


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

