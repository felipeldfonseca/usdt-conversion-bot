import uuid

def execute_trade(brl, usdt):
    print(f"[TRADE] Simulating trade: R${brl} → {usdt} USDT")
    return str(uuid.uuid4())  # Simulate TxID 