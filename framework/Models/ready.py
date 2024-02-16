from .user import User
from .guild import Guild

class Ready:
    def __init__(self, *args, **data):
        self.version = int(data.get("v", 0))
        self.user = User(self, **data.get("user"))
        self.guilds = (Guild(**d) for d in data.get("guilds", []))
        self.session_id = data.get("session_id")