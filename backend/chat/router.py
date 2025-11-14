from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from auth.models import User
from auth.router import get_current_user
from chat.models import Chat, Message
from chat.schemas import (
    ChatCreate, ChatResponse, MessageResponse, 
    ChatWithMessages, SendMessageRequest
)
from chat.service import llm_service, get_system_prompt_for_chat_type

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat_data: ChatCreate,
    current_user: User = Depends(get_current_user)
):
    if chat_data.type < 0 or chat_data.type > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chat type должен быть между 0 и 5"
        )
    chat = await Chat.create(type=chat_data.type, user=current_user)
    
    # системный промпт как первое сообщение
    system_prompt = get_system_prompt_for_chat_type(chat_data.type)
    await Message.create(
        chat=chat,
        text=system_prompt,
        is_user=0
    )
    
    return ChatResponse(id=chat.id, type=chat.type, user_id=current_user.id)

@router.get("/", response_model=List[ChatResponse])
async def get_user_chats(current_user: User = Depends(get_current_user)):
    chats = await Chat.filter(user=current_user).all()
    return [ChatResponse(id=chat.id, type=chat.type, user_id=current_user.id) for chat in chats]

@router.get("/{chat_id}", response_model=ChatWithMessages)
async def get_chat(
    chat_id: int,
    current_user: User = Depends(get_current_user)
):
    chat = await Chat.get_or_none(id=chat_id, user=current_user)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Чат не найден"
        )
    
    messages = await Message.filter(chat=chat).order_by("created_at")
    chat_data = ChatResponse(id=chat.id, type=chat.type, user_id=current_user.id)
    messages_data = [MessageResponse.model_validate(msg) for msg in messages]
    
    return ChatWithMessages(**chat_data.model_dump(), messages=messages_data)

@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
    chat_id: int,
    current_user: User = Depends(get_current_user)
):
    chat = await Chat.get_or_none(id=chat_id, user=current_user)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Чат не найден"
        )
    await chat.delete()

@router.post("/message", response_model=MessageResponse)
async def send_message(
    message_data: SendMessageRequest,
    current_user: User = Depends(get_current_user)
):
    if message_data.chat_id:
        chat = await Chat.get_or_none(id=message_data.chat_id, user=current_user)
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Чат не найден"
            )
    else:
        if message_data.chat_type is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="chat_type необходимо при создании нового чата"
            )
        if message_data.chat_type < 0 or message_data.chat_type > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chat type должен быть между 0 и 5"
            )
        chat = await Chat.create(type=message_data.chat_type, user=current_user)
        
        # опять системный промпт первое сообщ
        system_prompt = get_system_prompt_for_chat_type(message_data.chat_type)
        await Message.create(
            chat=chat,
            text=system_prompt,
            is_user=0
        )
    
    user_message = await Message.create(
        chat=chat,
        text=message_data.text,
        is_user=1
    )
    
    messages = await Message.filter(chat=chat).order_by("created_at")
    
    llm_messages = llm_service.format_messages_for_llm(messages)
    
    try:
        llm_response_text = await llm_service.generate_response(llm_messages)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting LLM response: {str(e)}"
        )
    
    llm_message = await Message.create(
        chat=chat,
        text=llm_response_text,
        is_user=0
    )
    
    return MessageResponse.model_validate(llm_message)

@router.get("/{chat_id}/messages", response_model=List[MessageResponse])
async def get_chat_messages(
    chat_id: int,
    current_user: User = Depends(get_current_user)
):
    chat = await Chat.get_or_none(id=chat_id, user=current_user)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Чат не найден"
        )
    
    messages = await Message.filter(chat=chat).order_by("created_at")
    return [MessageResponse.model_validate(msg) for msg in messages]

