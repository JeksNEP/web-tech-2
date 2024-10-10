from sqlalchemy import create_engine, MetaData
from database import Database


DATABASE_URL = "postgresql://user:1234@localhost:5423/library"

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)