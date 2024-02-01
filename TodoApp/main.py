from fastapi import FastAPI

from database import engine
from models import Base
from routers import auth, todos


app = FastAPI()

app.include_router(todos.router)
app.include_router(auth.router)

Base.metadata.create_all(engine)







