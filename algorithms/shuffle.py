import random

class Shuffle:
    @staticmethod
    def is_empty(head):
        return head is None

    @staticmethod
    def count_song(head):
        count = 0
        current = head
        while current is not None:
            count += 1
            current = current.next
        return count
    
    @staticmethod
    def can_shuffle(head):
        return Shuffle.count_song(head) >= 2

    @staticmethod
    def linked_list_to_list(head):
        nodes = []
        current = head
        while current is not None:
            nodes.append(current)  
            current = current.next
        return nodes

    @staticmethod
    def fisher_yates_shuffle(node_list):
        n = len(node_list)
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            node_list[i], node_list[j] = node_list[j], node_list[i]
        return node_list

def fisher_yates_shuffle(dll):
    if Shuffle.is_empty(dll.head) or not Shuffle.can_shuffle(dll.head):
        return

    nodes = Shuffle.linked_list_to_list(dll.head)
    Shuffle.fisher_yates_shuffle(nodes)
    dll.from_list(nodes)

def restore_order(dll, original_order):
    dll.from_list(original_order)
