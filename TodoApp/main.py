from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import FastAPI, Depends, status, Path, HTTPException
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal
from models import Todos


app = FastAPI()

models.Base.metadata.create_all(engine)


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get('/')
async def read_all_todos(db: db_dependency):
    return db.query(Todos).all()


@app.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def read_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_db = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_db:
        return todo_db
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found!')


@app.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump())

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)


@app.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo_db = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')

    todo_db = Todos(**todo_request.model_dump())
    db.add(todo_db)
    db.commit()
    db.refresh(todo_db)

    return todo_db


@app.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_db = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
    db.delete(todo_db)
    db.commit()
