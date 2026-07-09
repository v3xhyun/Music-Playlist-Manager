class Node:
    def __init__(self, data):
        self.data = data  
        self.prev = None
        self.next = None

    def __repr__(self):
        return f"Node({self.data!r})"
