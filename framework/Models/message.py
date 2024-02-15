import datetime
from dataclasses import dataclass
from __init__ import Member, Author, Guild
import discord
discord.Message

class Message:
    def __init__(self, client, data):
        self.client = client
        self.messageEvent = MessagePayload(data)

    async def send(self, *args, **kwargs):
        await self.client.message(self.channel_id, *args, **kwargs)

    async def reply(self, *args, **kwargs):
        await self.client.message(self.channel_id, *args, **kwargs, add_data = {"message_reference": {"channel_id": self.channel_id, "guild_id": self.guild_id, "message_id": self.id}})

    def __getattr__(self, name):
        return getattr(self.messageEvent, name)


@dataclass
class MessagePayload:
    __slots__ = (
        "type", 
        "tts", 
        "timestamp", 
        "referenced_message", 
        "pinned",
        "nonce", 
        "mentions", 
        "mention_roles", 
        "mention_everyone",
        "member", 
        "id", 
        "flags", 
        "embeds", 
        "edited_timestamp", 
        "content",
        "components",
        "channel_id", 
        "author", 
        "attachments", 
        "guild_id"
    )
    
    def __init__(self, **data):
        self.type = int(data.get("type"))
        self.tts = data.get("tts")
        self.timestamp = datetime.datetime.fromisoformat(data.get("timestamp"))
        self.referenced_message = data.get("referenced_message")
        self.pinned = data.get("pinned")
        self.nonce = data.get("nonce")
        self.mentions = data.get("mentions")
        self.mention_roles = data.get("mention_roles")
        self.mention_everyone = data.get("mention_everyone")
        self.member = Member(data.get("member"))
        self.id = int(data.get("id"))
        self.flags = data.get("flags")
        self.embeds = data.get("embeds")
        self.edited_timestamp = data.get("edited_timestamp")
        self.content = data.get("content")
        self.components = data.get("components")
        self.channel_id = int(data.get("channel_id"))
        self.author = Author(data.get("author"))
        self.attachments = data.get("attachments")
        self.guild_id = data.get("guild_id")
        self.guild = Guild(int(data.get("guild_id")))

    @property