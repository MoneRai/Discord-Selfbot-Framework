import asyncio
import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import parsers
from Models import Context, Message, Ready
from commands import Command
from client_ import Requestor
from events import Event
from cache import Cache
import datetime

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class Client(Requestor):
    def __init__(self, auth, prefix = "", loop: asyncio.AbstractEventLoop = None, cache_size = 1024):
        super().__init__(f"https://discord.com/api/v9", auth)
        if loop:
            self.loop = loop
        else:
            self.loop = asyncio.new_event_loop()
        self.auth = auth
        self.prefix = prefix
        self._types = {
            "MESSAGE_CREATE": Message,
            "READY": Ready
        }
        self.gateway_listeners = {
            "MESSAGE_CREATE": []
        }
        self.commands = {}
        self._events = {
            "MESSAGE_CREATE": []
        }
        self._message_cache = Cache(cache_size)
        self.started = False

    async def deploy_ready(self, ready: Ready):
        super().__init__(f"https://discord.com/api/v{ready.version}", self.auth)
        self.user = ready.user
        self.guilds = ready.guilds
        self.session_id = ready.session_id

        @self.event("MESSAGE_CREATE")
        async def _(message):
            if message:
                self._message_cache.put("MESSAGES", message)
                await self.process_commands(message)
        self.started = True

    async def message(self, channel, content, *, tts = False, flags = 0, add_data = {}):
        last = (await self.get_messages(channel, limit = 1))[0]
        if isinstance(last, dict):
            last = Message(self, **last)
        return await self.post(f"/channels/{channel}/messages", {
            "mobile_network_type": "unknown",
            "content": content,
            "nonce": last.nonce + 1,
            "tts": tts,
            "flags": flags,
            **add_data
        })
    
    async def edit_message(self, channel, id, content) -> dict:
        return await self.patch(f"/channels/{channel}/messages/{id}", {"content": content})

    async def get_message(self, channel, *, limit = 1000, before: int = None, check = None) -> dict:
        if not check:
            return await self.get_messages(channel)[0]
        else:
            for _ in range(limit // 50):
                messages = await self.get_messages(channel, before = before)
                for message in messages:
                    if check(message):
                        return message
                    before = message["id"]

    async def get_messages(self, channel, *, limit = 50, before: int = None, check = None) -> list:
        if not check:
            if not before:
                return await self.get(f"/channels/{channel}/messages?limit={limit}")
            else:
                return await self.get(f"/channels/{channel}/messages?limit={limit}&before={before}")
        else:
            if not before:
                messages = await self.get(f"/channels/{channel}/messages?limit={limit}")
            else:
                messages = await self.get(f"/channels/{channel}/messages?limit={limit}&before={before}")
            for message in messages:
                if not check(message):
                    messages.remove(message)
            return messages
        
    async def get_messages_per(self, channel, *, limit: int = 1000, before: int = None, per: int = 50, check = None) -> list:
        result = []

        for _ in range(limit // per):
            messages = await self.get_messages(channel, limit = per, before = before, check = check)
            before = messages[-1]["id"]
            result.extend(messages)
        return result

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
                await callback(Context(self, message), *parsers.parse_args(message.content.lstrip(f"{self.prefix}{key}"), callback.original))

    def event(self, name: str):
        def wrapped(coro):
            event = Event(self, name, coro)
            self._events[name].append(event)
            return coro
        return wrapped

    async def proceed_event(self, event):
        if event["t"] == "READY":
            await self.deploy_ready(self._types[event["t"]](**event["d"]))

        if (callbacks := self._events.get(event["t"])):
            for callback in callbacks:
                callback(self._types[event["t"]](self, **event["d"]))

        for future, check in self.gateway_listeners.get(event["t"], {}):
            if check(r := self._types[event["t"]](self, **event["d"])):
                if not future.done() and not future.cancelled():
                    future.set_result(r)
                self.gateway_listeners[event["t"]].remove((future, check))

    async def run(self):
        async for event in self.run_gateway():
            self.loop.create_task(self.proceed_event(event))

    async def run_gateway(self):
        async with aiohttp.ClientSession(headers = {"Content-Type": "application/json", "Authorization": self.auth}) as session:
            async with session.get(f"https://discord.com/api/v9/gateway") as response:
                d = await response.json()
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

    async def wait_for(self, event: str, check = lambda element: True, timeout = None):         
        future = self.loop.create_future()
        try:
            listeners = self.gateway_listeners[event]
        except:
            listeners = []
            self.gateway_listeners[event] = listeners
        
        listeners.append((future, check))
        return await asyncio.wait_for(future, timeout)

    async def type(self, channel: int):
        await self.post(f"/channels/{channel}/typing", {})