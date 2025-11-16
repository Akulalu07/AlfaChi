from fastapi import (
    APIRouter, Depends,
    HTTPException, status, Header
)

from auth import schemas, models
from chat.models import Chat, Message


router = APIRouter(prefix="/auth", tags=["auth"])


async def get_user (
    x_telegram_user_id: int = Header(..., alias="X-Telegram-User-Id", description="Telegram User ID")
) -> models.User:
    user = await models.User.get_or_none(telegram_id=x_telegram_user_id)
    if user is None:
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found"
        )
    return user


@router.post("/register", response_model=schemas.User.Response, status_code=status.HTTP_201_CREATED)
async def register(data: schemas.User.Create):
    existing_user = await models.User.get_or_none(telegram_id=data.telegram_id)
    
    if existing_user:
        raise HTTPException (
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "User with this Telegram ID already registered"
        )
    
    user = await models.User.create (
        telegram_id=data.telegram_id,
        user_name=data.user_name,
        company_name=data.company_name,
        company_info=data.company_info,
    )
    
    return schemas.User.Response.model_validate(user)


@router.get("/me", response_model=schemas.User.Response)
async def get_me(user: models.User = Depends(get_user)):
    return schemas.User.Response.model_validate(user)


@router.put("/me", response_model=schemas.User.Response)
async def update_me(user_data: schemas.User.Update, user: models.User = Depends(get_user)):
    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    await user.save()
    return schemas.User.Response.model_validate(user)


# УБРАТЬ НА ПРОДАКШЕНЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕ
# Каскадное удаление пользователя, чата и сообщений
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT) 
async def delete_me(user: models.User = Depends(get_user)):
    chats = await Chat.filter(user=user)
    for chat in chats:
        await Message.filter(chat=chat).delete()
        await chat.delete()
    await user.delete()
    return None
