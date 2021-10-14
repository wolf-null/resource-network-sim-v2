#import threading


class Node:
    def __init__(self, index=-1, initial_wealth=0, **kwargs):
        self.index = index
        self.__connections = list()
        self.__reverse_connections = list()
        self.my_input_buffer = list()
        self._data = {'wealth': initial_wealth}

        self._host = None
        self._data_write_stack = list()
        self._idle_mode = False

    def get(self, key, default_value=None):
        """
        :return: the value associated with :param key: if it exists, in other case returns :param default_value:
        The latter ability allows to use get as
        """
        if key in self._data:
            return self._data[key]
        return default_value

    def set(self, key, value):
        self._data[key] = value

    def append(self, key, value):
        self._data[key].append(value)

    def apply(self, func):
        return func(self._data)

    def apply_get_set(self, func):
        return func(lambda var, dfv: self.get(var, dfv), lambda var, val: self.set(var, val))

    def __contains__(self, item):
        return item in self._data

    def copy(self, dst=None):
        # TODO: Such a behavior below might be counterintuitive. Refactor?
        if dst is None:
            result = (type(self))(self.index)
        else:
            result = dst
        result.__connections = self.__connections.copy()
        result.__reverse_connections = self.__reverse_connections.copy()
        result.my_input_buffer = self.my_input_buffer.copy()
        result._data = self._data.copy()
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
        self.my_input_buffer.append((src, dst, amount))
        return True

    def pop_signal_stack(self, number_or_records=-1):
        if number_or_records != -1:
            result = self.my_input_buffer[0:number_or_records]
        else:
            result = self.my_input_buffer.copy()
        self.my_input_buffer = self.my_input_buffer[number_or_records:-1]
        return result

    def send_signal(self, dst, amount):
        self._host.send_signal_to(self, dst, amount)

    def set_idle(self, state):
        self._idle_mode = state

    def is_idle(self):
        return self._idle_mode

    def exec(self):
        """
        The way of cleaning input stack is also determined by inheritors
        Use pop_signal_stack when exec() starts and
        """
        pass

    def post_exec(self):
        """
        Launched after the end of the stage
        """
        pass

