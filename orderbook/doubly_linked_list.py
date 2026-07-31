from models import Order

class Node:
    def __init__(self, order: Order):
        self.order = order
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.size = 0

        self.head.next = self.tail
        self.tail.prev = self.head
    
    def unlink(self, node: Node) -> Node:
        next_node = node.next
        prev_node = node.prev

        prev_node.next = next_node
        next_node.prev = prev_node
        
        return node
    
    def _add_to_tail(self, node: Node):
        curr_oldest_order = self.tail.prev
        
        curr_oldest_order.next = node
        node.prev = curr_oldest_order
        
        node.next = self.tail
        self.tail.prev = node
    
    def append(self, order: Order) -> Node:
        new_node = Node(order)
        self._add_to_tail(new_node)

        self.size += 1
        return new_node

    def pop_left(self) -> Order | None:
        if self.size == 0:
            return None
    
        most_recent_order = self.head.next
        new_most_recent_order = self.head.next.next
        
        self.head.next = new_most_recent_order
        new_most_recent_order.prev = self.head
        
        self.size -= 1
        return most_recent_order.order
    
    def is_empty(self) -> bool:
        return self.head.next == self.tail
