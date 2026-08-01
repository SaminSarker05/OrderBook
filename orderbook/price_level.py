from decimal import Decimal
from orderbook.DoublyLinkedList import DoublyLinkedList, OrderNode

class PriceLevel:
    """
    Price level in orderbook. All resting orders
    at a single price point. Maintains FIFO time priority
    using a DoublyLinkedList.
    """
    def __init__(self, price: Decimal):
        self.price = price
        self.orders = DoublyLinkedList()
        self.total_quantity: Decimal = Decimal('0')
    
    def append(self, node: OrderNOde) -> None:
        self.orders.append(node)
        self.total_quantity += node.order.quantity
    
    def remove(self, node: OrderNode) -> None:
        self.orders.remove(node)
        self.total_quantity -= node.order.quantity
    
    def peek(self) -> OrderNode | None:
        if len(self.orders) != 0:
            return self.orders.head.next

    def pop_front(self) -> OrderNode | None:
        node = self.orders.pop_front()
        if node:
            self.total_quantity -= node.order.quantity
        return node

    def __len__(self) -> int:
        return len(self.orders)

    def __iter__(self) -> Iterator[OrderNode]:
        return iter(self.orders)
