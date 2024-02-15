from dataclasses import dataclass

@dataclass
class Author:
    username: str
    public_flags: str
    premium_type: str
    id: int
    global_name: str
    discriminator: str
    avatar: str