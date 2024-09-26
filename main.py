from fastapi import FastAPI
from databases import Database
import sqlalchemy

DATABASE_URL = "postgresql://user:1234@localhost:5423/database"

database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hi hi!"}