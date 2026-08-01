from decimal import Decimal
from orderbook.doubly_linked_list import DoublyLinkedList, OrderNode
from typing import Iterator

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
    
    def append(self, node: OrderNode) -> None:
        """
        Add an order node to tail of queue.
        """
        self.orders.append(node)
        self.total_quantity += node.order.quantity
    
    def remove(self, node: OrderNode) -> None:
        """
        Remove an order from any position within the queue.
        """
        self.orders.remove(node)
        self.total_quantity -= node.order.quantity
    
    def peek(self) -> OrderNode | None:
        """
        Get oldest/first order node without removing.
        """
        if len(self.orders) != 0:
            return self.orders.head.next

    def pop_front(self) -> OrderNode | None:
        """
        Remove and return the oldest order node.
        """
        node = self.orders.pop_front()
        if node:
            self.total_quantity -= node.order.quantity
        return node

    def __len__(self) -> int:
        return len(self.orders)

    def __iter__(self) -> Iterator[OrderNode]:
        return iter(self.orders)
