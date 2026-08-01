
from orderbook.price_level import PriceLevel
from decimal import Decimal
from orderbook.order_book import OrderBook
from matching_engine import MatchingEngine

test = PriceLevel(Decimal("100"))
orderbook = OrderBook()
engine = MatchingEngine()

print("hello world")