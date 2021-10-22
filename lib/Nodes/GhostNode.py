import time

from lib.Node import Node
from lib.Signals import SignalSet, SignalAppend, Signal
from lib.Errors import HostError_NotSupported


class GhostNode(Node):
    def __init__(self, **kwargs):
        super(GhostNode, self).__init__(**kwargs)

    def emit(self, signal=Signal()):
        # self.push_signal(signal.src, signal.dst, signal)
        self.my_input_buffer.append(signal)

    def pop_signal(self, number_of_records=-1):
        return self.pop_signal_stack(number_of_records)

    def emit_host(self, signal=Signal()):
        if self._host is not None:
            self._host.emit(signal)

    def set(self, key, value, mirror=True):
        super(GhostNode, self).set(key, value)
        if mirror:
            self.emit_host(SignalSet(self.index, self.index, key=key, value=value))

    def append(self, key, value, mirror=True):
        super(GhostNode, self).append(key, value)
        if mirror:
            self.emit_host(SignalAppend(self.index, self.index, key=key, value=value))

    def connect_to_node(self, node):
        raise HostError_NotSupported('connect_to_node(<node>) {0} is not supported by GhostNodes.'
                                     'Use connect_to(<node_index>) instead'.format(node))

    def disconnect_from_node(self, node):
        raise HostError_NotSupported('disconnect_from_node(<node>) {0} is not supported by GhostNodes.'
                                     'Use disconnect_from(<node_index>) instead'.format(node))

    def exec(self):
        self.print("[GhostNode|{0}]: exec()".format(self.index))

    # TODO: Decorate all connection/disconnection routines with connection messages back to host
