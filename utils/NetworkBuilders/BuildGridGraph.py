from utils.NewtorkBuilder import NetworkBuilder
from lib.Node import Node


class BuildGridGraph(NetworkBuilder):
    def __init__(self, previous=None, node_initializer=None):
        super(BuildGridGraph, self).__init__(previous)
        self._node_init = node_initializer

    def building_operations(self, n=0):
        print('[BuildGridGraph]: Begin')
        n_nodes = n ** 2
        nodes = [self._node_init() if callable(self._node_init) else Node() for node in range(n_nodes)]
        self._host.add_nodes(nodes)
        links = list()
        for k in range(n_nodes):
            if (k+1) % n != 0:
                links += [[k, k + 1]]
            if k // n != n - 1:
                links += [[k, k + n]]
        self._host.connect_both_ways_n(links)
        print('[BuildGridGraph]: End')


