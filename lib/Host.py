from typing import List

from lib.Node import Node
from lib.Errors import *


def dict_sum(a=dict(), b=dict()):
    difference = dict()
    united_keys = list(set(a.keys()) | set(b.keys()))
    for key in united_keys:
        a_val = a[key] if key in a else 0
        b_val = b[key] if key in b else 0
        difference[key] = a_val + b_val
    return difference


def dict_by_number(a=dict(), number=int()):
    result = a.copy()
    for key in a.keys():
        result[key] *= number
    return result


def dict_add_number(a=dict(), number=int()):
    result = a.copy()
    for key in a.keys():
        result[key] += number
    return result

class Host:
    """
    Host class implements basic node management functions like adding, connecting, connectivity check
    Host class doesn't implement execution functions and other pipeline functional. For this see StageHost
    """
    class IgnoreNoValues:
        pass

    def __init__(self):
        self.size = 0
        self.__nodes = List[Node]
        self.__rising_connection_errors = True
        self.__global_data = list()

    def reset_nodes(self):
        self.size = 0
        self.__nodes.clear()

    def copy(self):
        result = Host()
        for node in self.__nodes:
            new_node = node.copy()
            new_node.set_host(result)
            result.__nodes.append(new_node)
        result.size += self.size
        return result

    def is__rising_connection_errors(self):
        return self.__rising_connection_errors

    def set_is__rising_connection_errors(self, enabled=False):
        self.__rising_connection_errors = enabled

    def get_node(self, index):
        return self.__nodes[index]

    def add_node(self, node):
        if not isinstance(node, Node):
            raise HostError_NotANode('Added node should be inherited from Node class (see Node.py)')
        node.index = len(self.__nodes)
        node.set_host(self)
        self.__nodes.append(node)
        self.size += 1
        return node.index

    def add_nodes(self, list_nodes):
        for node in list_nodes:
            self.add_node(node)

    def connect(self, src, dst):
        s2d = self.__nodes[src].connect_to(dst)
        d2s = self.__nodes[dst].reverse_connect_to(src)
        if self.__rising_connection_errors and not (s2d and d2s):
            raise HostError_Connection(str("{0} -> {1} are already connected.\nCheck: {2},{3}").format(src, dst, s2d, d2s))

    def connect_n(self, pairs):
        for src, dst in pairs:
            self.connect(src, dst)

    def connect_both_ways(self, node_a, node_b):
        asb = self.__nodes[node_a].connect_to(node_b)
        bra = self.__nodes[node_b].reverse_connect_to(node_a)
        bsa = self.__nodes[node_b].connect_to(node_a)
        arb = self.__nodes[node_a].reverse_connect_to(node_b)
        if not (asb and bra and bsa and arb):
            if self.__rising_connection_errors:
                raise HostError_Connection(str("{0} and {1} are already connected\nCheck: {2},{3},{4},{5}").format(node_a, node_b, asb, bra, bsa, arb))
            else:
                return False
        return True

    def connect_both_ways_n(self, pairs):
        for a, b in pairs:
            self.connect_both_ways(a, b)

    def disconnect(self, src, dst):
        s2d = self.__nodes[src].disconnect_from(dst)
        d2s = self.__nodes[dst].reverse_disconnect_from(src)
        if self.__rising_connection_errors and not (s2d and d2s):
            raise HostError_Connection(str("{0} -> {1} are not connected.\nCheck: {2},{3}").format(src, dst, s2d, d2s))

    def disconnect_n(self, pairs):
        for src, dst in pairs:
            self.disconnect(src, dst)

    def disconnect_both_ways(self, node_a, node_b):
        asb = self.__nodes[node_a].disconnect_from(node_b)
        bra = self.__nodes[node_b].reverse_disconnect_from(node_a)
        bsa = self.__nodes[node_b].disconnect_from(node_a)
        arb = self.__nodes[node_a].reverse_disconnect_from(node_b)
        if self.__rising_connection_errors and not (asb and bra and bsa and arb):
            raise HostError_Connection(str("{0} and {1} are not connected\nCheck: {2},{3},{4},{5}").format(node_a, node_b, asb, bra, bsa, arb))

    def disconnect_both_ways_n(self, pairs):
        for a, b in pairs:
            self.disconnect_both_ways(a, b)

    def check_connectivity(self):
        front = {0, }
        visited_nodes = set()
        while True:
            new_front = set()
            for node in front:
                new_front |= set(self.__nodes[node].connections()) | set(self.__nodes[node].reverse_connections())
            new_front -= visited_nodes
            visited_nodes |= front
            if len(new_front) == 0:
                if len(visited_nodes) < len(self.__nodes):
                    return False
                else:
                    return True
            front = new_front

    def print_data(self):
        for node in self.__nodes:
            print("Node: ", node.index, " :")
            print("Connections : ", node.connections())
            print("Rev. connections : ", node.reverse_connections())
            print()

    def graph_statistics_dict(self):
        stats = dict()
        for node_index in range(self.size):
            connections, rev_connections = self.__nodes[node_index].connection_count()
            if connections not in stats:
                stats[connections] = 0
            stats[connections] += 1
        return stats

    def graph_statistics_list(self):
        stats = [0 for k in range(self.size)]
        for node_index in range(self.size):
            connections, rev_connections = self.__nodes[node_index].connection_count()
            stats[connections] += 1
        return stats

    def save_structure(self):
        nodes = [node.index for node in self.__nodes]
        links = list()
        for src in self.__nodes:
            for dst in src.get_connections()[0]:
                links += [[src.index, dst], ]
        return nodes, links

    def load_structure(self, nodes, links):
        self.__nodes.clear()
        for node in nodes:
            new_node = Node()
            self.add_node(Node())
            new_node.index = node

        self.connect_n(links)
        self.size = len(nodes)

    def send_signal_to(self, src, dst, amount):
        self.__nodes[dst].push_signal(src, dst, amount)

    def filter_indexes(self, func, from_indexes=None):
        if from_indexes is None:
            from_indexes = range(self.size)
        return list(filter(lambda k: self.__nodes[k].check_condition(func), from_indexes))

    def filter(self, func, from_nodes=None):
        if from_nodes is None:
            from_nodes = self.__nodes
        return list(filter(lambda node: node.apply(func), from_nodes))

    def neighbors(self, indexes=list()):
        result = set()
        for k in indexes:
            result |= set().union(*self.__nodes[k].get_connections())
        result = list(result - set(indexes))
        return result

    def hist_values(self, key, from_indexes=None, default_value=IgnoreNoValues()):
        if from_indexes is None:
            from_indexes = range(self.size)
        result = dict()
        for k in from_indexes:
            val = self.__nodes[k].get(key, default_value)
            if isinstance(val, self.IgnoreNoValues):
                continue
            if val not in result:
                result[val] = 0
            result[val] += 1
        return result

    def apply(self, func):
        return [node.apply(func) for node in self.__nodes]

    def apply_get_set(self, func):
        return [node.apply_get_set(func) for node in self.__nodes]
