import redis
import os
from dotenv import load_dotenv

load_dotenv()

class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0))
        )
    
    def set_quote(self, user_id: str, quote_data: dict, expiry: int = 60):
        """Store a quote with expiry time"""
        key = f"quote:{user_id}"
        self.client.setex(key, expiry, str(quote_data))
    
    def get_quote(self, user_id: str) -> dict:
        """Retrieve a quote for a user"""
        key = f"quote:{user_id}"
        data = self.client.get(key)
        return eval(data) if data else None
    
    def delete_quote(self, user_id: str):
        """Delete a quote"""
        key = f"quote:{user_id}"
        self.client.delete(key)

# Create a singleton instance
redis_client = RedisClient() 