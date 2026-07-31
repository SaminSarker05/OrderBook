from .doubly_linked_list import DoublyLinkedList, Node
from .models import Order

class PriceLevel:
    def __init__(self, price: float):
        self.price = price
        self.orders = DoublyLinkedList()
        self.total_volume: int = 0
    
    def add_order(self, order: Order) -> Node:
        new_node = self.orders.append(order)
        self.total_volume += new_node.order.quantity
        return new_node
    
    def remove_node(self, node: Node) -> None:
        node = self.orders.unlink(node)
        self.total_volume -= node.order.quantity
