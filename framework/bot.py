from client import Client
import asyncio
from Models import *
from typing import List
from Models.slash_command import SlashCommand, SlashCommandGroup

class Bot(Client):
    def __init__(self, token: str, *args, **kwargs):
        super().__init__(token, *args, **kwargs)

    def run(self):
        self.loop.run_until_complete(super().run())

    async def fetch_guild(self, id: int) -> Guild:
        return Guild(**await super().get_guild(id))

    async def fetch_channel(self, id: int) -> Channel:
        return Channel(**await super().get_channel(id))

    async def fetch_user(self, id: int) -> User:
        return User(**await super().get_user(id))

    async def get_messages(self, channel, *, limit = 50, before: int = None, check = None) -> List[Message]:
        return [Message(self, **data) for data in await super().get_messages(channel, limit = limit, before = before, check = check)]
    
    async def get_message(self, channel, *, limit = 1000, before: int = None, check = None) -> Message:
        if not check:
            return (await self.get_messages(channel))[0]
        else:
            for _ in range(limit // 50):
                messages = await self.get_messages(channel, before = before)
                for message in messages:
                    if check(message):
                        return message
                    before = message.id

    async def get_messages_per(self, channel, *, limit: int = 1000, before: int = None, per: int = 50, check = None) -> list:
        result = []

        for _ in range(limit // per):
            messages = await self.get_messages(channel, limit = per, before = before, check = check)
            before = messages[-1].id
            result.extend(messages)
        return result

    async def get_slash_command(self, guild, name):
        for command in (await self.get_slash_commands_config(guild))["application_commands"]:
            if command["name"] == name:
                if command["options"]:
                    if command["options"][0]["type"] == 1:
                        return SlashCommandGroup(self, **command)
                    else:
                        return SlashCommand(self, **command)
                else:
                    return SlashCommand(self, **command)
        else:
            raise KeyError(("Slash command with that name not found"))
