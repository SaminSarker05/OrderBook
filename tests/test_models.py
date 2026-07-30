from orderbook import models

def test_create_order():
    order = Order(order_id="01", side=Side.BUY, price=180.0, quantity=50)
    
    assert order.order_id == "01"
    assert order.side == Side.BUY
    assert order.price == 180.0
    assert order.quantity == 50
    
