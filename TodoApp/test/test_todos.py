from fastapi import status

from .utils import *
from ..main import app
from ..models import Todos
from ..routers.todos import get_db, get_current_user


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get("/todo/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'id': 1, 'complete': False, 'title': 'Learn to code',
                                'description': 'Lorem', 'priority': 5, 'user_id': 1}]


def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'id': 1, 'complete': False, 'title': 'Learn to code',
                                'description': 'Lorem', 'priority': 5, 'user_id': 1}


def test_read_one_authenticated_not_found():
    response = client.get("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found!'}


def test_create_todo(test_todo):
    request_data = {
        'title': 'Learn to code',
        'description': 'Lorem',
        'priority': 5,
        'complete': False
    }
    response = client.post("/todo/", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    todo_model = db.query(Todos).filter(Todos.id == 2).first()

    assert todo_model.title == request_data.get('title')
    assert todo_model.description == request_data.get('description')
    assert todo_model.priority == request_data.get('priority')
    assert todo_model.complete == request_data.get('complete')


def test_update_todo(test_todo):
    request_data = {
        'title': 'Change the title of the todo',
        'description': 'Lorem',
        'priority': 5,
        'complete': False
    }

    response = client.put("/todo/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    todo_model = db.query(Todos).filter(Todos.id == 1).first()

    assert todo_model.title == 'Change the title of the todo'


def test_update_todo_not_found(test_todo):
    request_data = {
        'title': 'Change the title of the todo',
        'description': 'Lorem',
        'priority': 5,
        'complete': False
    }

    response = client.put("/todo/999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}


def test_delete_todo(test_todo):
    response = client.delete("/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    todo_model = db.query(Todos).filter(Todos.id == 1).first()
    assert todo_model is None


def test_delete_todo_not_found(test_todo):
    response = client.delete("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}
