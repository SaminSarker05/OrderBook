from decimal import Decimal
from orderbook.models import Order, Side
from orderbook.doubly_linked_list import OrderNode
from orderbook.price_level import PriceLevel

# helper func to make orders
def make_order(order_id: int, quantity: str = "1") -> Order:
    return Order(
        order_id=order_id,
        side=Side.BUY,
        price=Decimal("100.00"),
        quantity=Decimal(quantity),
    )

def test_price_level_append_updates_length_and_total_quantity():
    level = PriceLevel(Decimal("100.00"))
    node1 = OrderNode(make_order(1, "5"))
    node2 = OrderNode(make_order(2, "10"))

    level.append(node1)
    level.append(node2)

    assert len(level) == 2
    assert level.total_quantity == Decimal("15")
    assert level.peek() is node1

def test_price_level_pop_front_returns_oldest_and_adjusts_total():
    level = PriceLevel(Decimal("100.00"))
    nodes = [OrderNode(make_order(i, "5")) for i in range(1, 4)]
    for node in nodes:
        level.append(node)

    assert len(level) == 3
    oldest = level.pop_front()
    assert oldest is nodes[0]
    assert len(level) == 2
    assert level.total_quantity == Decimal("10")
    assert level.peek() is nodes[1]

def test_price_level_remove_middle_node_updates_total_and_links():
    level = PriceLevel(Decimal("100.00"))
    nodes = [OrderNode(make_order(i, "5")) for i in range(1, 4)]
    for node in nodes:
        level.append(node)

    level.remove(nodes[1])
    assert len(level) == 2
    assert level.total_quantity == Decimal("10")
    assert list(level) == [nodes[0], nodes[2]]
    assert level.peek() is nodes[0]


def test_price_level_peek_returns_none_when_empty():
    level = PriceLevel(Decimal("100.00"))
    assert level.peek() is None
    assert len(level) == 0
    assert level.total_quantity == Decimal("0")
