from client import Client
import asyncio
from Models import *
from typing import List

class Bot(Client):
    def __init__(self, token: str, *args, **kwargs):
        super().__init__(token, *args, **kwargs)

    def run(self):
        asyncio.new_event_loop().run_until_complete(super().run())

    async def fetch_guild(self, id: int) -> Guild:
        return Guild(await super().get_guild(id))

    async def fetch_channel(self, id: int) -> Channel:
        return Channel(await super().get_channel(id))

    async def fetch_user(self, id: int) -> User:
        return User(await super().get_user(id))

    async def get_messages(self, channel, *, limit = 50, before: int = None) -> List[Message]:
        return [Message(**data) for data in await super().get_messages(channel, limit = limit, before = before)]