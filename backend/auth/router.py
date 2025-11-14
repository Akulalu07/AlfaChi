from fastapi import APIRouter, Depends, HTTPException, status, Header
from typing import Optional
from auth.models import User
from auth.schemas import (
    UserCreate, UserResponse, UserUpdate, 
)

router = APIRouter(prefix="/auth", tags=["auth"])

async def get_current_user(
    x_telegram_user_id: int = Header(..., alias="X-Telegram-User-Id", description="Telegram User ID")
) -> User:
    user = await User.get_or_none(telegram_id=x_telegram_user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    existing_user = await User.get_or_none(telegram_id=user_data.telegram_id)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this Telegram ID already registered"
        )
    
    user = await User.create(
        telegram_id=user_data.telegram_id,
        name=user_data.name,
        surname=user_data.surname,
        company_name=user_data.company_name
    )
    return UserResponse.model_validate(user)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)

@router.put("/me", response_model=UserResponse)
async def update_me(user_data: UserUpdate, current_user: User = Depends(get_current_user)):
    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    await current_user.save()
    return UserResponse.model_validate(current_user)

