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
