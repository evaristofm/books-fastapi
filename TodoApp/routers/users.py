from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException, APIRouter

from auth import get_current_user, bcrypt_context
from database import get_db
from models import User
from schemas import ChangePassWordUser


router = APIRouter(prefix='/users', tags=['users'])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
    user_db = db.query(User).filter(User.id == user.get('id')).first()
    return user_db


@router.put('/', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, change_user_password: ChangePassWordUser):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')

    user_db = db.query(User).filter(User.id == user.get('id')).first()

    if not bcrypt_context.verify(change_user_password.password, user_db.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Error on password change')

    user_db.hashed_password = bcrypt_context.hash(change_user_password.password)
    db.add(user_db)
    db.commit()
