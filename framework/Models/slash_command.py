import json
import random

class SlashCommandOption:
    def __init__(self, **data):
        self.type: int = data.get("type")
        self.name: str = data.get("name")
        self.description: str = data.get("description")

    @property
    def dump(self):
        return {"type": self.type, "name": self.name, "description": self.description}

class SlashCommand:
    def __init__(self, client, **data):
        self.client = client

        self.type: int = int(data.get("type", 0))
        self.application_id: int = int(data.get("application_id", 0))
        self.id: int = int(data.get("id", 0))
        self.version: int = int(data.get("version", 0))
        self.name: str = data.get("name")
        self.description: str = data.get("description")
        self.options: list = tuple(SlashCommandOption(**d) for d in data.get("options", ()))
        self.integration_types: list = data.get("integration_types", [])
        self.global_popularity_rank: int = data.get("global_popularity_rank")
        self.description_localized: str = data.get("description_localized")
        self.name_localized: str = data.get("name_localized")

    def __load_options(self, options: tuple):
        result = [] 
        for option in options:
            for curopt in self.options:
                if option[0] == curopt.name:
                    result.append(SlashCommandOption(type = curopt.type, name = curopt.name, description = curopt.description))
        return result

    async def send(self, guild: int, channel: int, options: list = (), attachments: list = ()):
        data = json.dumps({
            "type": 2,
            "application_id": str(self.application_id),
            "guild_id": str(guild),
            "channel_id": str(channel),
            "session_id": self.client.session_id,
            "data": {
                "version": str(self.version),
                "id": str(self.id),
                "name": self.name,
                "type": self.type,
                "options": [
                    option.dump for option in options
                ],
                "attachments": [attachment.dump for attachment in self.__load_options(options)]
            },
            "nonce": None, 
            "analytics_location": "slash_ui"
        })
        data = json.dumps(data, ensure_ascii = False).replace('\\', '')[1:-1]
        data = await self.client.post("/interactions", f"--0\nContent-Disposition: form-data; name=\"payload_json\"\n\n{data}\n--0--", content_type = "multipart/form-data; boundary=0")