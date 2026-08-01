from orderbook.models import Order

class OrderNode:
    """
    Node in double linked list wrapping an Order.
    """
    def __init__(self, order: Order):
        self.order = order
        self.next = None
        self.prev = None

class DoublyLinkedList:
    """
    Doubly Linked List reprseting a FIFO time-priority queue.
    O(1) append to tail, pop from head, and removal of nodes.
    """
    def __init__(self):
        self.head = OrderNode()
        self.tail = OrderNode()
        self._size: int = 0

        self.head.next = self.tail
        self.tail.prev = self.head
    
    def append(self, new_node: OrderNode) -> None:
        self._add_to_tail(new_node)

        self._size += 1
    
    def remove(self, node: OrderNode) -> Node:
        next_node = node.next
        prev_node = node.prev

        prev_node.next = next_node
        next_node.prev = prev_node
        
        self._size -= 1
        return node
    
    def _add_to_tail(self, node: OrderNode):
        curr_oldest_order = self.tail.prev
        
        curr_oldest_order.next = node
        node.prev = curr_oldest_order
        
        node.next = self.tail
        self.tail.prev = node

    def pop_front(self) -> OrderNode | None:
        if self._size == 0:
            return None
    
        most_recent_node = self.head.next
        self.remove(most_recent_node)
        return most_recent_node
    
    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[OrderNode]:
        curr = self.head.next
        while curr != self.tail:
            yield curr
            curr = curr.next
