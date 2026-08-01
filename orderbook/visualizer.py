from decimal import Decimal
from typing import List
from orderbook.models import Trade
from orderbook.order_book import OrderBook

class OrderBookVisualizer:
    @staticmethod
    def render(order_book: OrderBook, recent_trades: list[Trade] = None, depth: int = 20) -> str:
        bids_l2, asks_l2 = order_book.get_l2_snapshot(depth=depth)
        