from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
import sqlalchemy
from database import metadata, engine, database
from handlers import books_handler, users_handler
from schemas.user import UserCreate, UserAuthorize
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
    return {"msg": "Welcome all"}

@app.post("/create-book")
async def create_book(title = Form(...), author = Form(...), description = Form(...), file: UploadFile = File(...), user = Depends(validate_token_and_role(["admin"]))):
    return await books_handler.upload_book(database, title, author, description, file,)

@app.get("/books/get-book/{book_id}")
async def download_book(book_id, user = Depends(validate_token_and_role(["user","admin","aprooved_user"]))):
    return await books_handler.download_book(database, book_id)

@app.get("/books/download/{book_id}")
async def download_book(book_id: int, user = Depends(validate_token_and_role(["user", "approved_user","admin"]))):
    return await books_handler.download_book(database, book_id)