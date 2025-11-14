import aiohttp
from aiogram import Bot, Dispatcher

class HTTPService:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = None

    async def get_session(self):
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
            self.session = aiohttp.ClientSession(
                timeout=timeout, 
                connector=connector,
                headers={"Content-Type": "application/json"}
            )
        return self.session

    async def close_session(self):
        if self.session and not self.session.closed:
            await self.session.close()

http_service = HTTPService(base_url="http://backend:8080")
