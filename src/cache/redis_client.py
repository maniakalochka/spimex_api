import redis.asyncio as redis
from datetime import datetime, timedelta, time
import hashlib
import json


redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

def get_seconds_until_1411() -> int:
    now = datetime.now()
    today_1411 = datetime.combine(now.date(), time(hour=14, minute=11))

    if now >= today_1411:
        today_1411 += timedelta(days=1)

    delta = today_1411 - now
    return int(delta.total_seconds())

def make_cache_key(prefix: str, params: dict) -> str:
    serialized = json.dumps(params, sort_keys=True)
    hash_key = hashlib.md5(serialized.encode()).hexdigest()
    return f"{prefix}:{hash_key}"


async def get_dynamic_cached(self, **params) -> list[SpimexTradingResult]:
    key = make_cache_key("dynamic", params)

    cached = await redis_client.get(key)
    if cached:
        return json.loads(cached)

    result = await self.get_dynamic(**params)

    ttl = get_seconds_until_1411()
    await redis_client.set(key, json.dumps([r.model_dump() for r in result]), ex=ttl)

    return result
