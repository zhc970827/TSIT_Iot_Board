import redis
from .config import app_config

def getRedis():
    conn = redis.Redis(host=app_config.REDIS_HOST, port=app_config.REDIS_PORT)
