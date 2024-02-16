from .message import Message
from .guild import Guild
from .channel import Channel
from .author import Author

class Context:
    __slots__ = (
        "message",
        "client"
    )

    def __init__(self, client, message: Message):
        self.client = client
        self.message = message

    async def guild(self) -> Guild:
        return await self.message.guild()
    
    async def channel(self) -> Channel:
        return await self.message.channel()
    
    async def author(self) -> Author:
        return await self.message.author()

    async def reply(self, *args, **kwargs) -> Message:
        return await self.message.reply(*args, **kwargs)

    async def send(self, *args, **kwargs) -> Message:
        return await self.message.send(*args, **kwargs)

    async def type(self):
        await self.message.type()

    async def add_reaction(self, emoji: str):
        await self.message.add_reaction(emoji)