from lib.Node import Node
from lib.Signals import SignalSet, SignalAppend, Signal
from lib.Errors import HostError_NotSupported


class CommittedNode(Node):
    """
    Provides specific functionality for the node committed to the bus
    """

    def __init__(self, **kwargs):
        super(CommittedNode, self).__init__(**kwargs)

    def set(self, key, value, mirror=True):
        super(CommittedNode, self).set(key, value)
        if mirror:
            self.emit_to_host(SignalSet(self.index, self.index, key=key, value=value))

    def append(self, key, value, mirror=True):
        super(CommittedNode, self).append(key, value)
        if mirror:
            self.emit_to_host(SignalAppend(self.index, self.index, key=key, value=value))

    def connect_to_node(self, node):
        raise HostError_NotSupported('connect_to_node(<node>) {0} is not supported by GhostNodes.'
                                     'Use connect_to(<node_index>) instead'.format(node))

    def disconnect_from_node(self, node):
        raise HostError_NotSupported('disconnect_from_node(<node>) {0} is not supported by GhostNodes.'
                                     'Use disconnect_from(<node_index>) instead'.format(node))



    # TODO: Decorate all connection/disconnection routines with connection messages back to host
