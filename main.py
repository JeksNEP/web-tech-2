from fastapi import FastAPI
from databases import Database
import sqlalchemy
from handlers import users_handler
from schemas.user import UserCreate, UserAuthorize
from database import metadata


metadata.create_all(bind=sqlalchemy.Engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hi hi!"}

@app.post("/users/")
async def create_user(user):
    return await users_handler.create_user(user.database)

@app.post("/users/authorize")
async def create_user(user):
    return await users_handler.authorize_user(user.database)