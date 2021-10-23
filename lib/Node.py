from typing import Any, Dict, AnyStr
from lib.Signals import Signal


class Node:
    def __init__(self, index=-1, **kwargs):
        self.index = index
        self.__connections = list()
        self.__reverse_connections = list()
        self.input_buffer = list()

        # All **kwagrs will be interpreted as the initial state
        self._state = kwargs  # type: Dict[AnyStr, Any]

        self._host = None

        self.iteration = 0

    def get(self, key, default_value=None):
        """
        :return: the value associated with :param key: if it exists, in other case returns :param default_value:
        The latter ability allows to use get as
        """
        if key in self._state:
            return self._state[key]
        return default_value

    def set(self, key, value):
        self._state[key] = value

    def append(self, key, value):
        self._state[key].append(value)

    def apply(self, func):
        return func(self._state)

    def apply_get_set(self, func):
        return func(lambda var, dfv: self.get(var, dfv), lambda var, val: self.set(var, val))

    def __contains__(self, item):
        return item in self._state

    def copy(self, dst=None):
        # TODO: Such a behavior below might be counterintuitive. Refactor?
        if dst is None:
            result = (type(self))(self.index)
        else:
            result = dst
        result.__connections = self.__connections.copy()
        result.__reverse_connections = self.__reverse_connections.copy()
        result.input_buffer = self.input_buffer.copy()
        result._state = self._state.copy()
        result.index = self.index
        return result

    def set_host(self, host=None):
        self._host = host

    def connections(self):
        return self.__connections

    def reverse_connections(self):
        return self.__reverse_connections

    def get_connections(self):
        return self.__connections.copy(), self.__reverse_connections.copy()

    def set_connections(self, connections, rev_connections):
        self.__connections = connections
        self.__reverse_connections = rev_connections

    def connection_count(self):
        return len(self.__connections), len(self.__reverse_connections)

    def connect_to_node(self, node):
        if node.index in self.__connections:
            return False
        self.__connections.append(node.index)
        node.__reverse_connections.append(self.index)
        return True

    def disconnect_from_node(self, node):
        if node not in self.__connections:
            return False
        self.__connections.remove(node)
        node.__reverse_connections.remove(self.index)
        return True

    def connect_to(self, node_index):
        """
        Integrity-unsafe operation
        """
        if node_index in self.__connections:
            return False
        self.__connections.append(node_index)
        return True

    def disconnect_from(self, node_index):
        """
        Integrity-unsafe operation
        """
        if node_index not in self.__connections:
            return False
        self.__connections.remove(node_index)
        return True

    def reverse_connect_to(self, node_index):
        """
        Integrity-unsafe operation
        """
        if node_index in self.__reverse_connections:
            return False
        self.__reverse_connections.append(node_index)
        return True

    def reverse_disconnect_from(self, node_index):
        """
        Integrity-unsafe operation
        """
        if node_index not in self.__reverse_connections:
            return False
        self.__reverse_connections.remove(node_index)
        return True

    def push_signal(self, src, dst, amount):
        """
        :param src: sender of wealth
        :param dst: in simple cases node is receiving only the wealth send directly to it, but there are cases
        :param amount: amount of wealth sent
        :return: True if success or False if blocked. The way of calling this function is:

        while not node.push_signal(...):
            pass
        """
        self.input_buffer.append((src, dst, amount))
        return True

    def pop_signals(self, number_or_records=-1):
        if number_or_records != -1:
            result = self.input_buffer[0:number_or_records]
        else:
            result = self.input_buffer.copy()
        self.input_buffer = self.input_buffer[number_or_records:-1]
        return result

    def send_signal(self, dst, amount):
        self._host.send_signal_to(self, dst, amount)

    def exec(self):
        """
        The way of cleaning input stack is also determined by inheritors
        Use pop_signals when exec() starts and
        """
        pass

    def print(self, *args):
        print("<{0}> [{1}|{2}]:".format(self.iteration, type(self).__name__, self.index), *args)


    def emit(self, signal=Signal()):
        self.input_buffer.append(signal)

    def emit_to_host(self, signal=Signal()):
        if self._host is not None:
            self._host.emit(signal)