from __init__ import Guild

class Channel:
    __slots__ = (
        "client",
        "id",
        "guild_id",
        "type",
        "name",
        "parent_id",
        "last_message_id",
        "last_pin_timestamp",
        "permission_overwrites"
    )
    
    def __init__(self, client, **data):
        self.client = client
        self.id: int = int(data.get("id"))
        self.guild_id: int = int(data.get("guild_id"))
        self.type: int = int(data.get("type"))
        self.name: str = data.get("name")
        self.parent_id: int = int(data.get("parent_id"))
        self.last_message_id: int = int(data.get("last_message_id"))
        self.last_pin_timestamp: str = data.get("last_pin_timestamp")
        self.permission_overwrites: list = data.get("permission_overwrites")

    @property
    def guild(self):
        return Guild(**self.client.get_guild(self.guild_id))