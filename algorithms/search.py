class Search:
    @staticmethod
    def is_empty(head):
        return head is None

    @staticmethod
    def search_by_title(head, keyword):
        result = []
        if Search.is_empty(head):
            return result
            
        keyword = keyword.strip().lower()
        current = head
        while current is not None:
            if keyword in current.data.title.lower():
                result.append(current) 
            current = current.next
        return result

    @staticmethod
    def search_by_artist(head, keyword):
        result = []
        if Search.is_empty(head):
            return result
            
        keyword = keyword.strip().lower()
        current = head
        while current is not None:
            if keyword in current.data.artist.lower():
                result.append(current)
            current = current.next
        return result

def linear_search(dll, keyword, field="title"):
    if field == "title":
        return Search.search_by_title(dll.head, keyword)
    elif field == "artist":
        return Search.search_by_artist(dll.head, keyword)
    else:
        return Search.search_by_title(dll.head, keyword)
