class Context:
    __slots__ = (
        "message",
        "client"
    )

    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def guild(self):
        return await self.message.guild()
    
    async def channel(self):
        return await self.message.channel()
    
    async def author(self):
        return await self.message.author()

    async def reply(self, *args, **kwargs):
        await self.message.reply(*args, **kwargs)

    async def send(self, *args, **kwargs):
        await self.message.send(*args, **kwargs)

    async def type(self):
        return await self.message.type()