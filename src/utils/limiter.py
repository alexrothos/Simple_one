import redis
from flask import request
from src.config import Config

redis_conn = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)


def rate_limit(key_prefix, limit, period):
    def decorator(f):
        def wrapper(*args, **kwargs):
            ip = request.remote_addr
            key = f"{key_prefix}:{ip}"
            current = redis_conn.get(key)

            if current and int(current) > limit:
                return {"error": "Too many requests"}, 429

            pipe = redis_conn.pipeline()
            pipe.incr(key)
            pipe.expire(key, period)
            pipe.execute()

            return f(*args, **kwargs)
        return wrapper
    return decorator
