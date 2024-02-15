class Context:
    __slots__ = (
        "author",
        "message",
        "client",
        "guild",
        "channel"
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