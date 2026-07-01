from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict

# ============================================================
# ORDER
# ============================================================


@dataclass
class Order:
    order_id: int     
    side: str                # BUY OR SELL.    
    price: float
    quantity: int            # NUMBER OF SECURITIES.
    timestamp: datetime      # TIME OF ORDER.

# This creates a class for Orders and has related variables such as price, quantity, etc.
