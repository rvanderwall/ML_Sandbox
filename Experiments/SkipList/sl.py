import timeit
import random


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.down = None

    def clone(self):
        c = Node(self.key, self.value)
        c.next = self.next
        c.down = self.down
        return c


class SkipList:
    def __init__(self, depth):
        self.head = []
        self.depth = depth
        self.top_layer = depth - 1
        self.bottom_layer = 0
        for d in range(depth):
            self.head.append(Node(None, None))
            if d > 0:
                self.head[d].down = self.head[d-1]

        self.beta = 0.1
        self.min = 99999999999
        self.max = 0

    def insert(self, key, value):
        if key < self.min:
            self.min = key
        if key > self.max:
            self.max = key
        item = Node(key, value)

        if self.head[self.top_layer].next is None:
            self.__link_first_item(self.top_layer, item)
            return

        node_list = []
        _, found = self.__find_node(node_list, self.head[self.top_layer], item.key)
        if found:
            print(f"Node with this key {key} already inserted")
            return

        # Insert at bottom layer
        assert len(node_list) == self.depth
        n = node_list[-1]
        item.next = n.next
        n.next = item

        for level in range(self.depth - 2, -1, -1):
            n = node_list[level]
            add_to_next_level = random.random()
            if add_to_next_level > 1 - self.beta:
                item1 = item.clone()
                item1.down = item
                item1.next = n.next
                n.next = item1
                item = item1
            else:
                break

    def __link_first_item(self, cur_layer, item_to_link):
        item_to_link.next = None
        self.head[cur_layer].next = item_to_link

        if self.head[cur_layer].down is None:
            return
        else:
            lower_item = item_to_link.clone()
            item_to_link.down = lower_item
            return self.__link_first_item(cur_layer - 1, lower_item)

    @staticmethod
    def __find_node_in_list(head: Node, key) -> (bool, Node):
        cur_node = head
        while cur_node.next:
            prev_node = cur_node
            cur_node = cur_node.next
            if cur_node.key > key:
                return False, prev_node    # We passed it
            if cur_node.key == key:
                return True, cur_node      # We found it
        return False, cur_node             # We passed it

    def __find_node(self, cur_list, head: Node, key) -> (bool, Node):
        found, node = self.__find_node_in_list(head, key)
        if found:
            cur_list.append(node)
            # Make sure to return the node from the lowest layer
            while node.down:
                node = node.down
                cur_list.append(node)
            return True, node
        else:
            cur_list.append(node)
            if node.down:
                return self.__find_node(cur_list, node.down, key)
            else:
                return False, None

    def find(self, key):
        found, node = self.__find_node([], self.head[self.top_layer], key)
        return found, node.value if node else None

    def find_print(self, key):
        f, v = self.find(key)
        # print(f"Found ({f}) for key {key} with value '{v}'")

    def find_first(self):
        self.find_print(self.min)

    def find_mid(self):
        self.find_print((self.min + self.max) // 2)

    def find_last(self):
        self.find_print(self.max)


def build_list():
    sl = SkipList(7)
    for i in range(1_000_000):
        key = i
        val = f"Value for key {i}"
        sl.insert(key, val)
    return sl


def main():
    print("SkipList")
    sl = build_list()
    tt = timeit.timeit(build_list, number=1)
    print(f"Time to build list: {tt}")

    tt = timeit.timeit(sl.find_first, number=100)
    print(f"Time to find first value: {tt}")

    tt = timeit.timeit(sl.find_mid, number=100)
    print(f"Time to find midrange value: {tt}")

    tt = timeit.timeit(sl.find_last, number=100)
    print(f"Time to find last value: {tt}")


if __name__ == "__main__":
    main()