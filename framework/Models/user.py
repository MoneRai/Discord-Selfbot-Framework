class User:
    def __init__(self, client, **data):
        self.client = client
        self.payload = UserPayload(**data)

    def __getattr__(self, name):
        return getattr(self.payload, name)

    def send(self, *args, **kwargs):
        return self.client.message(self.id, *args, **kwargs)

class UserPayload:
    __slots__ = (
        "id",
        "username",
        "global_name",
        "avatar",
        "avatar_decoration_data",
        "discriminator",
        "public_flags",
        "flags",
        "banner",
        "banner_color",
        "accent_color",
        "bio"
    )

    def __init__(self, **data):
        self.id: int = int(data.get("id", 0))
        self.username: str = data.get("username")
        self.global_name: str = data.get("global_name")
        self.avatar: str = data.get("avatar")
        self.avatar_decoration_data: str = data.get("avatar_decoration_data")
        self.discriminator: str = data.get("discriminator")
        self.public_flags: int = int(data.get("public_flags", 0))
        self.flags: int = int(data.get("flags", 0))
        self.banner: str = data.get("banner")
        self.banner_color: int = int(data.get("banner_color", 0))
        self.accent_color: int = int(data.get("accent_color", 0))
        self.bio: str = data.get("bio")