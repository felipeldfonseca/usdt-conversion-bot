import time
from redis_client import redis_client

def lock_quote(user_id, brl, usdt, price):
    quote = {
        'brl': brl,
        'usdt': usdt,
        'price': price,
        'timestamp': time.time()
    }
    redis_client.set_quote(str(user_id), quote)
    return quote 