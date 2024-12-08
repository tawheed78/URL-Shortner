"""
Redis Configuration Module
"""
import os
from dotenv import load_dotenv
import redis.asyncio as aioredis

load_dotenv()

host = os.getenv("HOST")

"Create Redis connection pool"
redis_client = aioredis.from_url(
  host,
  decode_responses=True,
  max_connections=10
)
async def get_redis_client():
    "Initialize redis client"
    return redis_client
