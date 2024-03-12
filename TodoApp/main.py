from fastapi import FastAPI

from .database import engine
from .models import Base
from .routers import auth, todos, admin, users


app = FastAPI()


@app.get("/healthy")
def healthy_check():
    return {'status': 'Healthy'}


app.include_router(todos.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)


Base.metadata.create_all(engine)







