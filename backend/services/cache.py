from cachetools import TTLCache

conversation_cache = TTLCache(
    maxsize=100,
    ttl=60
)