import aiohttp
import json

class Requestor:
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth

    async def post(self, url, data, *, content_type = "application/json", headers = {}):
        async with aiohttp.ClientSession(headers = {"Authorization": self.auth, "Content-Type": content_type, **headers}) as session:
            async with session.post(self.base_url + url, data = json.dumps(data) if content_type == "application_json" else data) as response:
                if response.content_type == "application/json":
                    return await response.json()
                else:
                    return await response.text()
            
    async def get(self, url, *, content_type = "application/json", headers = {}):
        async with aiohttp.ClientSession(headers = {"Authorization": self.auth, "Content-Type": content_type, **headers}) as session:
            async with session.get(self.base_url + url) as response:
                if response.content_type == "application/json":
                    return await response.json()
                else:
                    return await response.text()

            
    async def put(self, url, data, *, content_type = "application/json", headers = {}):
        async with aiohttp.ClientSession(headers = {"Authorization": self.auth, "Content-Type": content_type, **headers}) as session:
            async with session.put(self.base_url + url, data = json.dumps(data) if content_type == "application_json" else data) as response:
                if response.content_type == "application/json":
                    return await response.json()
                else:
                    return await response.text()
                
    async def patch(self, url, data, *, content_type = "application/json", headers = {}):
        async with aiohttp.ClientSession(headers = {"Authorization": self.auth, "Content-Type": content_type, **headers}) as session:
            async with session.patch(self.base_url + url, data = json.dumps(data) if content_type == "application_json" else data) as response:
                if response.content_type == "application/json":
                    return await response.json()
                else:
                    return await response.text()