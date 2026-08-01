from decimal import Decimal
from sortedcontainers import SortedDict
from orderbook.models import Order, Side
from orderbook.doubly_linked_list import OrderNode
from orderbook.price_level import PriceLevel

class OrderBook:
    """
    Price-time priority order book.
    - Bids = sorted in decreasing order
    - Asks = sorted in ascending order
    """
    def __init__(self):
        # store prices in descending order
        self.bids: SortedDict = SortedDict(lambda price: -price)
        self.asks: SortedDict = SortedDict()
        self.order_to_node: dict[int, OrderNode] = {}
    
    def get_best_bid(self) -> Decimal | None:
        if self.bids:
            return self.bids.peekitem(0)[0]
    
    def get_best_ask(self) -> Decimal | None:
        if self.asks:
            return self.asks.peekitem(0)[0]
    
    def get_spread(self) -> Decimal | None:
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()
        
        if best_bid is None or best_ask is None:
            return
        return best_ask - best_bid

    def add_order(self):
        pass

    def cancel_order(self):
        pass

    
        