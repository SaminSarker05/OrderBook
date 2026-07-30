from enum import Enum
from dataclasses import dataclass

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
    timestamp: float

@dataclass
class Trade:
    trade_id: str
    # maker/taker represent different sides of
    # an executed trade.
    maker_order_id: str
    taker_order_id: str
    price: float
    quantity: float
    timestamp: float
