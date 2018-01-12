import collections


class LRUCache(collections.OrderedDict):
    def __init__(self, size=5, *args, **kwds):
        super().__init__(*args, **kwds)
        self.size = size
        self.cache = collections.OrderedDict()

    def get(self, key, **kwargs):
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        else:
            return None

    def set(self, key, value):
        if key in self.cache:
            self.cache.pop(key)
            self.cache[key] = value
        elif self.size == len(self.cache):
            self.cache.popitem(last=False)
            self.cache[key] = value
        else:
            self.cache[key] = value


if __name__ == '__main__':
    cache = LRUCache()
    cache.set('fuck1', 1)
    cache.set('fuck2', 2)
    cache.set('fuck3', 3)
    cache.set('fuck4', 4)
    cache.set('fuck5', 5)

    print(cache.get('fuck5'))
    print(cache.get('fuck1'))

    cache.set('fuck6', 6)

    print(cache.get('fuck1'))
    print(cache.get('fuck2'))
    print(cache.get('fuck3'))
    print(cache.get('fuck4'))
    print(cache.get('fuck5'))
    print(cache.get('fuck6'))
