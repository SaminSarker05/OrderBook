from decimal import Decimal
from sortedcontainers import SortedDict
from orderbook.models import Order, Side
from orderbook.order_book import OrderBook

# helper func to make orders
def make_order(order_id: int, side: Side, price: str, quantity: str) -> Order:
    return Order(
        order_id=order_id,
        side=side,
        price=Decimal(price),
        quantity=Decimal(quantity),
    )

def test_order_book_add_order_updates_best_prices_and_depth():
    book = OrderBook()

    book.add_order(make_order(1, Side.BUY, "100.00", "5"))
    book.add_order(make_order(2, Side.BUY, "101.00", "3"))
    book.add_order(make_order(3, Side.SELL, "102.00", "4"))
    book.add_order(make_order(4, Side.SELL, "103.00", "2"))

    assert book.get_best_bid() == Decimal("101.00")
    assert book.get_best_ask() == Decimal("102.00")
    assert book.get_spread() == Decimal("1.00")

    bids, asks = book.get_l2_snapshot()
    assert bids == [(Decimal("101.00"), Decimal("3")), (Decimal("100.00"), Decimal("5"))]
    assert asks == [(Decimal("102.00"), Decimal("4")), (Decimal("103.00"), Decimal("2"))]

def test_order_book_cancel_order_removes_node_and_price_level_when_empty():
    book = OrderBook()

    book.add_order(make_order(1, Side.BUY, "100.00", "5"))
    book.add_order(make_order(2, Side.SELL, "105.00", "1"))

    assert book.cancel_order(2) is True
    assert book.get_best_ask() is None
    assert book.get_spread() is None
    assert book.get_l2_snapshot() == ([(Decimal("100.00"), Decimal("5"))], [])

def test_order_book_cancel_nonexistent_order_returns_false():
    book = OrderBook()
    assert book.cancel_order(999) is False

def test_order_book_l2_snapshot_respects_depth_limit():
    book = OrderBook()

    for i in range(1, 6):
        book.add_order(make_order(i, Side.BUY, f"{100 + i}.00", "1"))
        book.add_order(make_order(100 + i, Side.SELL, f"{110 + i}.00", "1"))

    bids, asks = book.get_l2_snapshot(depth=3)
    assert len(bids) == 3
    assert len(asks) == 3
    assert bids[0][0] == Decimal("105.00")
    assert asks[0][0] == Decimal("111.00")
