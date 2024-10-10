from fastapi import Depends, FastAPI
from databases import Database
import sqlalchemy
from handlers import users_handler
from schemas.user import UserCreate, UserAuthorize
from database import metadata
from utils.token import validate_token_and_role


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

@app.get("/with-credentials")
async def check_credentials(user = Depends(validate_token_and_role(["user","admin","aprooved_user"]))):
    return {"msg": "Welcome allowed user"}

@app.get("/without-credentials")
async def check_credentials():
    return {"msg": "Wlcome all"}