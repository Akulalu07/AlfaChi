from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    telegram_id: int
    name: Optional[str] = None
    surname: Optional[str] = None
    company_name: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    telegram_id: int
    name: Optional[str] = None
    surname: Optional[str] = None
    company_name: Optional[str] = None
    created_at: datetime
    is_admin: bool
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    company_name: Optional[str] = None
