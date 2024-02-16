from .emoji import Emoji

class Reaction:
    def __init__(self, **data):
        self.count: int = int(data.get("count", 0))
        self.count_details: dict = data.get("count_details")
        self.me: bool = data.get("me")
        self.emoji: Emoji = Emoji(**data.get("emoji"))
        self.burst_colors: list = data.get("burst_colors")