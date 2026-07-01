from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict
# ============================================================
# TRADE
# ============================================================

@dataclass
class Trade:
    trade_id: int
    buy_order_id: int
    sell_order_id: int
    execution_price: float
    quantity: int
    timestamp: datetime

# This creates a class for the Trades occured and has related variables such as price, quantity, etc.

