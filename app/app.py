from fastapi import FastAPI
from . import models
from .routes.v1.users import user
from .routes.v1.auth import auth
from .database.database import engine

app = FastAPI()

models.models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)


@app.get("/", tags=["Home"])
async def index():
    return {
        "message": "Welcome to simpl money!"
    }
