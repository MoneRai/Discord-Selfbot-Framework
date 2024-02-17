import datetime
from .member import Member
from .author import Author
from .guild import Guild
from .channel import Channel
from .emoji import Emoji
from .reaction import Reaction
from .embed import Embed
from .components import MessageComponent
from urllib.parse import quote_plus

class Message:
    def __init__(self, client, **data):
        self.client = client
        self.payload = MessagePayload(self, **data)

    async def add_reaction(self, emoji: Emoji | str):
        return await self.client.put(f"/channels/{self._channel_id}/messages/{self.id}/reactions/{quote_plus(str(emoji))}/@me", {})

    async def send(self, *args, **kwargs):
        return Message(self.client, **await self.client.message(self._channel_id, *args, **kwargs))

    async def reply(self, *args, **kwargs):
        return Message(self.client, **await self.client.message(self._channel_id, *args, **kwargs, add_data = {"message_reference": {"channel_id": self._channel_id, "guild_id": self._guild_id, "message_id": self.id}}))
    
    async def edit(self, content, *args, **kwargs):
        return Message(self.client, **await self.client.edit_message(self._channel_id, self.id, content, *args, **kwargs))

    async def type(self):
        return await self.client.type(self._channel_id)

    async def click_button(self, button):
        await self.payload._load_guild()
        await self.client.post(f"/interactions", {
            "application_id": self.author.id,
            "channel_id": self._channel_id,
            "data": {
                "component_type": 2,
                "custom_id": button.custom_id
            },
            "guild_id": self._guild_id,
            "message_flags": 0,
            "message_id": self.id,
            "nonce": self.nonce,
            "session_id": self.client.session_id,
            "type": 3
        })

    async def response_select(self, select, values: list):
        await self.payload._load_guild()
        await self.client.post(f"/interactions", {
            "application_id": str(self.author.id),
            "channel_id": str(self._channel_id),
            "data": {
                "component_type": select.type,
                "custom_id": select.custom_id,
                "type": 3,
                "values": values
            },
            "guild_id": str(self._guild_id),
            "message_flags": 0,
            "message_id": str(self.id),
            "nonce": str(self.nonce),
            "session_id": str(self.client.session_id),
            "type": 3
        })

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
        "parent",
        "type", 
        "tts", 
        "timestamp", 
        "_message_reference",
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
        "_channel_id", 
        "_author", 
        "attachments", 
        "_guild_id",
        "reactions"
    )
    
    def __init__(self, parent, **data):
        self.parent: Message = parent

        self.type: int = int(data.get("type", 0))
        self.tts: bool = data.get("tts")
        if data.get("timestamp"):
            self.timestamp: datetime.datetime = datetime.datetime.fromisoformat(data.get("timestamp"))
        self._message_reference: dict = data.get("message_reference")
        self._referenced_message: dict = data.get("referenced_message")
        self.pinned: bool = data.get("pinned")
        self.nonce: str = data.get("nonce")
        self.id: int = int(data.get("id", 0))
        if not self.nonce:
            self.nonce: int = self.id
        self.mentions: list = data.get("mentions")
        self.mention_roles: list = data.get("mention_roles")
        self.mention_everyone: bool = data.get("mention_everyone")
        if data.get("member"):
            self.member: Member = Member(self.parent.client, **data.get("member"))
        self.flags: int = int(data.get("flags", 0))
        self.embeds: list = (Embed(**d) for d in data.get("embeds"))
        self._edited_timestamp: str = data.get("edited_timestamp")
        self.content: str = data.get("content")
        self.components: list = tuple(MessageComponent(self, **d) for d in data.get("components"))
        self._channel_id: int = int(data.get("channel_id", 0))
        if data.get("author"):
            self._author = data.get("author")
        self.attachments: list = data.get("attachments")
        self.reactions: list = (Reaction(**d) for d in data.get("reactions", []))

    @property
    def referenced_message(self) -> Message:
        return Message(self.parent.client, **self._referenced_message)

    @property
    def message_reference(self) -> _MessageReference:
        return _MessageReference(**self._message_reference)

    async def guild(self) -> Guild:
        return Guild(**await self.parent.client.get_guild(self._guild_id))

    async def channel(self) -> Channel:
        return Channel(self.parent.client, **await self.parent.client.get_channel(self._channel_id))

    async def _load_guild(self):
        self._guild_id = (await self.channel()).guild_id

    @property
    def author(self) -> Author:
        return Author(self.parent.client, **self._author)

    @property
    def edited_timestamp(self):
        return datetime.datetime.fromisoformat(self._edited_timestamp)