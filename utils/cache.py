from cachetools import TTLCache

CACHE = TTLCache(
    maxsize=1000,
    ttl=300
)
