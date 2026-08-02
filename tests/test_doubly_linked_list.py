from orderbook.doubly_linked_list import DoublyLinkedList, OrderNode
from decimal import Decimal
from orderbook.models import Order, Side

# helper func to make orders
def make_order(order_id: int) -> Order:
    return Order(
        order_id=order_id,
        side=Side.BUY,
        price=Decimal("100.00"),
        quantity=Decimal("1"),
    )

def test_doubly_linked_list_append_updates_length_and_links():
    linked_list = DoublyLinkedList()
    node = OrderNode(make_order(1))

    linked_list.append(node)

    assert len(linked_list) == 1
    assert linked_list.head.next is node
    assert linked_list.tail.prev is node
    assert node.prev is linked_list.head
    assert node.next is linked_list.tail

def test_doubly_linked_list_pop_front_returns_oldest_node():
    linked_list = DoublyLinkedList()
    nodes = [OrderNode(make_order(i)) for i in range(1, 4)]
    for node in nodes:
        linked_list.append(node)

    assert len(linked_list) == 3

    first = linked_list.pop_front()
    assert first is nodes[0]
    assert len(linked_list) == 2

    second = linked_list.pop_front()
    assert second is nodes[1]
    assert len(linked_list) == 1

    third = linked_list.pop_front()
    assert third is nodes[2]
    assert len(linked_list) == 0

def test_doubly_linked_list_remove_middle_node():
    linked_list = DoublyLinkedList()
    nodes = [OrderNode(make_order(i)) for i in range(1, 4)]
    for node in nodes:
        linked_list.append(node)

    removed = linked_list.remove(nodes[1])
    assert removed is nodes[1]
    assert len(linked_list) == 2

    assert nodes[0].next is nodes[2]
    assert nodes[2].prev is nodes[0]
    assert linked_list.head.next is nodes[0]
    assert linked_list.tail.prev is nodes[2]

def test_doubly_linked_list_pop_front_on_empty_list_returns_none():
    linked_list = DoublyLinkedList()
    assert linked_list.pop_front() is None
    assert len(linked_list) == 0

def test_doubly_linked_list_iteration_yields_nodes_in_order():
    linked_list = DoublyLinkedList()
    nodes = [OrderNode(make_order(i)) for i in range(1, 4)]
    for node in nodes:
        linked_list.append(node)

    assert list(linked_list) == nodes
