import urllib.parse
from aioproperty import aioproperty
from typing import List
import re
import json
import traceback, sys

class Message:
    @classmethod
    async def create(cls, __client, __data):
        instance = super().__new__(cls)
        await instance.__proceed_context(__client, __data)
        return instance

    async def __proceed_context(self, __client, __data):
        data = __data
        self.id:                      int | None = int(data.get("id", None))
        self.timestamp:               str | None = data.get("timestamp", None)
        self.pinned:                 bool | None = data.get("pinned", False)
        self.edited_timestamp:        str | None = data.get("edited_timestamp", None)
        self.author:               Author | dict | None = Author(data.get("author", {}))
        self.content:                 str | None = data.get("content", None)
        self._channel:            Channel | int | None = int(data.get("channel_id", None))
        self.mentions:               list | None = data.get("mentions", [])
        self.type:                    int | None = data.get("type", None)
        self.mention_everyone:       bool | None = data.get("mention_everyone", False)
        self.embeds:                 list | None = data.get("embeds", [])
        self.tts:                    bool | None = data.get("tts", False)
        self.attachments:            list | None = data.get("attachments", [])
        self.reactions:    List[Reaction] | None = [Reaction(reaction_data) for reaction_data in data.get("reactions", [])]
        self.__client = __client
        return self

    async def channel(self):
        return await Channel.create(self.__client, self._channel)

    async def add_reaction(self, emoji):
        if isinstance(emoji, Emoji):
            emoji = emoji.string
        await self.__client.put(f"/channels/{(await self.channel()).id}/messages/{self.id}/reactions/{urllib.parse.quote(emoji)}/{urllib.parse.quote('@')}me")

    async def edit(self, content):
        await self.__proceed_context(self.__client, await self.__client.patch(f"/channels/{(await self.channel()).id}/messages/{self.id}", body = json.dumps({"content": content})))

class Author:
    def __init__(self, data):
        self.username:                str | None = data.get("username", None)
        self.discriminator:           str | None = data.get("discriminator", None)
        self.id:                      int | None = int(data.get("id", None))
        self.avatar:                  str | None = data.get("avatar", None)

class Reaction:
    def __init__(self, data):
        self.count:                   int | None = data.get("count", 0)
        self.count_details:          dict | None = data.get("count_details", {})
        self.me:                     bool | None = data.get("me", False)
        emoji_data = data.get("emoji", {})
        self.emoji:                 Emoji | dict | None = Emoji(emoji_data)
        self.burst_colors:           list | None  = data.get("burst_colors", [])

class Emoji:
    def __init__(self, data):
        self.id:                      int | None = int(data.get("id", None))
        self.name:                    str | None = data.get("name", None)

    def __repr__(self):
        return f"<:{self.name}:{self.id}>"

    @property
    def string(self):
        return f"<:{self.name}:{self.id}>"

    @classmethod
    def parse(cls, string):
        result = re.compile(r"<?:?(.+):(\d+)>?").match(string)
        if result:
            return cls({"id": result.group(2), "name": result.group(1)})
        else:
            return None

