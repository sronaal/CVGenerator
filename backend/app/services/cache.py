import hashlib
import json
import structlog

from app.config import get_settings

settings = get_settings()
logger = structlog.get_logger()


class AICache:
    def __init__(self):
        self._redis = None

    async def _get_redis(self):
        if self._redis is None:
            try:
                import redis.asyncio as redis
                self._redis = await redis.from_url(
                    settings.redis_url,
                    socket_connect_timeout=2,
                    socket_timeout=2,
                )
                await self._redis.ping()
            except Exception:
                logger.warning("redis_cache_unavailable", redis_url=settings.redis_url)
                self._redis = None
        return self._redis

    def _parse_key(self, raw_text: str) -> str:
        return f"ai:parse:{hashlib.sha256(raw_text.encode()).hexdigest()}"

    def _prompt_key(self, system: str, user: str) -> str:
        return f"ai:prompt:{hashlib.sha256((system + user).encode()).hexdigest()}"

    async def get_parse(self, raw_text: str) -> dict | None:
        r = await self._get_redis()
        if not r:
            return None
        try:
            data = await r.get(self._parse_key(raw_text))
            return json.loads(data) if data else None
        except Exception:
            return None

    async def set_parse(self, raw_text: str, data: dict):
        r = await self._get_redis()
        if not r:
            return
        try:
            await r.setex(self._parse_key(raw_text), settings.ai_cache_ttl, json.dumps(data))
        except Exception:
            pass

    async def get_prompt(self, system: str, user: str) -> str | None:
        r = await self._get_redis()
        if not r:
            return None
        try:
            data = await r.get(self._prompt_key(system, user))
            return data.decode() if data else None
        except Exception:
            return None

    async def set_prompt(self, system: str, user: str, result: str):
        r = await self._get_redis()
        if not r:
            return
        try:
            await r.setex(self._prompt_key(system, user), settings.ai_cache_ttl * 7, result)
        except Exception:
            pass
