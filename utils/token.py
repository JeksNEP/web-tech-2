from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

SECRET_KEY = "web-tech-2"
ALGORITHM = "HS246"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else TimeoutError
    if expires_delta:
        expire = datetime.utcnow() + 
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt