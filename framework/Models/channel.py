from .guild import Guild
from .user import User

class Channel:
    def __new__(cls, client, **data):
        ident = {
            0: GuildTextChannel,
            1: DMChannel,
            2: GuildVoiceChannel,
            3: GroupDMChannel,
            4: ChannelCategory,
            5: GuildAnnouncementChannel
        }
        return ident[data.get("type", 0)](client, **data)

class GuildTextChannel(Channel):
    __slots__ = (
        "client",
        "id",
        "guild_id",
        "type",
        "name",
        "parent_id",
        "last_message_id",
        "permission_overwrites",
        "topic",
        "nsfw",
        "position"
    )
    
    def __init__(self, client, **data):
        self.client = client

        self.id: int = int(data.get("id", 0))
        self.guild_id: int = int(data.get("guild_id", 0))
        self.type: int = int(data.get("type", 0))
        self.name: str = data.get("name")
        self.parent_id: int = int(data.get("parent_id", 0))
        self.last_message_id: int = int(data.get("last_message_id", 0))
        self.permission_overwrites: list = data.get("permission_overwrites")
        self.topic: str = data.get("topic")
        self.nsfw: bool = data.get("nsfw")
        self.position: int = int(data.get("position", 0))

    @property
    def guild(self):
        return Guild(**self.client.get_guild(self.guild_id))

class GuildAnnouncementChannel(Channel):
    __slots__ = (
        "client",
        "id",
        "guild_id",
        "type",
        "name",
        "parent_id",
        "last_message_id",
        "permission_overwrites",
        "topic",
        "nsfw",
        "position",
        "default_auto_archive_duration"
    )

    def __init__(self, client, **data):
        self.client = client

        self.id: int = int(data.get("id", 0))
        self.guild_id: int = int(data.get("guild_id", 0))
        self.type: int = int(data.get("type", 0))
        self.name: str = data.get("name")
        self.parent_id: int = int(data.get("parent_id", 0))
        self.last_message_id: int = int(data.get("last_message_id", 0))
        self.permission_overwrites: list = data.get("permission_overwrites")
        self.topic: str = data.get("topic")
        self.nsfw: bool = data.get("nsfw")
        self.position: int = int(data.get("position", 0))
        self.default_auto_archive_duration: int = int(data.get("default_auto_archive_duration", 0))

class GuildVoiceChannel(Channel):
    __slots__ = (
        "client",
        "id",
        "guild_id",
        "type",
        "name",
        "parent_id",
        "permission_overwrites",
        "nsfw",
        "position",
        "bitrate",
        "user_limit",
        "rtc_region",
        "last_message_id",
        "rate_limit_per_user"
    )

    def __init__(self, client, **data):
        self.client = client

        self.id: int = int(data.get("id", 0))
        self.guild_id: int = int(data.get("guild_id", 0))
        self.type: int = int(data.get("type", 0))
        self.name: str = data.get("name")
        self.parent_id: int = int(data.get("parent_id", 0))
        self.permission_overwrites: list = data.get("permission_overwrites")
        self.nsfw: bool = data.get("nsfw")
        self.position: int = int(data.get("position", 0))
        self.bitrate: int = int(data.get("bitrate", 0))
        self.user_limit: int = int(data.get("user_limit", 0))
        self.rtc_region: str = data.get("rtc_region")
        self.last_message_id: int = int(data.get("last_message_id", 0))
        self.rate_limit_per_user: int = int(data.get("rate_limit_per_user", 0))

class DMChannel(Channel):
    __slots__ = (
        "client",
        "id",
        "last_message_id",
        "type",
        "recipients",
        "owner_id",
        "icon"
    )

    def __init__(self, client, **data):
        self.client = client

        self.id: int = int(data.get("id", 0))
        self.last_message_id: int = int(data.get("last_message_id", 0))
        self.type: int = int(data.get("type", 0))
        self.recipients: list = map(User(client, **d) for d in data.get("recipients"))

class GroupDMChannel(Channel):
    __slots__ = (
        "client",
        "id",
        "last_message_id",
        "type",
        "recipients",
        "owner_id",
        "icon"
    )

    def __init__(self, client, **data):
        self.client = client

        self.id: int = int(data.get("id", 0))
        self.last_message_id: int = int(data.get("last_message_id", 0))
        self.type: int = int(data.get("type", 0))
        self.recipients: list = map(User(client, **d) for d in data.get("recipients"))
        self.owner_id: int = int(data.get("owner_id", 0))
        self.icon: str = data.get("icon")

class ChannelCategory:
    __slots__ = (
        "client",
        "id",
        "guild_id",
        "type",
        "name",
        "parent_id",
        "permission_overwrites",
        "nsfw",
        "position"
    )

    def __init__(self, client, **data):
        self.client = client

        self.id: int = int(data.get("id", 0))
        self.guild_id: int = int(data.get("guild_id", 0))
        self.type: int = int(data.get("type", 0))
        self.name: str = data.get("name")
        self.parent_id: int = int(data.get("parent_id", 0))
        self.permission_overwrites: list = data.get("permission_overwrites")
        self.nsfw: bool = data.get("nsfw")
        self.position: int = int(data.get("position", 0))

class Thread(Channel):
    __slots__ = (
        "client",
        "id",
        "guild_id",
        "parent_id",
        "owner_id",
        "name",
        "type",
        "last_message_id",
        "message_count",
        "member_count",
        "rate_limit_per_user",
        "thread_metadata",
        "total_message_sent"
    )
    
    def __init__(self, client, **data):
        self.client = client

        self.id: int = int(data.get("id", 0))
        self.guild_id: int = int(data.get("guild_id", 0))
        self.parent_id: int = int(data.get("parent_id", 0))
        self.owner_id: int = int(data.get("owner_id", 0))
        self.name: str = data.get("name")
        self.type: int = int(data.get("type", 0))
        self.last_message_id: int = int(data.get("last_message_id", 0))
        self.message_count: int = int(data.get("message_count", 0))
        self.member_count: int = int(data.get("member_count", 0))
        self.rate_limit_per_user: int = int(data.get("rate_limit_per_user", 0))
        self.thread_metadata: dict = data.get("thread_metadata")
        self.total_message_sent: int = int(data.get("total_message_sent", 0))