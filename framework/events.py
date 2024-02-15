from Models import *

class Message:
    def __init__(self, client, data):
        self.client = client
        self.messageEvent = Message(data)

    async def send(self, *args, **kwargs):
        await self.client.message(self.channel_id, *args, **kwargs)

    async def reply(self, *args, **kwargs):
        await self.client.message(self.channel_id, *args, **kwargs, add_data = {"message_reference": {"channel_id": self.channel_id, "guild_id": self.guild_id, "message_id": self.id}})

    def __getattr__(self, name):
        return getattr(self.messageEvent, name)