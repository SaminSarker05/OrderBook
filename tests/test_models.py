from orderbook.models import Order, Trade, OrderType, Side
from decimal import Decimal

def test_create_order():
    order = Order(
        order_id=1, 
        side=Side.BUY, 
        price=Decimal('180.00'), 
        quantity=Decimal('50')
    )
    
    assert order.order_id == 1
    assert order.side == Side.BUY
    assert order.price == Decimal('180.00')
    assert order.quantity == Decimal('50')
    assert order.original_quantity == Decimal('50')
    assert order.is_filled is False
    assert order.fill_percentage == 0.0
    
def test_order_fill_percentage_after_partial_fill():
    order = Order(
        order_id=2,
        side=Side.SELL,
        price=Decimal("100.00"),
        quantity=Decimal("25"),
    )

    order.quantity = Decimal("10")
    assert order.original_quantity == Decimal("25")
    assert order.fill_percentage == 60.0
    assert order.is_filled is False

def test_order_is_filled_when_quantity_zero():
    order = Order(
        order_id=3,
        side=Side.BUY,
        price=Decimal("50.00"),
        quantity=Decimal("0"),
    )

    assert order.is_filled is True
    assert order.fill_percentage == 100.0
    
def test_trade_creation_fields():
    trade = Trade(
        trade_id=1,
        buy_order_id=10,
        sell_order_id=20,
        price=Decimal("175.50"),
        quantity=Decimal("5"),
    )

    assert trade.trade_id == 1
    assert trade.buy_order_id == 10
    assert trade.sell_order_id == 20
    assert trade.price == Decimal("175.50")
    assert trade.quantity == Decimal("5")
    assert hasattr(trade, "timestamp")
    assert isinstance(trade.timestamp, int)
