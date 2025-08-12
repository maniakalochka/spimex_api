# utils/cache/redis_client.py
from datetime import datetime, time, timedelta

import redis.asyncio as redis
from fastapi import Request

from core.config import settings


redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=False
)


def seconds_until_1411() -> int:
    now = datetime.now()
    cutoff = datetime.combine(now.date(), time(14, 11))
    if now >= cutoff:
        cutoff += timedelta(days=1)
    return max(1, int((cutoff - now).total_seconds()))


def _normalized_path(path: str) -> str:
    return path[:-1] if path.endswith("/") and path != "/" else path


def _normalize_query(request: Request) -> str:
    items = []
    for k, v in request.query_params.multi_items():
        if v is None or v == "":
            continue
        items.append((k, v))
    items.sort(key=lambda kv: (kv[0], kv[1]))
    return "&".join(f"{k}={v}" for k, v in items)


def _cache_key(request: Request) -> str:
    path = _normalized_path(request.url.path)
    qp = _normalize_query(request)
    return f"{path}?{qp}"
