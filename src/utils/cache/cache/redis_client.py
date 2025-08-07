import redis.asyncio as redis
from datetime import datetime, timedelta, time
import hashlib
import json
import logging
from typing import Callable, Any, Awaitable
from functools import wraps

logger = logging.getLogger(__name__)

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

def get_seconds_until_1411() -> int:
    """
    Возвращает количество секунд до ближайших 14:11.
    """
    now = datetime.now()
    today_1411 = datetime.combine(now.date(), time(hour=14, minute=11))
    if now >= today_1411:
        today_1411 += timedelta(days=1)
    delta = today_1411 - now
    return int(delta.total_seconds())

def make_cache_key(prefix: str, *args: Any, **kwargs: Any) -> str:
    """
    Формирует ключ для кеша на основе префикса и параметров.
    """
    params = {"args": args, "kwargs": kwargs}
    serialized = json.dumps(params, sort_keys=True, default=str)
    hash_key = hashlib.md5(serialized.encode()).hexdigest()
    return f"{prefix}:{hash_key}"

async def get_dynamic_cached(self, **params) -> Any:
    """
    Получает данные с кешированием в Redis.
    """
    key = make_cache_key("dynamic", **params)
    cached = await redis_client.get(key)
    if cached:
        logger.info("Данные взяты из кеша")
        return json.loads(cached)
    result = await self.get_dynamic(**params)
    ttl = get_seconds_until_1411()
    await redis_client.set(key, json.dumps([r.model_dump() for r in result]), ex=ttl)
    logger.info("Данные сохранены в кеш")
    return result

def redis_cache(ttl_func: Callable[[], int] = get_seconds_until_1411) -> Callable:
    """
    Декоратор для кеширования результата функции в Redis.
    """
    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = make_cache_key(func.__name__, *args, **kwargs)
            try:
                cached = await redis_client.get(key)
                if cached:
                    logger.info("Данные взяты из кеша")
                    return json.loads(cached)
            except Exception as e:
                logger.warning(f"Ошибка Redis: {e}")
            result = await func(*args, **kwargs)
            try:
                await redis_client.set(key, json.dumps(result), ex=ttl_func())
                logger.info("Данные сохранены в кеш")
            except Exception as e:
                logger.warning(f"Ошибка Redis при сохранении: {e}")
            return result
        return wrapper
    return decorator
