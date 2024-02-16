import re

class Emoji:
    def __init__(self, name: str, id: int, animated: bool = False):
        self.name: str = name
        self.id: int = id
        self.animated: bool = animated

    @property
    def string(self):
        return f"<{'a' if self.animated else ''}:{self.name}:{self.id}>"

    @property
    def url(self):
        return f"https://cdn.discordapp.com/emojis/{self.id}.{self.animated and 'gif' or 'png'}"

    @classmethod
    def parse(cls, string: str):
        return cls(*re.search(r"<a?(:\w+):(\d+)>", string).groups())

    def __str__(self):
        return self.string