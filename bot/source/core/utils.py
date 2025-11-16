from aiogram.types import Message

import re
import asyncio

from stuff import *


async def is_registered(telegram_id: int) -> bool:
    try:
        async with (await backend.get(f"/auth/me", headers={"X-Telegram-User-Id": str(telegram_id)})) as response:
            return response.status == 200
    except Exception as error:
        logger.error(f"Error checking registration: {str(error)}")
        return False


async def create_chats(telegram_id: int) -> bool:
    for type in range(6):
        try:
            async with await backend.post(f"/chats", json={"type": type}, headers={"X-Telegram-User-Id": str(telegram_id)}) as response:
                if response.status != 201:
                    return False
        except Exception as e:
            logger.error(f"Error creating chats: {str(e)}")
            return False
    return True


async def get_chat_id(telegram_id: int, type: int) -> int | None:
    try:
        async with (await backend.get("/chats", headers={"X-Telegram-User-Id": str(telegram_id)})) as response:
            if response.status == 200:
                chats = await response.json()
                for chat in chats:
                    if chat["type"] == type:
                        return chat["id"]
            else:
                logger.error(f"Error getting chat id: {response.status}")
                return None
            return None
        
    except Exception as error:
        logger.error(f"Error getting chat id: {str(error)}")
        return None


async def send_long_message(message: Message, text: str, reply_markup=None, delay: float = 0.3):
    parts = await split_long_message(text)
    
    for i, part in enumerate(parts):
        markup = reply_markup if i == 0 else None
        await message.answer(part, reply_markup=markup)
        
        if i < len(parts) - 1:
            await asyncio.sleep(delay)


def clean_markdown(text: str) -> str:
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    text = re.sub(r'(?<!_)_([^_]+)_(?!_)', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'[*_`#]', '', text)
    return text.strip()


async def split_long_message(text: str, max_length: int = 4000) -> list[str]:
    if len(text) <= max_length:
        return [text]
    
    parts = []
    paragraphs = text.split('\n\n')
    current_part = ""
    
    for paragraph in paragraphs:
        if len(paragraph) > max_length:
            if current_part:
                parts.append(current_part.strip())
                current_part = ""
            lines = paragraph.split('\n')
            for line in lines:
                if len(current_part) + len(line) + 1 <= max_length:
                    if current_part:
                        current_part += "\n" + line
                    else:
                        current_part = line
                else:
                    if current_part:
                        parts.append(current_part.strip())
                    current_part = line
        else:
            separator = "\n\n" if current_part else ""
            if len(current_part) + len(paragraph) + len(separator) <= max_length:
                current_part += separator + paragraph
            else:
                if current_part:
                    parts.append(current_part.strip())
                current_part = paragraph
    
    if current_part:
        parts.append(current_part.strip())
    
    return parts
