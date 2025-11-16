from fastapi import APIRouter, Depends, HTTPException, status

from auth.models import User
from auth.router import get_user

from chat import schemas, models
from chat.service import LLM


router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def setup_chat(data: schemas.Chat.Setup, user: User = Depends(get_user)) -> None:
    if not (0 <= data.type <= 5):
        raise HTTPException (
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Chat type must be in range(0, 6)"
        )
    chat = await models.Chat.create(type=data.type, user=user)

    await models.Message.create (
        chat=chat,
        text=LLM.build_prompt(data.type, user.company_info),
        is_user=0
    )


@router.get("", response_model=list[schemas.Chat.Response])
async def get_chats(user: User = Depends(get_user)):
    chats = await models.Chat.filter(user=user).all()
    return [
        schemas.Chat.Response (
            id = chat.id,
            type = chat.type,
            user_id = user.id
        )
        for chat in chats
    ]


@router.get("/{id}", response_model=schemas.ChatWithMessages)
async def get_chat(id: int, user: User = Depends(get_user)):
    chat = await models.Chat.get_or_none(id=id, user=user)
    if not chat:
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Chat not found"
        )
    
    messages = await models.Message.filter(chat=chat).order_by("created_at")
    chat_data = schemas.Chat.Response(id=chat.id, type=chat.type, user_id=user.id)
    messages_data = [schemas.Message.Response.model_validate(msg) for msg in messages]
    
    return schemas.ChatWithMessages(**chat_data.model_dump(), messages=messages_data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(id: int, user: User = Depends(get_user)):
    chat = await models.Chat.get_or_none(id=id, user=user)
    if not chat:
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Chat not found"
        )
    await chat.delete()


@router.post("/messages", response_model=schemas.Message.Response)
async def send_message (
    message_data: schemas.SendMessageRequest,
    user: User = Depends(get_user)
):
    if message_data.chat_id:
        chat = await models.Chat.get_or_none(id=message_data.chat_id, user=user)
        if not chat:
            raise HTTPException (
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found"
            )
    else:

        if message_data.chat_type is None:
            raise HTTPException (
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chat type required for setup"
            )
        
        if message_data.chat_type < 0 or message_data.chat_type > 5:
            raise HTTPException (
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chat type must be in range(0, 6)"
            )
        
        chat = await models.Chat.create(type=message_data.chat_type, user=user)
        await models.Message.create (
            chat=chat,
            text=LLM.build_prompt(message_data.chat_type, user.company_info),
            is_user=0
        )
    
    type = message_data.chat_type
    await models.Message.create (
        chat=chat,
        text=message_data.text,
        is_user=1
    )
    
    messages = await models.Message.filter(chat=chat).order_by("created_at")
    llm_messages = LLM.format_messages_for_llm(messages, type)
    
    try:
        llm_response_text = await LLM.generate_response(llm_messages)
    except Exception as error:
        print(error)
        raise HTTPException (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting LLM response: {str(error)}"
        )
    
    llm_message = await models.Message.create (
        chat=chat,
        text=llm_response_text,
        is_user=0
    )
    
    return schemas.Message.Response.model_validate(llm_message)


@router.get("/{id}/messages", response_model=list[schemas.Message.Response])
async def get_chat_messages(id: int, user: User = Depends(get_user)):
    chat = await models.Chat.get_or_none(id=id, user=user)
    if not chat:
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Chat not found"
        )
    
    messages = await models.Message.filter(chat=chat).order_by("created_at")
    return [schemas.Message.Response.model_validate(msg) for msg in messages]
