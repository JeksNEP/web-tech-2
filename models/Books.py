from sqlalchemy import Table, Column, Integer, String
from databases import metadata


books = Table(
    "Books",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("title", String(200)),
    Column("author", String(100)),
    Column("Description", String),
    Column("link", String(50))
)