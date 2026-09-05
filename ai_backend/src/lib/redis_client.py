# lib/redis_client.py
import json
from fastapi.encoders import jsonable_encoder
from upstash_redis.asyncio import Redis
from dotenv import load_dotenv
load_dotenv()
import os

redis = Redis(
    url=os.getenv("UPSTASH_REDIS_REST_URL"),
    token=os.getenv("UPSTASH_REDIS_REST_TOKEN")
)

# -------- jwt blacklist (for logout) --------

async def blacklist_token(jti: str):
    key = f"blacklist_token:{jti}"
    await redis.set(key, "true", ex=24 * 3600)  # blacklist for 24 hours (or match your token expiry)

async def is_token_blacklisted(jti: str):
    key = f"blacklist_token:{jti}"
    return await redis.get(key) == "true"


# -------- caching responses --------

async def cache_response(key: str, value: dict, ttl: int):
    value = jsonable_encoder(value)
    await redis.set(key, json.dumps(value), ex=ttl)

async def get_cached_response(key: str):
    data = await redis.get(key)
    return json.loads(data) if data else None

async def delete_cache(key: str):
    await redis.delete(key)