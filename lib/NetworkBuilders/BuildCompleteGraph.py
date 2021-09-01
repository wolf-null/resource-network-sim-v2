from lib.NewtorkBuilder import NetworkBuilder
from lib.Node import Node
from lib.Host import Host


class BuildCompleteGraph(NetworkBuilder):
    """
    def build(self, n=0):
        super(BuildCompleteGraph, self).build(n)
    """

    def __init__(self, previous=None):
        super(BuildCompleteGraph, self).__init__(previous)

    def building_operations(self, n=0):
        # self._host = super(BuildCompleteGraph, self).build(n)
        nodes = [Node() for node in range(n)]
        self._host.add_nodes(nodes)
        links = [[a,b] for a in range(n) for b in range(n) if a < b]
        self._host.connect_both_ways_n(links)


