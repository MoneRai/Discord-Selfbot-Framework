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
    
    @property
    def author(self) -> Author:
        return self.message.author

    async def reply(self, *args, **kwargs) -> Message:
        return await self.message.reply(*args, **kwargs)

    async def send(self, *args, **kwargs) -> Message:
        return await self.message.send(*args, **kwargs)

    async def send_slash_command(self, name, options):
        command = await self.client.get_slash_command(self.message._guild_id, name)
        return await command.send(self.message._guild_id, self.message._channel_id, options)

    async def type(self):
        await self.message.type()

    async def add_reaction(self, emoji: str):
        await self.message.add_reaction(emoji)