from contextlib import asynccontextmanager
from typing import AsyncGenerator

from redis.asyncio import ConnectionPool, Redis

from core.settings import settings


class RedisHelper:
    def __init__(self) -> None:
        self.url = settings.redis.redis_url
        self._pool: ConnectionPool = self._init_pool()


    def _init_pool(self) -> ConnectionPool:
        return ConnectionPool.from_url(
            url=self.url,
            encoding='utf-8',
            decode_responses=True
        )


    @asynccontextmanager
    async def client_getter(self) -> AsyncGenerator:
        redis_client = Redis(connection_pool=self._pool)
        try:
            yield redis_client
        finally:
            await redis_client.aclose()
