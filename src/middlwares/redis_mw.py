from __future__ import annotations

import logging
from typing import List

import orjson
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from utils.redis import (
    _cache_key,
    redis_client, seconds_until_1411
)

logger = logging.getLogger(__name__)


class RedisCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method != "GET" or not request.url.path.startswith("/spimex"):
            return await call_next(request)

        key = _cache_key(request)
        logger.info("cache key=%s", key)

        try:
            cached = await redis_client.get(key)
            if cached is not None:
                logger.info("cache HIT: %s", key)
                payload = orjson.loads(cached)
                return JSONResponse(payload)  # отдадим сразу, БД не трогаем
            logger.info("cache MISS: %s", key)
        except Exception as e:
            logger.warning("Redis read error (%s): %s", key, e)

        response: Response = await call_next(request)

        content_type = (response.headers.get("content-type") or "").lower()
        if response.status_code == 200 and content_type.startswith("application/json"):
            body_parts: List[bytes] = []
            async for chunk in response.body_iterator:  # type: ignore
                body_parts.append(chunk)
            raw = b"".join(body_parts)

            try:
                payload = orjson.loads(raw)
                await redis_client.set(
                    key, orjson.dumps(payload), ex=seconds_until_1411()
                )
            except Exception as e:
                logger.warning("Redis write error (%s): %s", key, e)

            headers = dict(response.headers)
            headers.pop("content-length", None)  # пересчитается
            headers.pop("transfer-encoding", None)  # не копируем
            return Response(
                content=raw,
                status_code=response.status_code,
                media_type=response.media_type,
                headers=headers,
                background=response.background,
            )
        return response
