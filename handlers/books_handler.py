from fastapi import Form, File, UploadFile, Depends, HTTPException
import os
from databases import Database
from models import Books
from sqlalchemy import select, insert
from starlette.responses import FileResponse
from utils.token import validate_token_and_role

UPLOAD_FOLDER = "uploaded_books"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

async def upload_book(
        db,
        title = Form(...),
        author = Form(...),
        description = Form(...),
        file = File(...),
):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    query = insert(Books).values(
        title=title,
        author=author,
        description=description,
        link=file_path
    )

    await db.execute(query)

    return {"title": title, "message": "Book created"}

async def get_book(db, book_id):
    query = select(Books).where(Books.c.id == book_id)
    book = await Database.fetch_one(query)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    downloar_url = f"/download/{book_id}"

    return {
        "title": book.title,
        "author": book.author,
        "description": book.description,
        "download_url": downloar_url
    }

async def download_book(db ,book_id):
    query = select(Books).where(Books.c.id == book_id)
    book = await db.fetch_one(query)

    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    
    file_path = book.link

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="file not found")
    
    return FileResponse(path=file_path, filename=os.path.basename(file_path))