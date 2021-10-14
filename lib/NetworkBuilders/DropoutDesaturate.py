from lib.NewtorkBuilder import NetworkBuilder
from lib.Node import Node
from lib.Host import Host
from random import sample


class DropoutDesaturate(NetworkBuilder):
    def __init__(self, previous=None, dropout=0.5):
        super(DropoutDesaturate, self).__init__(previous)
        self._dropout = dropout

    def building_operations(self, n=0):
        rce = self._host.is_rising_connection_errors()
        self._host.set_is_rising_connection_errors(False)

        disconnections = list()

        for node_index in range(self._host.size):
            node = self._host.get_node(node_index)
            connections = node.connections()
            connections_to_delete = sample(connections, k=int(len(connections) * self._dropout))
            disconnections += [[node_index, node_b] for node_b in connections_to_delete]

        self._host.disconnect_n(disconnections)

        self._host.set_is_rising_connection_errors(rce)



