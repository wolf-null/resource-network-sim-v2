from lib.NewtorkBuilder import NetworkBuilder
from lib.Node import Node
from lib.Host import Host
from lib.Host import dict_sum, dict_by_number, dict_add_number
import random as rnd
from lib.Errors import GeneralError_WrongInput, HostError_CompletenessViolated
import random as rnd


class BuildParametricalGraph(NetworkBuilder):
    def __init__(self, previous=None):
        super(BuildParametricalGraph, self).__init__(previous)
        self._structure = dict()
        self._saturation = list()
        self._desaturation = list()
        self._actual = list()
        self._n = 0
        self._m = 0
        self._goal_error = 1

    def pre_buiilding(self):
        """Attention: govnocode"""
        self._host.add_nodes([Node() for k in range(self._n)])
        for k in range(self._n):
            # Retrieve allowed nodes to connect

            allowed_nodes = list(range(k+1, self._n))

            mandatory_node = list()
            if k > 0:
                mandatory_node_pre = list(range(k))
                rnd.shuffle(mandatory_node_pre)
                for node in mandatory_node_pre:
                    if self._host.get_node(node).connection_count()[0] + 1 <= self._saturation[node]:
                        mandatory_node += [node, ]
                        self._host.connect_both_ways(k, node)
                        # allowed_nodes.remove(node)
                        break

            already_connected = self._host.get_node(k).connection_count()[0]
            # We should try not to "finish" node as soon as possible.
            # At first, we shall throw out all already saturated nodes:
            for node in allowed_nodes:
                if self._host.get_node(node).connection_count()[0] + 1 > self._saturation[node]:
                    allowed_nodes.remove(node)

            # Then one shall find entirely desaturated nodes from the allowed ones:
            allowed_node_ranks = [(node, self._saturation[node] - self._host.get_node(node).connection_count()[0]) for node in allowed_nodes]
            allowed_node_ranks = sorted(allowed_node_ranks, key=lambda q: q[1], reverse=False)
            allowed_nodes = list(map(lambda q: q[0], allowed_node_ranks))

            # And take the very desaturated ones:

            connected_nodes = allowed_nodes[0:max(0, self._saturation[k] - already_connected)]

            for connect_to in connected_nodes:
                if self._host.get_node(connect_to).connection_count()[0] + 1 <= self._saturation[connect_to]:
                    self._host.connect_both_ways(k, connect_to)

            """connected_nodes = rnd.sample(allowed_nodes, k=max(0, min(self._saturation[k] - already_connected,len(allowed_nodes)) ))
            for connect_to in connected_nodes:
                if self._host.get_node(connect_to).connection_count()[0] + 1 <= self._saturation[connect_to]:
                    self._host.connect_both_ways(k, connect_to)
            """

        if not self._host.check_connectivity():
            print(self._host.print_data())
            raise HostError_CompletenessViolated(self._host.graph_statistics_dict())

    def resaturate(self):
        # desaturation = actual link amount - saturation
        self._actual = self._host.graph_statistics_list()
        self._desaturation = [(k, self._actual[k] - self._saturation[k]) for k in range(self._n)]
        if sum(map(lambda q: abs[q[1]], self._desaturation)) <= self._goal_error:
            return True

        sorted(self._desaturation, key=lambda v: v[1], reverse=True)
        print(self._desaturation)
        print()
        # Now all oversaturated nodes are on the top of the list.

        # Take the first one. And take out it's neighbor (which is to be disconnected)
        oversat = self._desaturation[0][0]
        oversat_neighbors = self._host.get_node(oversat).get_connections()
        oversat_neighbors.remove(oversat)
        neighbor_to_disconnect = rnd.choice(oversat_neighbors)

        # Now let's find a node no connect to
        neighbors_to_connect = self._desaturation[rnd.randint(len(self._desaturation)//2, len((self._desaturation))-1)][0]
        neighbors_to_connect.remove(neighbor_to_disconnect)
        neighbor_to_connect = rnd.choice(neighbors_to_connect)

        # Now finalize the job
        print(str("Switch {0} from {1} to {2}").format(neighbor_to_disconnect, oversat, neighbor_to_connect))
        self._host.disconnect_both_ways(oversat, neighbor_to_disconnect)
        self._host.connect_both_ways(neighbor_to_disconnect, neighbor_to_connect)

        if not self._host.check_connectivity():
            raise HostError_CompletenessViolated()

        return False

    def building_operations(self, n=tuple):
        # Input: amount of nodes + link structure [{link_amount : quantity, ...} like (nodes, {...})
        rcr = self._host.is_rising_connection_errors()
        self._host.set_is_rising_connection_errors(False)

        if not isinstance(n[1], dict):
            raise GeneralError_WrongInput("building_operations shall receive (node_amount, {link_amount:quantity, ...})")
        self._n = n[0]
        self._structure = n[1]
        for sat in self._structure.keys():
            amount = self._structure[sat]
            self._saturation += [sat for k in range(amount)]
        self._saturation = sorted(self._saturation, reverse=True)

        # self._saturation = list(zip(range(1, len(n[1])+1), list(self._structure.values())))
        # self._saturation = sorted(self._saturation, reverse=True, key=lambda q: q[1])
        # self._sat_order = list(map(lambda q: q[0], self._saturation))
        # self._saturation = list(map(lambda q: q[1], self._saturation))
        # sorted(self._saturation, reverse=True)

        self._m = sum(self._saturation) // 2 # Number of links
        self.pre_buiilding()
        self._host.print_data()
        print(self._host.graph_statistics_dict())
        exit(0)
        while not self.resaturate():
            pass

        self._host.set_is_rising_connection_errors(rcr)

