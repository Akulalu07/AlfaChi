from pydantic import BaseModel
from datetime import datetime


class User:

    class Create(BaseModel):
        telegram_id: int
        user_name: str | None = None
        company_name: str | None = None
        company_info: str | None = None

    class Response(BaseModel):
        id: int
        telegram_id: int

        user_name: str | None = None
        company_name: str | None = None
        company_info: str | None = None

        created_at: datetime
        is_admin: bool
        
        class Config:
            from_attributes = True

    class Update(BaseModel):
        user_name: str | None = None
        company_name: str | None = None
        company_info: str | None = None
