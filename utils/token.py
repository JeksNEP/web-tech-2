from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from fastapi.security import HTTPBearer

SECRET_KEY = "web-tech-2"
ALGORITHM = "HS246"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else TimeoutError
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = HTTPBearer()
def validate_token_and_role(required_roles: List[str]):
    def token_validator(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            name = payload.get("sub")
            id = payload.get("id")
            role = payload.get("role")
            if name is None or role in None:
                raise HTTPException(
                    status_code="401",
                    detail="User or userRole in not identified"
                )
            if role not in required_roles:
                raise HTTPException(
                    status_code="403",
                    detail="Your role is not valid for this request"
                )
            return {"name": name,"role": role, "id": id}
        except JWTError:
            raise HTTPException(
            status_code=401,
            detail="Token is not valid"
        )