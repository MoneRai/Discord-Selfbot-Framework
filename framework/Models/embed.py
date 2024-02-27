import datetime

class Embed:
    def __init__(self, **data):
        self.title: str = data.get("title")
        self.description: str = data.get("description")
        self.url: str = data.get("url")
        self.color: int = int(data.get("color", 0))
        if data.get("timestamp"):
            self.timestamp: datetime.datetime = datetime.datetime.fromisoformat(data.get("timestamp"))
        self.footer: EmbedFooter = EmbedFooter(**data.get("footer", {}))
        self.image: EmbedImage = EmbedImage(**data.get("image", {}))
        self.thumbnail: EmbedThumbnail = EmbedThumbnail(**data.get("thumbnail", {}))
        self.video: EmbedVideo = EmbedVideo(**data.get("video", {}))
        self.provider: EmbedProvider = EmbedProvider(**data.get("provider", {}))
        self.author: EmbedAuthor = EmbedAuthor(**data.get("author", {}))
        self.fields: list = tuple(EmbedField(**d) for d in data.get("fields", ()))
        self.type: str = data.get("type")

class EmbedThumbnail:
    def __init__(self, **data):
        self.url: str = data.get("url")
        self.proxy_url: str = data.get("proxy_url")
        self.width: int = int(data.get("width", 0))
        self.height: int = int(data.get("height", 0))

class EmbedVideo:
    def __init__(self, **data):
        self.url: str = data.get("url")
        self.proxy_url: str = data.get("proxy_url")
        self.height: int = int(data.get("height", 0))
        self.width: int = int(data.get("width", 0))

class EmbedImage:
    def __init__(self, **data):
        self.url: str = data.get("url")
        self.proxy_url: str = data.get("proxy_url")
        self.height: int = int(data.get("height", 0))
        self.width: int = int(data.get("width", 0))

class EmbedProvider:
    def __init__(self, **data):
        self.name: str = data.get("name")
        self.url: str = data.get("url")

class EmbedAuthor:
    def __init__(self, **data):
        self.name: str = data.get("name")
        self.url: str = data.get("url")
        self.icon_url: str = data.get("icon_url")
        self.proxy_icon_url: str = data.get("proxy_icon_url")

class EmbedFooter:
    def __init__(self, **data):
        self.text: str = data.get("text")
        self.icon_url: str = data.get("icon_url")
        self.proxy_icon_url: str = data.get("proxy_icon_url")

class EmbedField:
    def __init__(self, **data):
        self.name: str = data.get("name")
        self.value: str = data.get("value")
        self.inline: bool = data.get("inline")