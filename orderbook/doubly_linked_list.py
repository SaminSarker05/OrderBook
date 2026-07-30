from models import Order

class Node:
    def __init__(self, order: Order | None, prev: Order | None, next: Order | None):
        self.order = order
        self.prev = prev
        self.next = next
    

class DoublyLinkedList:
    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.size = 0
        
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def append(self, order: Order) -> Node:
        new_node = Node(order)
        next_node = self.head.next
        
        self.head.next = new_node
        new_node.prev = self.head
        
        next_node.prev = new_node
        new_node.next = next_node
        
        self.size += 1
        
    def is_empty(self) -> bool:
        return self.size == 0

    