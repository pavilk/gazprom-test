from pydantic import BaseModel
from uuid import UUID

class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: UUID

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserOut(BaseModel):
    id: UUID
    name: str
    email: str

class User(UserOut):
    password_hash: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
