import datetime
import os
from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

password_hash = PasswordHash.recommended()
secret = os.getenv("SUPER_SECRET", "dev-secret-change-me-in-production-0123456789")
ALGORITHM = "HS256"
TOKEN_TTL_MINUTES = 30

def create_access_token(user_id: UUID) -> str:
    exp = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=TOKEN_TTL_MINUTES)
    payload = {
        "sub": str(user_id),
        "exp": exp
    }
    return jwt.encode(payload, secret, algorithm=ALGORITHM)

def verify_password(password: str, hash_password: str) -> bool:
    return password_hash.verify(password, hash_password)

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UUID:
    try:
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
        return UUID(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
