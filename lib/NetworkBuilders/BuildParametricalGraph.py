from lib.NewtorkBuilder import NetworkBuilder
from lib.Node import Node
from lib.Host import Host
from lib.Host import dict_sum, dict_by_number, dict_add_number
import random as rnd


class BuildParametricalGraph(NetworkBuilder):
    """
    The logis is as follows:
        1. Collect current network statistics
        2. Randomly determine which size of node is more required to be added. Let it be m (or belong to m-class).
        3. This new node will be connected to m other nodes.
            This means that these nodes will move from k-class to k'-class each node it will be connected to
    """

    """
    Another version of the algorithm:
        1. Each node added to the network has initial amount of links (=1).
        2. This node is randomly connected to another node in m-class where m is so to improve difference
            between stats and stat-parameter.
    """
    def __init__(self, previous=None):
        super(BuildParametricalGraph, self).__init__(previous)


    def building_operations(self, n=0):
        pass
