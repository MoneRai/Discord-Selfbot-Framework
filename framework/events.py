import datetime
from dataclasses import dataclass

class Message:
    def __init__(self, client, data):
        self.client = client
        self.messageEvent = OnMessageEvent(data)

    async def send(self, *args, **kwargs):
        await self.client.message(self.channel_id, *args, **kwargs)

    async def reply(self, *args, **kwargs):
        await self.client.message(self.channel_id, *args, **kwargs, add_data = {"message_reference": {"channel_id": self.channel_id, "guild_id": self.guild_id, "message_id": self.id}})

    def __getattr__(self, name):
        return getattr(self.messageEvent, name)


@dataclass
class OnMessageEvent:
    data: dict

    type: int
    tts: bool
    timestamp: datetime.datetime
    referenced_message: str
    pinned: bool
    nonce: str
    mentions: list
    mention_roles: list
    mention_everyone: bool
    member: 'Member'
    id: int
    flags: str
    embeds: list
    edited_timestamp: str
    content: str
    components: list
    channel_id: int
    author: 'Author'
    attachments: list
    guild_id: int

    def __post_init__(self):
        self.type = int(self.data.get("type"))
        self.tts = self.data.get("tts")
        self.timestamp = datetime.datetime.fromisoformat(self.data.get("timestamp"))
        self.referenced_message = self.data.get("referenced_message")
        self.pinned = self.data.get("pinned")
        self.nonce = self.data.get("nonce")
        self.mentions = self.data.get("mentions")
        self.mention_roles = self.data.get("mention_roles")
        self.mention_everyone = self.data.get("mention_everyone")
        self.member = Member(self.data.get("member"))
        self.id = int(self.data.get("id"))
        self.flags = self.data.get("flags")
        self.embeds = self.data.get("embeds")
        self.edited_timestamp = self.data.get("edited_timestamp")
        self.content = self.data.get("content")
        self.components = self.data.get("components")
        self.channel_id = int(self.data.get("channel_id"))
        self.author = Author(self.data.get("author"))
        self.attachments = self.data.get("attachments")
        self.guild_id = int(self.data.get("guild_id"))

@dataclass
class Member:
    data: dict

    roles: list
    premium_since: str
    pending: bool
    nick: str
    mute: bool
    joined_at: str
    flags: str
    deaf: bool
    communication_disabled_until: str
    avatar: str

@dataclass
class Author:
    data: dict

    username: str
    public_flags: str
    premium_type: str
    id: int
    global_name: str
    discriminator: str
    avatar: str