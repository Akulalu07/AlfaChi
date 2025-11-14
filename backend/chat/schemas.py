from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ChatBase(BaseModel):
    type: int  # 0-5

class ChatCreate(ChatBase):
    pass

class ChatResponse(ChatBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    text: str
    is_user: int  # 0 - модель, 1 - пользователь

class MessageCreate(MessageBase):
    chat_id: int

class MessageResponse(MessageBase):
    id: int
    chat_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatWithMessages(ChatResponse):
    messages: List[MessageResponse] = []

class SendMessageRequest(BaseModel):
    text: str
    chat_id: Optional[int] = None
    chat_type: Optional[int] = None  # Если создается новый чат

