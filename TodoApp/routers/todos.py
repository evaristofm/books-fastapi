from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends, Path


from models import Todos
from auth import get_current_user
from database import get_db
from schemas import TodoRequest


router = APIRouter(prefix='/todo', tags=['todo'])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/')
async def read_all_todos(db: db_dependency):
    return db.query(Todos).all()


@router.get('/{todo_id}', status_code=status.HTTP_200_OK)
async def read_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_db = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_db:
        return todo_db
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found!')


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Authentication failed.')

    todo_model = Todos(**todo_request.model_dump(), user_id=user.get('id'))

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)


@router.put('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo_db = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')

    todo_db = Todos(**todo_request.model_dump())
    db.add(todo_db)
    db.commit()
    db.refresh(todo_db)

    return todo_db


@router.delete('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_db = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
    db.delete(todo_db)
    db.commit()