class Guild:
    @classmethod
    async def create(cls, __client, __id):
        instance = super().__new__(cls)
        await instance.__proceed_context(__client, __id)
        return instance

    async def __proceed_context(self, __client, __id):
        data = await __client.get_guild(__id)
        try:
            self.id:                      int | None = int(data.get("id", 0))
            self.guild_id:                int | None = int(data.get("guild_id", 0))
            self.name:                    str | None = data.get("name", None)
            self.icon:                    str | None = data.get("icon", None)
            self.description:             str | None = data.get("description", None)
            self.splash:                  str | None = data.get("splash", None)
            self.discovery_splash:        str | None = data.get("discovery_splash", None)
            self.features:               list | None = data.get("features", [])
            self.emojis:                 list | None = data.get("emojis", [])
            self.banner:                  str | None = data.get("banner", None)
            self.owner_id:                int | None = int(data.get("owner_id", 0))
            self.region:                  str | None = data.get("region", None)
            self.afk_timeout:             int | None = data.get("afk_timeout", None)
            self.widget_enabled:         bool | None = data.get("widget_enabled", None)
            self.verification_level:      int | None = data.get("verification_level", None)
            self.roles:                  list | None = data.get("roles", [])
            self.message_notifications:   int | None = data.get("default_message_notifications", None)
            self.mfa_level:               int | None = data.get("mfa_level", None)
            self.explicit_filter:         int | None = data.get("explicit_content_filter", None)
            self.max_presences:           int | None = data.get("max_presences", None)
            self.max_members:             int | None = data.get("max_members", None)
            self.vanity_url_code:         str | None = data.get("vanity_url_code", None)
            self.premium_tier:            int | None = data.get("premium_tier", None)
            self.premium_count:           int | None = data.get("premium_subscription_count", None)
            self.system_channel_flags:    int | None = data.get("system_channel_flags", None)
            self.preferred_locale:        str | None = data.get("preferred_locale", None)
        except:
            traceback.print_exc(file=sys.stdout)

class Channel:
    @classmethod
    async def create(cls, __client, __id):
        instance = super().__new__(cls)
        await instance.__proceed_context(__client, __id)
        return instance

    async def guild(self):
        return await Guild.create(self.__client, self._guild)

    async def __proceed_context(self, __client, __id):
        data = (await __client.get_channel(__id))
        self.json = data
        self.id:                      int | None = int(data.get("id", 0))
        self._guild:                  int | None = int(data.get("guild_id", 0))
        self.name:                    str | None = data.get("name", None)
        self.type:                    int | None = data.get("type", None)
        self.position:                int | None = data.get("position", None)
        self.permissions_overwrites: list | None = data.get("permissons_overwrite", None)
        self.rate_limit:              int | None = data.get("rate_limit_per_user")
        self.nsfw:                   bool | None = data.get("nsfw", None)
        self.topic:                   str | None = data.get("topic", None)
        self.parent_id:               int | None = int(data.get("parent_id", None))
        self.auto_archive:            int | None = data.get("default_auto_archive_duration", None)
        self.__client = __client
        return self

class User:
    @classmethod
    async def create(cls, __client, __id):
        instance = super().__new__(cls)
        await instance.__proceed_context(__client, __id)
        return instance
    
    async def __proceed_context(self, __client, __id):
        data = (await __client.get_profile(__id))
        data = data['user']
        self.json = data
        self.id:                      int | None = int(data.get("id", 0))
        self.username:                str | None = data.get("username", None)
        self.global_name:             str | None = data.get("global_name", None)
        self.avatar:                  str | None = data.get("avatar", None)
        self.avatar_decoration_data:  str | None = data.get("avatar_decoration_data", None)
        self.discriminator:           str | None = data.get("discriminator", None)
        self.public_flags:            int | None = data.get("public_flags", None)
        self.flags:                   int | None = data.get("flags", None)
        self.banner:                  str | None = data.get("banner", None)
        self.banner_color:            int | None = data.get("banner_color", None)
        self.accent_color:            int | None = data.get("accent_color", None)
        self.bio:                     str | None = data.get("bio", None)

class Context:
    @classmethod
    async def create(cls, __client, __message):
        instance = super().__new__(cls)
        await instance.__proceed_context(__client, __message)
        return instance

    async def __proceed_context(self, client, message):
        self.author = await User.create(client, message.get("author", {}).get("id", {}))
        self.channel = await Channel.create(client,  message.get("channel_id", None))
        self.message = await Message.create(client, message)
        self.guild = await self.channel.guild()
        self.client = client

    async def send(self, content, **kwargs):
        return await self.client.message(self.message.id, str(content), **kwargs)

    async def reply(self, content, **kwargs):
        return await Message.create(self.client, await self.client.message(
            (await self.message.channel()).id, str(content), **kwargs,
            add_data = {
                "message_reference": {
                    "channel_id": (await self.message.channel()).id,
                    "message_id": self.message.id
            }
        }))