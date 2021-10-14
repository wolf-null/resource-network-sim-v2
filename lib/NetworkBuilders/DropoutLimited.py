from lib.NewtorkBuilder import NetworkBuilder
from lib.Node import Node
from lib.Host import Host
from random import choice
from random import shuffle


class DropoutLimited(NetworkBuilder):
    """
    Brakes random connections so not to allow the fraction:
    <node's_final_connection_count> / <node's_initial_connection_count>
    for every node to go lower than <dropout> threshold value

    Recommended to use if one wants to lower connection amount without serious alteration of the network structure

    TODO: Optimize the code, bitch!
    """

    def __init__(self, previous=None, dropout=0.5):
        super(DropoutLimited, self).__init__(previous)
        self._dropout = dropout

    def building_operations(self, n=0):
        print('[DropoutLimited]: Start')
        initial_link_amounts = [self._host.get_node(k).connection_count()[0] for k in range(self._host.size)]
        forbidden = list()  # List of connection breaking of which violates network's connectivity (completeness)
        finalized_nodes = list()  # List of nodes as dropouted as possible
        links_dropped = 0  # Just an encounter for debug and entertainment statistics ;)

        while True:
            allowed_for_dropout = list(filter(lambda k: (self._host.get_node(k).connection_count()[0] - 1) / initial_link_amounts[k] > self._dropout, range(self._host.size)))
            allowed_for_dropout = list(filter(lambda disconnect_candidate: disconnect_candidate not in finalized_nodes, allowed_for_dropout))
            if len(allowed_for_dropout) < 2:
                # Finish if no links to break
                break

            # Traverse all nodes allowed for dropout in a random order (to prevent 'structural biases')
            shuffle(allowed_for_dropout)
            for node in allowed_for_dropout:
                p = (self._host.get_node(node).connection_count()[0] - 1) / initial_link_amounts[node]
                if p < self._dropout:
                    finalized_nodes += [node, ]
                    continue

                allowed_disconnects = list(filter(lambda k: (self._host.get_node(k).connection_count()[0] - 1) / initial_link_amounts[k], self._host.get_node(node).connections()))
                allowed_disconnects = list(filter(lambda disconnect_candidate: sorted([disconnect_candidate, node]) not in forbidden, allowed_disconnects))
                allowed_disconnects = list(filter(lambda disconnect_candidate: disconnect_candidate not in finalized_nodes, allowed_disconnects))

                if len(allowed_disconnects) == 0:
                    finalized_nodes += [node, ]
                    continue

                disconnect_from = choice(allowed_disconnects)
                self._host.disconnect_both_ways(node, disconnect_from)
                if not self._host.check_connectivity():
                    forbidden += [sorted([node, disconnect_from]), ]
                    self._host.connect_both_ways(node, disconnect_from)
                links_dropped += 1

        print(str("\r[DropoutLimited]: {0} links dropped, which is {1}% of initial value. The goal was {2}%").format(
            links_dropped,
            round(100*2*links_dropped/sum(initial_link_amounts),3),
            round(100 * (1-self._dropout), 3)
        ), end='')

