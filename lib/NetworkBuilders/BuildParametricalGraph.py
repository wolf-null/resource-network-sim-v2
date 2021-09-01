import math

from lib.NewtorkBuilder import NetworkBuilder
from lib.Node import Node
from lib.Host import Host
from lib.Host import dict_sum, dict_by_number, dict_add_number
import random as rnd
from lib.Errors import GeneralError_WrongInput, HostError_CompletenessViolated
import random as rnd


class BuildParametricalGraph(NetworkBuilder):
    """
        Generates network with <amount_of_nodes> with defined <interconnection_structure>,
        where not more than <goal_error> nodes are out of the structure (see below)
        If <goal_error> is unspecified it is set to 0

        <interconnection_structure> have form of a dict {link_amount:prob, link_amount:prob, ...},
        where <link_amount> is a number of connection and <prob> is the probability of it's emerging in the net

        After the generation phase (encapsulated for user, but may long for indefinite time - not solved yet),
        The algorithm checks total_error = |k'th_node_connections - k'th_node_expected_connections| and if
        total_error <= <goal_error> it stops the generation process
        and passes back to build() procedure (returns the net)
    """

    def __init__(self, previous=None):
        super(BuildParametricalGraph, self).__init__(previous)
        self._structure = dict()
        self._saturation = list()
        self._desaturation = list()
        self._actual = list()
        self._n = 0
        self._m = 0
        self._goal_error = 0

    def _pre_building(self):
        """Attention: bad code"""
        while True:
            self._host.add_nodes([Node() for k in range(self._n)])
            while True:
                changes_made = False
                desaturated = list(filter(lambda node: self._actual[node] < self._saturation[node], range(self._n)))
                if len(desaturated) == 0:
                    break
                for node in desaturated:
                    if node == 0:
                        continue
                    pickup_desaturated = list(filter(lambda k: self._actual[k] < self._saturation[k], range(node)))
                    if len(pickup_desaturated) == 0:
                        continue
                    pickup_node = rnd.choice(pickup_desaturated)  # rnd.randint(0,node-1)
                    if not self._host.connect_both_ways(node, pickup_node):
                        continue
                    self._actual[node] += 1
                    self._actual[pickup_node] += 1
                    changes_made = True
                if not changes_made:
                    break

            self._actual = [self._host.get_node(k).connection_count()[0] for k in range(self._n)]
            desat = sum([int(abs(self._actual[k] - self._saturation[k])) for k in range(self._n)])
            if desat <= self._goal_error:
                if self._host.check_connectivity():
                    return True

            print("desat={0} -> reset".format(desat))
            self._host.reset_nodes()

    def building_operations(self, n=tuple):
        """
        :param n: - the structure of the network. See BuildParametricalGraph class desc.
        """
        rcr = self._host.is_rising_connection_errors()
        self._host.set_is_rising_connection_errors(False)

        # Process inputs
        if not isinstance(n[1], dict):
            raise GeneralError_WrongInput("building_operations shall receive (node_amount, {link_amount:quantity, ...})")
        self._n = n[0]
        norm_structure = n[1].copy()
        for key in norm_structure:
            norm_structure[key] = int(norm_structure[key] * self._n)
        rounding_error = max(0, self._n - int(sum(norm_structure.values())))
        for k in range(rounding_error):
            keys = list(norm_structure.keys())
            norm_structure[rnd.choice(keys)] += 1
        self._structure = norm_structure

        if len(n) == 3:
            self._goal_error = n[2]
        else:
            self._goal_error = 0

        for sat in self._structure.keys():
            amount = self._structure[sat]
            self._saturation += [sat for k in range(amount)]
        self._saturation = sorted(self._saturation, reverse=True)
        self._actual = [0 for k in range(len(self._saturation))]

        # Start pre-building
        self._pre_building()

        self._host.set_is_rising_connection_errors(rcr)

        # Return back only the number of nodes:
        n = self._n

