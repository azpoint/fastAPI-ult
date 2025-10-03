from redis.asyncio import Redis
from app.env_config import REDIS_HOST, REDIS_PORT

_token_blacklist = Redis(
    host=REDIS_HOST if REDIS_HOST is not None else "localhost",
    port=int(REDIS_PORT) if REDIS_PORT is not None else 6379,
    db=0,
)


async def add_jti_to_blacklist(jti: str):
    await _token_blacklist.set(jti, "blacklisted")


async def is_jti_blacklisted(jti: str) -> bool:
    return await _token_blacklist.exists(jti)
