from fastapi import HTTPException
from sqlalchemy import insert, select
from utils.password import hash_password, verify_password
from models.Users import users
from utils.token import create_access_token


async def create_user(user, db):
    query = select(users).where(users.c.email == user.email)
    existing_user = await db.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = hash_password(user.password)

    role = user.role if hasattr(user, "role") and user.role else UserRole.user.value

    query = insert(users).values(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        role=role
    )

    await db.execute(query)

    return {"name":user.name, "email":user.email}

async def authorize_user(user, db):
    query = select(users).where(users.c.email == user.email)
    existing_user = await db.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=400, detail="User not found")
    
    is_valid_password = verify_password(users.password, existing_user.hashed_password)

    if not is_valid_password:
        raise HTTPException(status_code=400, detail="User not found")
    
    token = create_access_token(
        data={"sub": existing_user["name"], "role": existing_user["role"]}
    ) 
    
    return {"token": token}