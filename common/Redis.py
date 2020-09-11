import redis
from .config import app_config


def getRedis():
    pool = redis.ConnectionPool(host=app_config.REDIS_HOST, port=app_config.REDIS_PORT)
    conn = redis.Redis(connection_pool=pool)

    conn.set('key', 'value')
    token = conn.get('key')
    return token
