class Cache:
    def __init__(self, max_size):
        self.max_size = max_size
        self.cache = {}

    def put(self, key, value):
        if key not in self.cache:
            self.cache[key] = [value]
        else:
            if len(self.cache[key]) < self.max_size:
                self.cache[key].append(value)
            else:
                self.cache[key].pop(0)
                self.cache[key].append(value)

    def get(self, key):
        return self.cache.get(key, [])