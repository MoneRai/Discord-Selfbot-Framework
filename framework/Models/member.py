from dataclasses import dataclass

@dataclass
class Member:
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