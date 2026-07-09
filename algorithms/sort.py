import time

def split(head):
    if head is None or head.next is None:
        return head, None

    slow = head
    fast = head.next

    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next

    right_head = slow.next
    slow.next = None
    
    if right_head is not None:
        right_head.prev = None  

    return head, right_head

def merge(left, right, key_func, reverse=False):
    if left is None: return right
    if right is None: return left   

    left_value = key_func(left)
    right_value = key_func(right)

    take_left = left_value >= right_value if reverse else left_value <= right_value

    if take_left:
        result = left
        next_node = merge(left.next, right, key_func, reverse)
        result.next = next_node
        if next_node is not None: next_node.prev = result 
    else:
        result = right
        next_node = merge(left, right.next, key_func, reverse)
        result.next = next_node
        if next_node is not None: next_node.prev = result 
            
    result.prev = None
    return result

def merge_sort(head, key_func, reverse=False):
    if head is None or head.next is None:
        return head

    left, right = split(head)

    left = merge_sort(left, key_func, reverse)
    right = merge_sort(right, key_func, reverse)

    return merge(left, right, key_func, reverse)

def sort_playlist(dll, sort_key="title", algorithm="merge"):
    key_map = {
        "title":    lambda n: n.data.title.lower(),
        "artist":   lambda n: n.data.artist.lower(),
        "duration": lambda n: n.data.duration,
        "year":     lambda n: n.data.year,
    }
    key_func = key_map.get(sort_key, key_map["title"])

    if dll.head is None or dll.head.next is None:
        return {"algorithm": "merge", "time_ms": 0.0, "count": len(dll)}

    thoi_gian_bat_dau = time.perf_counter()

    new_head = merge_sort(dll.head, key_func)
    
    dll.head = new_head
    current = new_head
    count = 0
    while current is not None:
        count += 1
        if current.next is None:
            dll.tail = current
        current = current.next

    thoi_gian_ket_thuc = time.perf_counter()
    
    return {
        "algorithm": "merge",
        "time_ms":   round((thoi_gian_ket_thuc - thoi_gian_bat_dau) * 1000, 4),
        "count":     count,
    }
