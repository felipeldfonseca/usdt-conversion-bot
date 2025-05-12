import time
import random

def confirm_pix(user_id):
    print(f"[PIX] Awaiting PIX for user {user_id}...")
    time.sleep(random.randint(5, 15))  # Simulate wait time
    return random.choice([True, False])  # 50% success rate for test 