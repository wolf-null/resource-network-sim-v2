from random import shuffle, randint
import time

from lib.Bus import Bus
from lib.Node import Node
from lib.Nodes.GhostNode import GhostNode
from lib.Errors import HostError_NoSuchNode
import multiprocessing
from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing.synchronize import Event
from multiprocessing.connection import PipeConnection
from lib.Signals import Signal, DataSignal, HostSignal, HostTerminate, SignalSet, SignalAppend, HostWait
from typing import Mapping, Any, Dict


class ProcessingBus(Bus):
    def __init__(self, host_bus: multiprocessing.connection = None, a_start_event: Event = None, a_end_event: Event = None, name : str = str()):
        super(ProcessingBus, self).__init__()
        self._bus = host_bus
        self._a_start_event = a_start_event
        self._a_finish_event = a_end_event
        self._alias = dict()  # type:  Dict[Any, GhostNode]
        self._process = None
        if len(name) == 0:
            name = str(randint(0, 65535))
        self.name = name
        self._put_on_termination = False
        self.iteration = 0
        self._local_buffer = None  # multiprocessing.Queue

    def print(self, *args):
        print(*args)

    def get_process(self):
        return self._process

    def set_process(self, process):
        self._process = process

    def update_alias(self):
        """
        Traverse own nodes and adds an index alias to those nodes
        Also seeks for node[alias] if set and adds these too
        :return:
        """
        for node in self._nodes:
            if node.index not in self._alias:
                self._alias[node.index] = node

                # If the node provide it's own pseudonymous it will be also added to alias list:
                if 'alias' in node:
                    aliases = node.get('pseudonymous')
                    for alias in aliases:
                        self._alias[alias] = node
        self.print('[ProcessingBus|{0}]: Alias {1}'.format(self.name, self._alias))

    def belongs_here(self, index):
        return index in self._alias

    def process_data_signal(self, signal):
        """Update Node's states (receive set, append, set_last)"""
        if isinstance(signal, SignalSet):
            self._alias[signal.dst].set(signal.key(), signal.value(), mirror=False)
        elif isinstance(signal, SignalAppend):
            self._alias[signal.dst].append(signal.key(), signal.value(), mirror=False)
        else:
            self.print("#{2} [ProcessingBus|{0}]: No data instructions for signal {1}".format(self.name, type(signal), self.iteration))

    def process_host_signal(self, signal):
        """Signals for managing processing host itself"""
        if isinstance(signal, HostTerminate):
            # Terminate signal
            self.print(str("[ProcessingBus|{0}]: Terminating...").format(self.name))
            self._process.terminate()  # TODO: Shall be add at process creation by the Master host
            self._put_on_termination = True
        elif isinstance(signal, HostWait):
            time.sleep(signal.time())
        else:
            self.print("#{2} [ProcessingBus|{0}]: No host instructions for signal {1}".format(self.name, type(signal), self.iteration))

    def distribute_inputs(self):
        while not self._local_buffer.empty():
            signal = self._local_buffer.get()
            dst = signal.dst
            self._alias[dst].emit(signal)

        while self._bus.poll():
            signal = self._bus.recv()
            if isinstance(signal, DataSignal):      # Data-signals
                dst = signal.dst
                if self.belongs_here(dst):
                    self.process_data_signal(signal)
                else:
                    raise HostError_NoSuchNode('The node {0} is not here!'.format(dst))
            elif isinstance(signal, HostSignal):    # Bus-control signals
                self.process_host_signal(signal)
            else:                                   # To-node signals
                dst = signal.dst
                if self.belongs_here(dst):
                    self._alias[dst].emit(signal)  # Push signal to node's input stack. Processed by exec() at call
                else:
                    raise HostError_NoSuchNode('The node {0} is not here!'.format(dst))

    def exec(self):
        self.print("#{1} [ProcessingBus|{0}]: Wait for A-phase".format(self.name, self.iteration))
        self._a_start_event.wait()
        self._a_start_event.clear()
        self.print("#{1} [ProcessingBus|{0}]: A-phase started".format(self.name, self.iteration))
        self.distribute_inputs()
        exec_order = list(range(len(self._nodes))) # [node.index for node in self._nodes]
        shuffle(exec_order)
        for node_index in exec_order:   # TODO: Shuffling exec() order
            self.get_node(node_index).exec()
        self._a_finish_event.set()
        self.print("#{1} [ProcessingBus|{0}]: A-phase end".format(self.name, self.iteration))
        self.iteration += 1
        # MAN: Nodes pushes signals directly to the bus via Node._host.emit()
        # MAN: ... The node is linked to the host via Node._host
        # MAN: ... which is set in Bus.add_node(Node)
        # MAN: ... This is why there is no special code for collecting signals from nodes.

    def emit(self, signal: Signal):
        if not self.belongs_here(signal.dst) or isinstance(signal, DataSignal):
            self.print("#{0} [ProcessingBus|{1}]: Emit signal {2} to master host".format(self.iteration, self.name, signal))
            self._bus.send(signal)
        elif self.belongs_here(signal.dst):
            self._local_buffer.put(signal)
        # If not - it will be read at next distribute_inputs()

    def run(self, bus, stev, finev):
        self.print("[ProcessingBus|{0}]: Run the process".format(self.name))
        self._local_buffer = Queue()
        self._a_start_event = stev
        self._a_finish_event = finev
        self._bus = bus
        while not self._put_on_termination:
            self.exec()


