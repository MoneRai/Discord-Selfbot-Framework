import asyncio
import aiohttp
import json
import hashlib
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import parsers
from Models import Context, Message, Ready
from commands import Command
from client_ import Requestor
import traceback

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class Client(Requestor):
    def __init__(self, auth, prefix = ""):
        super().__init__(f"https://discord.com/api/v9", auth)
        self.auth = auth
        self.prefix = prefix
        self.gateway_listeners = {
            "MESSAGE_CREATE": [Message, self.process_commands],
            "READY": [Ready, self.deploy_ready]
        }
        self.commands = {}

    async def deploy_ready(self, ready: Ready):
        super().__init__(f"https://discord.com/api/v{ready.version}", self.auth)
        self.user = ready.user
        self.guilds = ready.guilds
        self.session_id = ready.session_id

    async def message(self, channel, content, *, tts = False, flags = 0, add_data = {}):
        return await self.post(f"/channels/{channel}/messages", {
            "mobile_network_type": "unknown",
            "content": content,
            "nonce": f"{hashlib.md5(int(datetime.datetime.now().timestamp()).to_bytes(64,'big')).hexdigest()[:25]}",
            "tts": tts,
            "flags": flags,
            **add_data
        })
    
    async def edit_message(self, channel, id, content):
        return await self.patch(f"/channels/{channel}/messages/{id}", {"content": content})

    async def get_messages(self, channel, *, limit = 50, before: int = None) -> list:
        if not before:
            return await self.get(f"/channels/{channel}/messages?limit={limit}")
        else:
            return await self.get(f"/channels/{channel}/messages?limit={limit}&before={before}")

    async def get_profile(self, id: int) -> dict:
        return await self.get(f"/users/{id}/profile?with_mutual_guilds=true&with_mutual_friends_count=true")

    async def get_user(self, id: int) -> dict:
        return await self.get(f"/users/{id}")
            
    async def get_channel(self, id: int) -> dict:
        return await self.get(f"/channels/{id}")
    
    async def get_guild(self, id) -> dict:
        return await self.get(f"/guilds/{id}")

    def command(self, name, *args, **kwargs) -> Command:
        def wrapped(coro):
            self.commands[name] = Command(coro, *args, **kwargs)
            return self.commands[name]
        return wrapped

    async def process_commands(self, message: Message):
        for key, callback in self.commands.items():
            if message.content.startswith(f"{self.prefix}{key}"):
                await callback.original(Context(self, message), *parsers.parse_args(message.content.lstrip(f"{self.prefix}{key}"), callback.original))

    def event(self, name: str):
        def wrapped(coro):
            async def call(*args, **kwargs):
                await coro(*args, **kwargs)
            self.gateway_listeners[name][1] = call
            return call
        return wrapped

    async def proceed_event(self, event):
        if self.gateway_listeners.get(event["t"]):
            await self.gateway_listeners[event["t"]][1](self.gateway_listeners[event["t"]][0](self, **event["d"]))

    async def run(self):
        async for event in self.run_gateway():
            await self.proceed_event(event)

    async def run_gateway(self):
        async with aiohttp.ClientSession(headers = {"Content-Type": "application/json", "Authorization": self.auth}) as session:
            async with session.get(f"https://discord.com/api/v9/gateway") as response:
                d = json.loads(await response.text())
                async with session.ws_connect(d['url'] + "?v=9&encoding=json") as websocket:
                    d = await websocket.receive_json()
                    await websocket.send_json({
                        "op": 2,
                        "d": {
                            "token": self.auth,
                            "properties": {
                                "browser_user_agent": "Monerai/1.0",
                            },
                            "compress": False
                        }
                    })

                    scheduler = AsyncIOScheduler()
                    i = 0

                    async def heatbeat():
                        await websocket.send_json({"op": 1, "d": i})
                    
                    scheduler.add_job(heatbeat, 'interval', seconds = d["d"]["heartbeat_interval"]/1000)
                    scheduler.start()

                    while True:
                        yield await websocket.receive_json()

    async def type(self, channel: int):
        await self.post(f"/channels/{channel}/typing", {})