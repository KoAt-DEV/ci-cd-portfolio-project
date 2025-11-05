from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.services.auth import create_access_token, get_current_user
from app.crud.usercrud import authenticate_user, get_user_by_email, create_user
from app.schemas.userschema import UserResponse, MeResponse, UserCreate
from app.db import get_db


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register(new_user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    existing_user = await get_user_by_email(db, new_user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(db, new_user.email, new_user.name, new_user.password)
    return user


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=UserResponse)
async def login(
    email: str, password: str, db: Annotated[AsyncSession, Depends(get_db)]
):
    user = await authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    return user


@router.get("/me", response_model=MeResponse)
async def read_users_me(user=Depends(get_current_user)):

    return MeResponse(
        user_name=user.name, user_email=user.email, user_created_at=user.created_at
    )
