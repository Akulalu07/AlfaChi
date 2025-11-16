import os
from aiohttp import (
    ClientTimeout, TCPConnector,
    ClientSession
)
from typing import Self, Any


class BackendService:
    session: ClientSession | None
    url: str

    def __init__(self: Self, *, url: str) -> None:
        self.url = url
        self.session = None

    async def get_session(self: Self) -> ClientSession:
        if self.session is None or self.session.closed:
            timeout = ClientTimeout(total=30)
            connector = TCPConnector(limit=100, limit_per_host=30)
            self.session = ClientSession(
                timeout=timeout,
                connector=connector,
                headers={"Content-Type": "application/json"}
            )
        return self.session

    async def close_session(self: Self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()

    async def get(self: Self, url: str, *args, **kw) -> Any:
        session = await self.get_session()
        return await session.get(f"{self.url}{url}", *args, **kw)
    
    async def post(self: Self, url: str, *args, **kw) -> Any:
        session = await self.get_session()
        return await session.post(f"{self.url}{url}", *args, **kw)


url: str = os.getenv("BACKEND_URL", "http://backend:8080")
backend = BackendService(url=url)
