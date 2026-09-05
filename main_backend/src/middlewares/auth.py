from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta, timezone
from src.lib.redis_client import is_token_blacklisted

import os

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
security = HTTPBearer() 

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(hours=24)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    
    token = credentials.credentials
    state = await is_token_blacklisted(token)
    
    if state:
        raise HTTPException(status_code=401, detail="Token has been revoked")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("user_id")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")