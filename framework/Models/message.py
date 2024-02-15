import datetime
from __init__ import Member, Author, Guild, Channel

class Message:
    def __init__(self, client, **data):
        self.client = client
        self.payload = MessagePayload(self, data)

    async def add_reaction(self, emoji):
        await self.client.put(f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}/@me")

    async def send(self, *args, **kwargs):
        await Message(self.client.message(self.channel_id, *args, **kwargs))

    async def reply(self, *args, **kwargs):
        await Message(self.client.message(self.channel_id, *args, **kwargs, add_data = {"message_reference": {"channel_id": self.channel_id, "guild_id": self.guild_id, "message_id": self.id}}))

    def __getattr__(self, name):
        return getattr(self.payload, name)

class _MessageReference:
    __slots__ = (
        "channel_id",
        "message_id",
        "guild_id"
    )

    def __init__(self, **data):
        self.channel_id = data.get("channel_id")
        self.message_id = data.get("message_id")
        self.guild_id = data.get("guild_id")

class MessagePayload:
    __slots__ = (
        "type", 
        "tts", 
        "timestamp", 
        "_message_reference"
        "_referenced_message", 
        "pinned",
        "nonce", 
        "mentions", 
        "mention_roles", 
        "mention_everyone",
        "member", 
        "id", 
        "flags", 
        "embeds", 
        "_edited_timestamp", 
        "content",
        "components",
        "channel_id", 
        "_author", 
        "attachments", 
        "_guild_id",
        "reactions"
    )
    
    def __init__(self, parent, **data):
        self.parent: Message = parent

        self.type: int = int(data.get("type"))
        self.tts: bool = data.get("tts")
        self.timestamp: datetime.datetime = datetime.datetime.fromisoformat(data.get("timestamp"))
        self._message_reference: dict = data.get("message_reference")
        self._referenced_message: dict = data.get("referenced_message")
        self.pinned: bool = data.get("pinned")
        self.nonce: int = int(data.get("nonce"))
        self.mentions: list = data.get("mentions")
        self.mention_roles: list = data.get("mention_roles")
        self.mention_everyone: bool = data.get("mention_everyone")
        self.member: Member = Member(data.get("member"))
        self.id: int = int(data.get("id"))
        self.flags: int = int(data.get("flags"))
        self.embeds: list = data.get("embeds")
        self._edited_timestamp: str | None = data.get("edited_timestamp")
        self.content: str = data.get("content")
        self.components: list = data.get("components")
        self.channel_id: int = int(data.get("channel_id"))
        self._author = Author(data.get("author"))
        self.attachments: list = data.get("attachments")
        self._guild_id: int = int(data.get("guild_id"))
        self.reactions = []

    @property
    def referenced_message(self) -> Message:
        return Message(self.parent.client, **self._referenced_message)

    @property
    def message_reference(self) -> _MessageReference:
        return _MessageReference(**self._message_reference)

    async def guild(self) -> Guild:
        return Guild(**await self.parent.client.get_guild(self._guild_id))

    async def channel(self) -> Channel:
        return Channel(**await self.parent.client.get_channel(self.channel_id))

    def author(self) -> Author:
        return Author(self._author)

    @property
    def edited_timestamp(self):
        return datetime.datetime.fromisoformat(self._edited_timestamp)

    def _add_reaction(self, reaction):
        self.reactions.append(reaction)

    async def add_reaction(self, emoji):
        self._add_reaction(emoji)
        await self.parent.add_reaction(emoji)