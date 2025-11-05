from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.usermodel import User
from app.db import get_db
import uuid
import os
from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))

oaut2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token", scheme_name="JWT")


def create_access_token(data: dict, expire_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expire_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except JWTError as e:
        print(f"Failed to decode token: {e}")
        return None


async def get_current_user(
    token: Annotated[str, Depends(oaut2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
):

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    print("Validating token...")

    payload = decode_access_token(token)
    if payload is None or "sub" not in payload:
        print("Failed to decode token")
        raise credential_exception

    user_id = payload["sub"]  # UUID string
    user = await db.get(User, uuid.UUID(user_id))
    if user is None:
        raise credential_exception

    return user
