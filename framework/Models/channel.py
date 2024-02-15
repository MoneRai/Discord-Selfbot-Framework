from .guild import Guild
from .user import User

class Channel:
    pass

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
    def __init__(self, client, **data):
        self.client = client

        self.id: int = int(data.get("id", 0))
        self.last_message_id: int = int(data.get("last_message_id", 0))
        self.type: int = int(data.get("type", 0))
        self.recipients: list = map(User(client, **d) for d in data.get("recipients"))

class GroupDMChannel(Channel):
    def __init__(self, client, **data):
        self.client = client

        self.id: int = int(data.get("id", 0))
        self.last_message_id: int = int(data.get("last_message_id", 0))
        self.type: int = int(data.get("type", 0))
        self.recipients: list = map(User(client, **d) for d in data.get("recipients"))
        self.owner_id: int = int(data.get("owner_id", 0))
        self.icon: str = data.get("icon")

class ChannelCategory:
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