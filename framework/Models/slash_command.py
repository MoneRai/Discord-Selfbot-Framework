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

    async def send(self, guild: int, channel: int, options: list = (), attachments: list = ()):
        data = json.dumps({
            "type": self.type,
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
                "attachments": attachment.dump for attachment in attachments
            },
            "nonce": None, 
            "analytics_location": "slash_ui"
        })
        num = random.randint(10*29, 10*30-1)
        await self.client.post("/interactions", f"{'-' * 29}{num}\n{data}\n{'-' * 29}{num}--")

class SlashCommandGroup:
    def __init__(self, client, parent, **data):
        self.client = client
        self.parent = parent

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

    async def send(self, subcommand: str, guild: int, channel: int, options: list = (), attachments: list = ()):
        ...