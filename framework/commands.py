class Command:
    def __init__(self, callback, *args, **kwargs):
        self.__callback = callback

    async def __call__(self, *args, **kwargs):
        await self.__callback(*args, **kwargs)

    @property
    def original(self):
        return self.__callback