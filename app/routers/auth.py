from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.token import Token
from app.models.user import UserCreate, UserInDB
from app.services.log_service import log_activity

router = APIRouter()

# In-memory user database
fake_users_db = {}


@router.post("/register", response_model=UserInDB)
def register(user: UserCreate):
    if user.email in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(**user.dict(), hashed_password=hashed_password)
    fake_users_db[user.email] = user_in_db
    log_activity(f"User registered: {user.email}")
    return user_in_db


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    log_activity(f"User logged in: {user.email}")
    return {"access_token": access_token, "token_type": "bearer"}
