from enum import Enum
from dataclasses import dataclass, field
import time

class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"

@dataclass
class Order:
    order_id: str
    side: Side
    price: float
    quantity: int
    timestamp: float = field(default_factory=time.time)

@dataclass
class Trade:
    trade_id: str
    # maker/taker represent different sides of
    # an executed trade.
    maker_order_id: str
    taker_order_id: str
    price: float
    quantity: int
    timestamp: float
