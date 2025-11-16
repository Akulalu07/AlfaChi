from fastapi import APIRouter, Depends, HTTPException, status, Header

from auth.models import User
from chat.models import Chat, Message
from auth.schemas import (
    UserCreate, UserResponse, UserUpdate, 
)


router = APIRouter(prefix="/auth", tags=["auth"])


async def get_current_user (
    x_telegram_user_id: int = Header(..., alias="X-Telegram-User-Id", description="Telegram User ID")
) -> User:
    user = await User.get_or_none(telegram_id=x_telegram_user_id)
    if user is None:
        raise HTTPException (
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
    
    user = await User.create (
        telegram_id=user_data.telegram_id,
        user_name=user_data.user_name,
        company_name=user_data.company_name,
        company_info=user_data.company_info,
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


# УБРАТЬ НА ПРОДАКШЕНЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕ
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT) # Каскадное удаление пользователя, чата и сообщений
async def delete_me(current_user: User = Depends(get_current_user)):
    chats = await Chat.filter(user=current_user)
    for chat in chats:
        await Message.filter(chat=chat).delete()
        await chat.delete()
    await current_user.delete()
    return None
