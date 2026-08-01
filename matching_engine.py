from decimal import Decimal
from orderbook.models import Order, Trade, Side, OrderType
from orderbook.order_book import OrderBook

class MatchingEngine:
    """
    Execute LIMIT and MARKET orders using price-time priority.
    """
    def __init__(self):
        self.order_book = OrderBook()
        self.trade_counter = 0
        self.trades: list[Trade] = []
    
    def process_order(self, order: Order) -> list[Trade]:
        executed_trades: list[Trade] = []
    
        while order.quantity > Decimal('0'):
            best_opposite_level = self._get_best_opposite_level(order.side)
            if not best_opposite_level:
                # no more orders that we can use
                break
            
            # ensure LIMIT order feasible
            if order.order_type == OrderType.LIMIT:
                if order.side == Side.BUY and order.price < best_opposite_level.price:
                    break
                if order.side == Side.SELL and order.price > best_opposite_level.price:
                    break
            
            # if no gap for LIMIT order or this is a MARKET order then continue
            resting_order_node = best_opposite_level.peek()
            if not resting_order_node:
                break
        
            resting_order = resting_order_node.order
            trade_quantity = min(order.quantity, resting_order.quantity)
            trade_price = resting_order.price  # trade occurs at maker/resting order price
            
            # record trade
            self.trade_counter += 1
            trade = Trade(
                trade_id = self.trade_counter,
                buy_order_id=order.order_id if order.side == Side.BUY else resting_order.order_id,
                sell_order_id=order.order_id if order.side == Side.SELL else resting_order.order_id,
                price=trade.price,
                quantity=trade_quantity
            )
            executed_trades.append(trade)
            self.trades.append(trade)
            
            # deduct order quantities
            order.quantity -= trade_quantity
            resting_order -= trade_quantity
            best_opposite_level.total_quantity -= trade_quantity
            
            # if resting order filled then remove from order book
            if resting_order.is_filled:
                self.order_book.cancel_order(resting_order.order_id)
            
        # if incoming order has remaining quantity -> add to resting book
        if order.quantity > Decimal('0') and order.order_type == OrderType.LIMIT:
            self.order_book.add_order(order)
        
        return executed_trades
        
    def _get_best_opposite_level(self, incoming_side: Side):
        book_side = self.order_books.asks if incoming_side == Side.BUY else self.order_book.bids
        if not book_side:
            return None
        _, price_level = book_side.peekitem[0]
        return price_level

    def cancel_order(self, order_id: int) -> bool:
        return self.order_book.cancel_order(order_id)
