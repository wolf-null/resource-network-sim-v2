from lib.NewtorkBuilder import NetworkBuilder
from lib.Node import Node
from lib.Host import Host
from random import choice
from random import shuffle


class DropoutLimited(NetworkBuilder):
    """
    Brakes random connections so not to allow the fraction:
    <node's_final_connection_count> / <node's_initial_connection_count>
    for every node to go lower than <dropout> value
    """
    def __init__(self, previous=None, dropout=0.5):
        super(DropoutLimited, self).__init__(previous)
        self._dropout = dropout

    def building_operations(self, n=0):
        """
        :param p: - minimum allowed fraction of 'survived' connections
        :return:
        """
        rce = self._host.is_rising_connection_errors()
        self._host.set_is_rising_connection_errors(False)

        initial_link_amounts = [self._host.get_node(k).connection_count()[0] for k in range(self._host.size)]
        forbidden = list()
        links_droped = 0

        while True:
            allowed_for_dropout = list(filter(lambda k: (self._host.get_node(k).connection_count()[0] - 1) / initial_link_amounts[k] > self._dropout, range(self._host.size)))
            if len(allowed_for_dropout) < 2:
                break
            shuffle(allowed_for_dropout)
            for node in allowed_for_dropout:
                p = (self._host.get_node(node).connection_count()[0] - 1) / initial_link_amounts[node]
                if p < self._dropout:
                    continue
                allowed_disconnects = list(filter(lambda k: (self._host.get_node(k).connection_count()[0] - 1) / initial_link_amounts[k], self._host.get_node(node).connections()))
                allowed_disconnects = list(filter(lambda disconnect_candidate: sorted([disconnect_candidate, node]) not in forbidden, allowed_disconnects))
                if len(allowed_disconnects) == 0:
                    continue
                disconnect_from = choice(allowed_disconnects)
                self._host.disconnect_both_ways(node, disconnect_from)
                if not self._host.check_connectivity():
                    forbidden += sorted([node, disconnect_from])
                    self._host.connect_both_ways(node, disconnect_from)
                links_droped += 1

        self._host.set_is_rising_connection_errors(rce)



