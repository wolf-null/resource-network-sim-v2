from lib.NewtorkBuilder import NetworkBuilder
from random import choice, randint
from lib.Node import Node
from lib.Host import Host
from math import ceil


class SameSegments(NetworkBuilder):
    def __init__(self, previous=None, segment_variable='color', n_segments=2, random_order=True):
        super(SameSegments, self).__init__(previous)
        self._segment_variable = segment_variable
        self._n_segments = n_segments
        self._random_ord = random_order

    def building_operations(self, n=0):
        print('[SameSegments]: Begin')

        available_nodes = list(range(self._host.size))
        for k in range(self._host.size):
            if self._random_ord:
                idx = available_nodes.pop(randint(0, len(available_nodes)-1))
            else:
                idx = k
            self._host.get_node(idx).set(self._segment_variable, ceil((k+1)/(self._host.size / self._n_segments)) )

        print('[SameSegments]: End')







