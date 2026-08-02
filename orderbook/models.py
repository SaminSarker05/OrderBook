from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from decimal import Decimal
import time

class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(str, Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"

@dataclass
class Order:
    order_id: int
    side: Side
    price: Decimal
    quantity: Decimal
    original_quantity: Decimal = field(init=False)
    order_type: OrderType = OrderType.LIMIT
    timestamp: int = field(default_factory=time.perf_counter_ns)
    
    def __post_init__(self):
        self.original_quantity = self.quantity
    
    @property
    def is_filled(self) -> bool:
        return self.quantity <= 0

    @property
    def fill_percentage(self) -> float:
        if self.original_quantity == Decimal('0'):
            return 100.0
        filled = self.original_quantity - self.quantity
        return float((filled / self.original_quantity) * Decimal('100'))

@dataclass
class Trade: 
    trade_id: int
    buy_order_id: int
    sell_order_id: int
    price: Decimal
    quantity: Decimal
    timestamp: int = field(default_factory=time.perf_counter_ns)
