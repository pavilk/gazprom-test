from fastapi import FastAPI, HTTPException, status, Depends
from uuid import uuid4, UUID

from typing import Annotated

from .models import User, UserOut, UserUpdate, UserCreate, Login, Token
from .secure import get_current_user, get_password_hash, verify_password, create_access_token

app = FastAPI()

users: list[User] = []

def check_email_free(email: str, exclude_id: UUID | None = None):
    email = email.lower()
    if any(email == user.email.lower() and user.id != exclude_id for user in users):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь с такой почтой уже существует")

def find(user_id: UUID) -> User:
    for u in users:
        if u.id == user_id:
            return u
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

@app.post("/login", response_model=Token)
def login(
        data: Login
    ):
    email = data.email.lower()
    for user in users:
        if user.email.lower() == email:
            if verify_password(data.password, user.password_hash):
                return Token(access_token=create_access_token(user.id))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неправильный пароль"
            )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Пользователя с такой почтой нет"
    )

@app.get("/users", response_model=list[UserOut])
def list_users():
    return users

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: UUID):
    return find(user_id)

@app.post("/registr", response_model=UserOut, status_code=status.HTTP_201_CREATED)
@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate):
    check_email_free(data.email)
    password_hash = get_password_hash(data.password)
    user = User(id=uuid4(), password_hash=password_hash, **data.model_dump(exclude={"password"}))
    users.append(user)
    return user

@app.put("/users/{user_id}", response_model=UserOut)
def update_user(
        user_id: UUID,
        data: UserUpdate,
        client_id: Annotated[UUID, Depends(get_current_user)]
    ):
    if client_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Чужой юзер"
        )
    user = find(user_id)
    changes = data.model_dump(exclude_none=True)
    if "email" in changes:
        check_email_free(changes["email"], exclude_id=user_id)
    updated = User(**{**user.model_dump(), **changes})
    users[users.index(user)] = updated
    return updated

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
        user_id: UUID,
        client_id: Annotated[UUID, Depends(get_current_user)]
    ):
    if client_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Чужой юзер"
        )
    users.remove(find(user_id))
