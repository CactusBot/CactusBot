import json
import time


class CacheUtils:

    # You have found MysticalMage's code, turn back now, no good lies ahead
    def __init__(self, filename):
        self.filename = filename

    def in_cache(self, user):
        """ Returns if user is in the cache. """
        with open(self.filename) as cache:
            cachedata = json.load(cache)
        return user in cachedata

    def cache_add(self, user):
        """ Adds user to cache with newline at end. """
        with open(self.filename, "r") as cache:
            cachedata = json.load(cache)
        cachedata[user] = time.time()
        with open(self.filename, "w") as cache:
            json.dump(cachedata, cache, indent=2)

    def return_data(self, user):
        """ Returns the data in cache for specified location. """
        with open(self.filename) as cache:
            cachedata = json.load(cache)
            return cachedata[user]
