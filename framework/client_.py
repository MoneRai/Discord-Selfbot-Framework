import aiohttp

class Requestor:
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth

    async def post(self, url, data):
        async with aiohttp.ClientSession(self.base_url, headers = {"Authorization": self.auth, "Content-Type": "application/json"}) as session:
            async with session.post(url, data = data) as response:
                return await response.json()
            
    async def get(self, url):
        async with aiohttp.ClientSession(self.base_url, headers = {"Authorization": self.auth, "Content-Type": "application/json"}) as session:
            async with session.get(url) as response:
                return await response.json()
            
    async def put(self, url, data):
        async with aiohttp.ClientSession(self.base_url, headers = {"Authorization": self.auth, "Content-Type": "application/json"}) as session:
            async with session.put(url, data = data) as response:
                return await response.json()