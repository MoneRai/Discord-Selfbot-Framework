from .user import User

class Author(User):
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
    
    def __init__(self, client, **data):
        super().__init__(client, **data)