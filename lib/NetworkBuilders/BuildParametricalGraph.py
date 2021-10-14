import math
from abc import abstractmethod

from lib.NewtorkBuilder import NetworkBuilder
from lib.Node import Node
from lib.Bus import Bus
import random as rnd
from lib.Errors import GeneralError_WrongInput, HostError_CompletenessViolated, GeneralError_NotCallable
import random as rnd


class NetworkConsistency:
    """Class which allows to init network with different types (subclasses) of <Node> class"""

    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def pick_a_node(self, **kwargs):
        pass


class DefaultNetworkConsistency(NetworkConsistency):
    def __init__(self, **kwargs):
        super(DefaultNetworkConsistency, self).__init__(**kwargs)

    def pick_a_node(self, **kwargs):
        return Node()


class RandomNetworkConsistency(NetworkConsistency):
    def __init__(self, distribution=dict(), node_initializer=dict(), **kwargs):
        """
        :param distribution:        dict {Node or subclass : weight}
                                    - Caution: pass subclasses without braces, e.g. RandomNetworkConsistency({Node:10, BigNode:1})

        :param node_initializer:    dict {Node or subclass : initfunc(node_type as <Node subclass>, n as <integer>) }
                                    - initfunc() returns arguments **kwargs for a particular Subclass of Node root class,
                                    which is put into it's __init__(...) as the arguments.

                                    initfunc() shall return a dict of **kwargs in form {argument:value}

                                    This is a pretty insecure but also a very flexible code maneuver.
                                    Use with caution.

        """
        super(RandomNetworkConsistency, self).__init__(**kwargs)
        self._distribution = distribution
        self._initializer = node_initializer
        self._picked_nodes = dict()
        for key in list(distribution.keys()):
            self._picked_nodes[key] = 0

    def pick_a_node(self, **kwargs):
        chosen_node_type = rnd.choices(
            list(self._distribution.keys()),
            weights=list(self._distribution.values()),
            k=1
        )

        self._picked_nodes[chosen_node_type] += 1

        if chosen_node_type in self._initializer:
            if callable(self._initializer[chosen_node_type]):
                # Attention: Satanic code!
                return chosen_node_type(**self._initializer[chosen_node_type](n=self._picked_nodes[chosen_node_type]-1, node_type=chosen_node_type, order=kwargs['order'] if 'order' in kwargs else None))
            else:
                raise GeneralError_NotCallable(str("Given initializer {0} isn't a callable object! Initializer with key of <Node> type shall be a function with arguments <n> and [<node_type>]").format(self._initializer[chosen_node_type]))
        else:
            return chosen_node_type()


class BuildParametricalGraph(NetworkBuilder):
    """
        Generates network with amount_of_nodes with defined interconnection_structure,
        where not more than goal_error nodes are out of the structure (see below)
        If goal_error is unspecified it is set to 0

        interconnection_structure have form of a dict: {link_amount:prob, link_amount:prob, ...},
        where link_amount is a number of connection and prob is the probability of it's emerging in the net

        After the generation phase (encapsulated for user, but may long for indefinite time - not solved yet),
        The algorithm checks total_error = |k'th_node_connections - k'th_node_expected_connections| and if
        total_error <= goal_error it stops the generation process
        and passes back to build() procedure (returns the net)
    """

    def __init__(self, previous=None, structure=dict(), goal_error=0, consistency=DefaultNetworkConsistency()):
        super(BuildParametricalGraph, self).__init__(previous)

        # Init
        self._structure = structure
        self._saturation = list()
        self._desaturation = list()
        self._actual = list()
        self._n = 0
        self._consistency = consistency

        # Process inputs
        self._norm_structure = structure.copy()
        self._goal_error = goal_error
        if not isinstance(structure, dict):
            raise GeneralError_WrongInput("building_operations shall receive (node_amount, {link_amount:quantity, ...})")

    def _pre_building(self):
        """Attention: bad code"""
        while True:
            self._host.add_nodes([self._consistency.pick_a_node(order=self._saturation[k]) for k in range(self._n)])
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

    def building_operations(self, n=0):
        """
        :param n: - the structure of the network. See BuildParametricalGraph class desc.
        """
        rcr = self._host.is_rising_connection_errors()
        self._host.set_is_rising_connection_errors(False)

        # Process inputs
        self._n = n

        for key in self._norm_structure:
            self._norm_structure[key] = int(self._norm_structure[key] * self._n)
        rounding_error = max(0, self._n - int(sum(self._norm_structure.values())))
        for k in range(rounding_error):
            keys = list(self._norm_structure.keys())
            self._norm_structure[rnd.choice(keys)] += 1
        self._structure = self._norm_structure

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

