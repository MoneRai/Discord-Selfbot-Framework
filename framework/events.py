class Event:
    def __init__(self, client, event, callback):
        self.client = client
        self.event = event
        self.callback = callback

    def __call__(self, *args, **kwargs):
        self.client.loop.create_task(self.callback(*args, **kwargs))