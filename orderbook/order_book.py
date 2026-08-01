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
        # map each price to a PriceLevel object in sorted dict
        # TODO(): make own sorteddict and red/black tree
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

    def add_order(self, order: Order):
        """
        Add order to book in logP time
        """
        book_side = self.bids if order.side == Side.BUY else self.asks
        if order.price not in self.book_side:
            self.book_side[order.price] = PriceLevel()
        
        node = OrderNode(order)
        book_side[order.price].append(node)
        self.order_to_node[order.order_id] = node
        
    def cancel_order(self, order_id: int) -> bool:
        """
        Cancel order using given order_id
        """
        if order_id not in self.order_to_node:
            return False
        node = self.order_to_node[order_id]
        order = node.order
        book_side = self.bids if order.side == Side.BUY else self.asks
        price_level = book_side.get(order.price)
        
        if price_level:
            # remove order from price level
            price_level.remove(node)
            if len(price_level) == 0:
                del book_side[order.price]
        
        del self.order_to_node[order_id]
        return True

    def get_l2_snapshot(self, depth: int = 20) -> tuple[list[tuple[Decimal, Decimal]], list[tuple[Decimal, Decimal]]]:
        """
        Display level 2 data of orderbook - best n (depth) prices 
        and total quantity for bid / ask sides of orderbook.
        """
        bids_l2 = [(price, level.total_quantity) for price, level in list(self.bids.items())[:depth]]
        asks_l2 = [(price, level.total_quantity) for price, level in list(self.asks.items())[:depth]]
        return bids_l2, asks_l2
