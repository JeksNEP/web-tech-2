from sqlalchemy import Table, Column, Integer, String
from databases import metadata
import enum


class UserRole(enum.Enum):
    user = "user"
    admin = "admin"
    approved_user = "approved_user"

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String(100), insex=True),
    Column("email", String(100), unique=True, index=True),
    Column("hashed_password", String),
    Column("link", String(50)),
    Column("role", enum(UserRole), default=UserRole.user.value)
)