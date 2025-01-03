from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
import sqlalchemy
from database import metadata, engine, database
from handlers import books_handler, users_handler, reviews_handler
from models import Users
from schemas.user import UserCreate, UserAuthorize
from schemas.review import ReviewCreate, ReviewUpdate
from utils.token import validate_token_and_role


metadata.create_all(bind=sqlalchemy.Engine)

app = FastAPI()

async def shutdown():
    await database.disconnect()

@app.get("/users/", tags=["Users"])
async def read_users():
   query = Users.select()
   return await database.fetch_all(query)

@app.post("/users/", tags=["Users"])
async def create_user(user:UserCreate):
    return await users_handler.create_user(user, database)

@app.post("/users/authorize", tags=["Users"])   
async def create_user(user):
    return await users_handler.authorize_user(user.database)

@app.get("/with-credentials")
async def check_credentials(user = Depends(validate_token_and_role(["user","admin","aprooved_user"]))):
    return {"msg": "Welcome allowed user"}

@app.get("/without-credentials")
async def check_credentials():
    return {"msg": "Welcome all"}

@app.post("/create-book", tags=["Books Managment"])
async def create_book(title = Form(...), author = Form(...), description = Form(...), file: UploadFile = File(...), user = Depends(validate_token_and_role(["admin"]))):
    return await books_handler.upload_book(database, title, author, description, file,)

@app.get("/books/get-book/{book_id}", tags=["Books Managment"])
async def download_book(book_id, user = Depends(validate_token_and_role(["user","admin","aprooved_user"]))):
    return await books_handler.download_book(database, book_id)

@app.get("/books/download/{book_id}", tags=["Books Managment"])
async def download_book(book_id: int, user = Depends(validate_token_and_role(["user", "approved_user","admin"]))):
    return await books_handler.download_book(database, book_id)

@app.post("/reviews/", tags=["Reviews Managment"], summary="Endpoint for review creation")
async def create_review(review: ReviewCreate, user = Depends(validate_token_and_role(["user", "approved_user","admin"]))):
    return await reviews_handler.create_review(review, user, database)

@app.get("/reviews/{book_id}", tags=["Reviews Managment"], description="Description")
async def get_reviews_for_book(book_id: int, user = Depends(validate_token_and_role(["user", "approved_user","admin"]))):
    return await reviews_handler.get_reviews_for_book(book_id, database)

@app.put("/reviews/{review_id}", tags=["Reviews Managment"], response_description="Response contains message about results")
async def update_review(review_id: int, updated_review: ReviewUpdate, user = Depends(validate_token_and_role(["user", "approved_user","admin"]))):
    return await reviews_handler.update_review(review_id, updated_review, user, database)

@app.delete("/reviews/{review_id}", tags=["Reviews Managment"])
async def delete_review(review_id: int, user = Depends(validate_token_and_role(["admin"]))):
    return await reviews_handler.delete_review(review_id, user, database)