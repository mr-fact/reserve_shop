import redis
from pydantic.v1 import BaseSettings

from db.settings import redis_settings


def get_redis():
    return redis.Redis(connection_pool=redis.ConnectionPool(
        host=redis_settings.redis_host,
        port=redis_settings.redis_port,
        db=0,
        decode_responses=True
    ))
