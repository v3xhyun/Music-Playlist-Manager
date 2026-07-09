from data_structures.node import Node
from models.song import Song

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def append(self, song):
        new_node = Node(song)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1
        return new_node

    def prepend(self, song):
        new_node = Node(song)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1
        return new_node

    def insert_after(self, target_node, song):
        if target_node is self.tail:
            return self.append(song)

        new_node  = Node(song)
        next_node = target_node.next

        new_node.prev      = target_node
        new_node.next      = next_node
        target_node.next   = new_node
        next_node.prev     = new_node

        self._size += 1
        return new_node

    def delete(self, node):
        prev_node = node.prev
        next_node = node.next

        if prev_node:
            prev_node.next = next_node
        else:
            self.head = next_node

        if next_node:
            next_node.prev = prev_node
        else:
            self.tail = prev_node

        node.prev = None
        node.next = None
        self._size -= 1
        return node.data

    def find_by_id(self, song_id):
        current = self.head
        while current is not None:
            if current.data.song_id == song_id:
                return current
            current = current.next
        return None

    def find_by_title(self, keyword):
        results = []
        keyword_lower = keyword.lower()
        current = self.head
        while current is not None:
            if keyword_lower in current.data.title.lower():
                results.append(current)
            current = current.next
        return results

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current)
            current = current.next
        return result

    def from_list(self, nodes):
        if not nodes:
            self.head  = None
            self.tail  = None
            self._size = 0
            return

        for i, node in enumerate(nodes):
            node.prev = nodes[i - 1] if i > 0 else None
            node.next = nodes[i + 1] if i < len(nodes) - 1 else None

        self.head  = nodes[0]
        self.tail  = nodes[-1]
        self._size = len(nodes)

    def __len__(self):
        return self._size

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current
            current = current.next

    def __bool__(self):
        return self._size > 0

    def __repr__(self):
        songs = " <-> ".join(f"[{n.data.title}]" for n in self)
        return f"DoublyLinkedList({songs})"
