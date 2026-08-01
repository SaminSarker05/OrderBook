from .doubly_linked_list import DoublyLinkedList, Node
from .models import Order

class PriceLevel:
    """
    """
    def __init__(self, price: Decimal):
        self.price = price
        self.orders = DoublyLinkedList()
        self.total_quantity: Decimal = Decimal('0')
    
    def append(self, node: OrderNOde) -> None:
        self.orders.append(order)
        self.total_quantity += node.order.quantity
    
    def remove(self, node: OrderNode) -> None:
        self.orders.unlink(node)
        self.total_quantity -= node.order.quantity
    
    
    
