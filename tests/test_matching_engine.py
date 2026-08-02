from decimal import Decimal
from orderbook.models import Order, Side, OrderType
from orderbook.matching_engine import MatchingEngine

# helper func to make orders
def make_order(order_id: int, side: Side, price: str, quantity: str, order_type=OrderType.LIMIT):
    return Order(
        order_id=order_id,
        side=side,
        price=Decimal(price),
        quantity=Decimal(quantity),
        order_type=order_type,
    )

def test_matching_engine_limit_buy_matches_best_ask():
    engine = MatchingEngine()
    engine.order_book.add_order(make_order(1, Side.SELL, "101.00", "5"))
    engine.order_book.add_order(make_order(2, Side.SELL, "102.00", "3"))

    incoming = make_order(3, Side.BUY, "105.00", "4")
    trades = engine.process_order(incoming)

    assert len(trades) == 1
    assert trades[0].buy_order_id == 3
    assert trades[0].sell_order_id == 1
    assert trades[0].price == Decimal("101.00")
    assert trades[0].quantity == Decimal("4")

    assert incoming.quantity == Decimal("0")
    assert engine.order_book.get_best_ask() == Decimal("102.00")
    assert engine.order_book.get_l2_snapshot() == ([], [(Decimal("102.00"), Decimal("3"))])

def test_matching_engine_partial_fill_of_resting_order():
    engine = MatchingEngine()
    engine.order_book.add_order(make_order(1, Side.SELL, "100.00", "10"))

    incoming = make_order(2, Side.BUY, "105.00", "3")
    trades = engine.process_order(incoming)

    assert len(trades) == 1
    assert trades[0].quantity == Decimal("3")
    assert engine.order_book.get_l2_snapshot() == ([], [(Decimal("100.00"), Decimal("7"))])
    assert engine.order_book.get_best_ask() == Decimal("100.00")

def test_matching_engine_limit_order_with_no_price_cross_rests_in_book():
    engine = MatchingEngine()
    engine.order_book.add_order(make_order(1, Side.SELL, "110.00", "5"))

    incoming = make_order(2, Side.BUY, "105.00", "5")
    trades = engine.process_order(incoming)

    assert trades == []
    assert incoming.quantity == Decimal("5")
    assert engine.order_book.get_best_bid() == Decimal("105.00")
    assert engine.order_book.get_l2_snapshot()[0] == [(Decimal("105.00"), Decimal("5"))]

def test_matching_engine_market_buy_consumes_resting_asks():
    engine = MatchingEngine()
    engine.order_book.add_order(make_order(1, Side.SELL, "101.00", "2"))
    engine.order_book.add_order(make_order(2, Side.SELL, "102.00", "2"))

    incoming = make_order(3, Side.BUY, "0.00", "3", order_type=OrderType.MARKET)
    trades = engine.process_order(incoming)

    assert len(trades) == 2
    assert trades[0].price == Decimal("101.00")
    assert trades[0].quantity == Decimal("2")
    assert trades[1].price == Decimal("102.00")
    assert trades[1].quantity == Decimal("1")
    assert incoming.quantity == Decimal("0")
    assert engine.order_book.get_best_ask() == Decimal("102.00")
    assert engine.order_book.get_l2_snapshot()[1] == [(Decimal("102.00"), Decimal("1"))]

def test_matching_engine_cancel_resting_order_after_fill_cleans_book():
    engine = MatchingEngine()
    engine.order_book.add_order(make_order(1, Side.BUY, "100.00", "5"))

    incoming = make_order(2, Side.SELL, "100.00", "5")
    trades = engine.process_order(incoming)

    assert len(trades) == 1
    assert engine.order_book.get_best_bid() is None
    assert engine.order_book.get_l2_snapshot() == ([], [])
