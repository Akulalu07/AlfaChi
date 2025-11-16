from pydantic import BaseModel
from datetime import datetime


class Chat:

    class Base(BaseModel):
        type: int  # 0-5

    class Setup(Base):
        pass

    class Response(Base):
        id: int
        user_id: int
        
        class Config:
            from_attributes = True


class Message:

    class Base(BaseModel):
        text: str
        is_user: int  # 0 - модель, 1 - пользователь

    class Response(Base):
        id: int
        chat_id: int
        created_at: datetime
        
        class Config:
            from_attributes = True


class ChatWithMessages(Chat.Response):
    messages: list[Message.Response] = []


class SendMessageRequest(BaseModel):
    text: str
    chat_id: int | None = None
    chat_type: int | None = None
