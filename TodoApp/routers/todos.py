from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends, Path


from models import Todos
from database import get_db
from schemas import TodoRequest


router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/')
async def read_all_todos(db: db_dependency):
    return db.query(Todos).all()


@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def read_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_db = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_db:
        return todo_db
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found!')


@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump())

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)


@router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo_db = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')

    todo_db = Todos(**todo_request.model_dump())
    db.add(todo_db)
    db.commit()
    db.refresh(todo_db)

    return todo_db


@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_db = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
    db.delete(todo_db)
    db.commit()
