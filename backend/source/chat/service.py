from openai import AsyncOpenAI
from typing import Self

from config import config
from chat.models import Message


def get_system_prompt_for_chat_type(chat_type: int) -> str:
    chat_prompt: str = config.PROMPTS.get(chat_type, "Ты - помощник для малого бизнеса. Готов помочь с различными вопросами.")
    return f"{config.BASE_PROMPT}\n\n{chat_prompt}"

def get_personalized_prompt(system_prompt: str, context_info: str) -> str:
    return f"{system_prompt}\n\nБизнес пользователя:{context_info}"


class LLMService:
    client: AsyncOpenAI
    model: str

    def __init__(self: Self) -> None:
        self.client = AsyncOpenAI (
            api_key=config.OPEN_ROUTER_API_KEY,
            base_url=config.OPEN_ROUTER_BASE_URL,
            default_headers={
                "HTTP-Referer": "https://github.com/your-repo",  # Optional
                "X-Title": "Goooooooooool",                      # Optional
            }
        )
        self.model = config.OPEN_ROUTER_MODEL
    
    async def generate_response(self: Self, messages: list[dict[str, str]]) -> str:
        try:
            response = await self.client.chat.completions.create (
                model=self.model,
                messages=messages,
                temperature=0.3,
                timeout=60.0
            )
            return response.choices[0].message.content
        
        except Exception as error:
            raise Exception(f"Error calling LLM: {str(error)}")
    
    def format_messages_for_llm(self: Self, messages: list[Message], type: int) -> list[dict[str, str]]:
        formatted: list[dict[str, str]] = []
        first_assistant_message: bool = True
        
        for message in messages:
            role: str = "user"
            content: str = message.text

            if not message.is_user:

                if first_assistant_message:
                    role = "system"
                    first_assistant_message = False

                else:
                    role = "assistant"

            formatted.append ({
                "role": role,
                "content": content
            })

        print(formatted)
        return formatted


llm_service = LLMService()
