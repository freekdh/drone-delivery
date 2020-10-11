class LinkedListNode:
    def __init__(self):
        self._next_node = None
        self._previous_node = None

    def get_next_node(self):
        if self._next_node:
            return self._next_node
        else:
            raise NoNextNodeError

    def get_previous_node(self):
        if self._previous_node:
            return self._previous_node
        else:
            raise NoPreviousNodeError

    def set_next_node(self, node):
        self._next_node = node

    def set_previous_node(self, node):
        self._previous_node = node


class HeadOfLinkedList:
    def __init__(self):
        self._next_node = None

    def get_next_node(self):
        if self._next_node:
            return self._next_node
        else:
            raise NoNextNodeError

    def set_next_node(self, node):
        self._next_node = node


class LinkedList:
    def __init__(self, head_of_linked_list=HeadOfLinkedList()):
        self._head_of_linked_list = head_of_linked_list

    def __iter__(self):
        class LinkedListIterator:
            def __init__(self, head=None):
                self.current = head

            def __iter__(self):
                return self

            def __next__(self):
                try:
                    self.current = self.current.get_next_node()
                    return self.current
                except NoNextNodeError:
                    raise StopIteration

        return LinkedListIterator(head=self._head_of_linked_list)

    def append(self, append_node):
        try:
            last_node = self._get_last_node()
        except EmptyListError:
            last_node = self._head_of_linked_list
        self._link_nodes(node1=last_node, node2=append_node)

    def pop(self):
        try:
            last_node = self._get_last_node()
            previous_node = last_node.get_previous_node()
            self._unlink_nodes(node1=previous_node, node2=last_node)
        except EmptyListError:
            raise EmptyListError

    def remove(self, node):
        raise NotImplementedError("work in progress")

        try:
            previous_node = node.get_previous_node()
            self._unlink_nodes(previous_node, node)
        except NoPreviousNodeError:
            pass

        try:
            next_node = node.get_next_node()
            self._unlink_nodes(node, next_node)
        except NoNextNodeError:
            pass

        self._link_nodes(previous_node, next_node)

    def _get_last_node(self):
        try:
            return list(self)[-1]
        except IndexError:
            raise EmptyListError

    def _link_nodes(self, node1, node2):
        try:
            node1.get_next_node()
            assert False
        except NoNextNodeError:
            node1.set_next_node(node2)

        try:
            node2.get_previous_node()
            assert False
        except NoPreviousNodeError:
            node2.set_previous_node(node1)

    def _unlink_nodes(self, node1, node2):
        assert node1.get_next_node() == node2
        assert node2.get_previous_node() == node1
        node1.set_next_node(None)
        node2.set_previous_node(None)


class EmptyListError(Exception):
    pass


class NoNextNodeError(Exception):
    pass


class NoPreviousNodeError(Exception):
    pass
