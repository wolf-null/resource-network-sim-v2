from lib.Node import Node
from lib.Errors import *


class Host:
    def __init__(self):
        self.size = 0
        self._nodes = list()
        self._rack = list()
        self._enable_connection_errors = True

    def add_node(self, node):

        if not isinstance(node, Node):
            raise HostError_NotANode('Added node should be inherited from Node class (see Node.py)')
        node.index = len(self._nodes)
        self._nodes.append(node)
        return node.index

    def add_nodes(self, list_nodes):
        for node in list_nodes:
            self.add_node(node)

    def connect(self, src, dst):
        s2d = self._nodes[src].connect_to(dst)
        d2s = self._nodes[dst].reverse_connect_to(src)
        if self._enable_connection_errors and not (s2d and d2s):
            raise HostError_Connection(str("{0} -> {1} are already connected.\nCheck: {2},{3}").format(src, dst, s2d, d2s))

    def connect_n(self, pairs):
        for src, dst in pairs:
            self.connect(src, dst)

    def connect_both_ways(self, node_a, node_b):
        asb = self._nodes[node_a].connect_to(node_b)
        bra = self._nodes[node_b].reverse_connect_to(node_a)
        bsa = self._nodes[node_b].connect_to(node_a)
        arb = self._nodes[node_a].reverse_connect_to(node_b)
        if self._enable_connection_errors and not (asb and bra and bsa and arb):
            raise HostError_Connection(str("{0} and {1} are already connected\nCheck: {2},{3},{4},{5}").format(node_a, node_b, asb, bra, bsa, arb))

    def connect_both_ways_n(self, pairs):
        for a, b in pairs:
            self.connect_both_ways(a, b)

    def disconnect(self, src, dst):
        s2d = self._nodes[src].disconnect_from(dst)
        d2s = self._nodes[dst].reverse_disconnect_from(src)
        if self._enable_connection_errors and not (s2d and d2s):
            raise HostError_Connection(str("{0} -> {1} are not connected.\nCheck: {2},{3}").format(src, dst, s2d, d2s))

    def disconnect_both_ways(self, node_a, node_b):
        asb = self._nodes[node_a].disconnect_from(node_b)
        bra = self._nodes[node_b].reverse_disconnect_from(node_a)
        bsa = self._nodes[node_b].disconnect_from(node_a)
        arb = self._nodes[node_a].reverse_disconnect_from(node_b)
        if self._enable_connection_errors and not (asb and bra and bsa and arb):
            raise HostError_Connection(str("{0} and {1} are not connected\nCheck: {2},{3},{4},{5}").format(node_a, node_b, asb, bra, bsa, arb))

    def check_connectivity(self):
        front = {0, }
        visited_nodes = set()
        while True:
            new_front = set()
            for node in front:
                new_front |= set(self._nodes[node].connections()) | set(self._nodes[node].reverse_connections())
            new_front -= visited_nodes
            visited_nodes |= front
            if len(new_front) == 0:
                if len(visited_nodes) < len(self._nodes):
                    return False
                else:
                    return True
            front = new_front

