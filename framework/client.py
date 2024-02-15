import asyncio
import aiohttp
import json
import hashlib
import datetime
import websockets
import time
from events import *
import parsers
from context import Context
from commands import Command

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def dict_structure_to_str(dictionary, indent=0):
    result_str = ''
    for key, value in dictionary.items():
        result_str += ' ' * indent + str(key) + ': '
        if isinstance(value, dict):
            result_str += '\n' + dict_structure_to_str(value, indent + 4)
        else:
            result_str += type(value).__name__ + '\n'
    return result_str

class Requestor:
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth

    async def post(self, url, data):
        async with aiohttp.ClientSession(self.base_url, headers = {"Authorization": self.auth}) as session:
            async with session.post(url, data = data) as response:
                return await response.json()
            
    async def get(self, url):
        async with aiohttp.ClientSession(self.base_url, headers = {"Authorization": self.auth}) as session:
            async with session.get(url) as response:
                return await response.json()
            
    async def put(self, url, data):
        async with aiohttp.ClientSession(self.base_url, headers = {"Authorization": self.auth}) as session:
            async with session.put(url, data = data) as response:
                return await response.json()

class Client(Requestor):
    def __init__(self, auth, prefix = ""):
        self.auth = auth
        self.prefix = prefix
        self.gateway_listeners = {
            "MESSAGE_CREATE": [Message, self.process_commands],
            "MESSAGE_DELETE": []
        }
        self.commands = {}

    async def message(self, channel, content, *, tts = False, flags = 0, add_data = {}):
        async with aiohttp.ClientSession(headers = {"Authorization": self.auth, "Content-Type": "application/json"}) as session:
            async with session.post(f"https://discord.com/api/v9/channels/{channel}/messages", data = json.dumps({
                "mobile_network_type": "unknown",
                "content": content,
                "nonce": f"{hashlib.md5(int(datetime.datetime.now().timestamp()).to_bytes(64,'big')).hexdigest()[:25]}",
                "tts": tts,
                "flags": flags,
                **add_data
            })) as response:
                return json.loads(await response.text())

    async def get_messages(self, channel, *, limit = 50, before: int = None):
        if not before:
            async with aiohttp.ClientSession(headers = {"Content-Type": "application/json", "Authorization": self.auth}) as session:
                async with session.get(f"https://discord.com/api/v9/channels/{channel}/messages?limit={limit}") as response:
                    return json.loads(await response.text())
        else:
            async with aiohttp.ClientSession(headers = {"Content-Type": "application/json", "Authorization": self.auth}) as session:
                async with session.get(f"https://discord.com/api/v9/channels/{channel}/messages?limit={limit}&before={before}") as response:
                    return json.loads(await response.text())

    async def get_profile(self, id):
        async with aiohttp.ClientSession(headers = {"Content-Type": "application/json", "Authorization": self.auth}) as session:
            async with session.get(f"https://discord.com/api/v9/users/{id}/profile?with_mutual_guilds=true&with_mutual_friends_count=true") as response:
                return json.loads(await response.text())
            
    async def get_channel(self, id):
        async with aiohttp.ClientSession(headers = {"Content-Type": "application/json", "Authorization": self.auth}) as session:
            async with session.get(f"https://discord.com/api/v9/channels/{int(id)}") as response:
                return json.loads(await response.text())
    
    async def get_guild(self, id):
        async with aiohttp.ClientSession(headers = {"Content-Type": "application/json", "Authorization": self.auth}) as session:
            async with session.get(f"https://discord.com/api/v9/guilds/{id}") as response:
                return json.loads(await response.text())

    def command(self, name, *args, **kwargs):
        def wrapped(coro):
            self.commands[name] = Command(coro)
            return self.commands[name]
        return wrapped

    async def process_commands(self, message):
        for key, callback in self.commands.items():
            if message.content.startswith(f"{self.prefix}{key}"):
                await callback.original(await Context.create(self, message.data), *parsers.parse_args(message.content.lstrip(f"{self.prefix}{key}"), callback.original))

    def event(self, name):
        def wrapped(coro):
            async def call(*args, **kwargs):
                await coro(*args, **kwargs)
            self.gateway_listeners[name][1] = call
            return call
        return wrapped

    async def proceed_event(self, event):
        if self.gateway_listeners.get(event["t"]):
            await self.gateway_listeners[event["t"]][1](self.gateway_listeners[event["t"]][0](self, event["d"]))

    async def run(self):
        async for event in self.run_gateway():
            await self.proceed_event(event)

    async def run_gateway(self):
        async with aiohttp.ClientSession(headers = {"Content-Type": "application/json", "Authorization": self.auth}) as session:
            async with session.get(f"https://discord.com/api/v9/gateway") as response:
                d = json.loads(await response.text())
                async with websockets.connect(d['url'] + "?v=9&encoding=json") as websocket:
                    d = json.loads(await websocket.recv())
                    await websocket.send(json.dumps({
                        "op": 2,
                        "capabilities": 16381,
                        "d": {
                            "token": self.auth,
                            "properties": {
                                "os": "Windows",
                                "browser": "Chrome",
                                "device": "",
                                "system_locale": "ru-RU",
                                "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                "browser_version": "120.0.0.0",
                                "os_version": "10",
                                "referrer": "",
                                "referring_domain": "",
                                "referrer_current": "",
                                "referring_domain_current": "",
                                "release_channel": "stable",
                                "client_build_number": 252966,
                                "client_event_source": None
                            },
                            "presence": {
                                "status": "online",
                                "since": 0,
                                "activities": [],
                                "afk": False
                            },
                            "compress": False,
                            "client_state": {
                                "guild_versions": {},
                                "highest_last_message_id": "0",
                                "read_state_version": 0,
                                "user_guild_settings_version": -1,
                                "user_settings_version": -1,
                                "private_channels_version": "0",
                                "api_code_version": 0
                            }
                        }
                    }))

                    t = time.time()
                    i = 0

                    while True:
                        if (time.time() - t) > d["d"]["heartbeat_interval"]/1000:
                            await websocket.send(json.dumps({"op": 1, "d": i}))
                            i += 1
                            t = time.time()

                        try:
                            recv_task = asyncio.ensure_future(websocket.recv())
                            done, _ = await asyncio.wait({recv_task}, timeout=1.0)
                            if recv_task in done:
                                yield json.loads(recv_task.result())
                        except Exception as E:
                            ...

    async def type(self, channel):
        async with aiohttp.ClientSession(headers = {"Content-Type": "application/json", "Authorization": self.auth}) as session:
            async with session.post(f"https://discord.com/api/v9/channels/{channel}/typing"):
                return

    async def get_ch_msgs(self, channel, limit = 1000):
        msgs = []
        n = None

        for j in range(limit//50):
            messages = await self.get_messages(channel, before = n)
            try:
                print(j*50, messages[0])
            except:
                break
            msgs.extend(messages)
            n = msgs[-1]["id"]
            await asyncio.sleep(2)
        return msgs