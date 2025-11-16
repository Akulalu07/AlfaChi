from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    telegram_id: int
    user_name: str | None = None
    company_name: str | None = None
    company_info: str | None = None


class UserResponse(BaseModel):
    id: int
    telegram_id: int

    user_name: str | None = None
    company_name: str | None = None
    company_info: str | None = None

    created_at: datetime
    is_admin: bool
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    user_name: str | None = None
    company_name: str | None = None
    company_info: str | None = None
