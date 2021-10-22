import random
import time

from lib.Bus import Bus
from lib.Node import Node
from lib.Nodes.GhostNode import GhostNode
from lib.Errors import HostError_NoSuchNode
import multiprocessing
from multiprocessing import Process
from multiprocessing.synchronize import Event
from multiprocessing.connection import PipeConnection
from lib.Signals import Signal, DataSignal, HostSignal, HostTerminate, SignalSet, SignalAppend, HostWait
from typing import Mapping, Any, Dict
from lib.Hosts.ProcessingBus import ProcessingBus


class MainBus(Bus):
    def __init__(self, host_bus: PipeConnection = None, a_start_event: Event = None, a_end_event: Event = None, this_process : Process = None, name : str = str()):
        super(MainBus, self).__init__()
        self._bus = host_bus
        self._a_start_event = a_start_event
        self._a_finish_event = a_end_event
        self._alias = dict()  # type:  Dict[Any, GhostNode]
        self._process = this_process
        if len(name) == 0:
            name = str(random.randint(0, 65535))
        self.name = name
        self._terminate_request = multiprocessing.Event()

        # List of processes
        self._processes = dict()  # type: Dict[str, multiprocessing.Process]

        # List of ProcessingHosts
        self._process_hosts = dict()  # type: Dict[str, ProcessingBus]

        # Message routing
        # dst node -> dst host (where to send to)
        self._routing = dict()  # type: Dict[str, str]

        # List of a_start events
        self._a_start_events = dict()  # type: Dict[str, Event]

        # List of a_finish events
        self._a_finish_events = dict()  # type: Dict[str, Event]

        # List of cross-process buses (queues)
        self._host_buses = dict()  # type: Dict[str, multiprocessing.connection]

        # Output signal buffers host_name --> list <signal>
        self._output_buffers = dict()  # type: Dict[str, list]

        # Number of exec() full stages passed
        self.iteration = 0

    def join(self, node_lists : list, host_names: list = None):
        # TODO: Check: Is join() can actually join a new host
        # TODO: Check: Will join() add node to an existing Bus if the hostname matches
        if host_names is None:
            host_names = ["{0}.ProcHost_{1}".format(self.name, k) for k in range(len(node_lists))]

        for nodes_index in range(len(node_lists)):
            nodes = node_lists[nodes_index]
            new_host_name = host_names[nodes_index]

            # Initialize bus (Pipe) and buffer
            bus = multiprocessing.Pipe()
            self._host_buses[new_host_name] = bus[0]
            self._output_buffers[new_host_name] = list()

            # Init a-start and a-finish events
            self._a_start_events[new_host_name] = multiprocessing.Event()
            self._a_finish_events[new_host_name] = multiprocessing.Event()
            self._a_finish_events[new_host_name].set()

            # Init ProcessingBus class
            host = ProcessingBus(bus[1], a_start_event=None,
                                 a_end_event=None, name=new_host_name)

            proc = multiprocessing.Process(target=host.run, args=(bus[1], self._a_start_events[new_host_name], self._a_finish_events[new_host_name]))

            host.set_process(proc)

            self._process_hosts[new_host_name] = host
            self._processes[new_host_name] = proc
            # TODO: Pass also a process...

            # Add nodes:
            for node in nodes:
                # Add nodes to ProcessHost
                host.add_node(node, override_index=False)

                # Add routing record
                self._routing[node.index] = new_host_name

                # Add a mirror node to master. Mirror node is not added to routing
                # since it doesn't expected to intercept messages
                # (except data, which is processed by process_data_signal)
                ghost = node.copy(dst=GhostNode())
                self.add_node(ghost, override_index=False)

            host.update_alias()
        self.update_alias()

    def belongs_here(self, index):
        return index in self._alias

    def update_alias(self):
        for node in self._nodes:
            if node.index not in self._alias:
                self._alias[node.index] = node

    def process_data_signal(self, signal):
        """Update Node's states (receive set, append, set_last)"""
        if isinstance(signal, SignalSet):
            self._alias[signal.dst].set(signal.key, signal.value, mirror=False)
        elif isinstance(signal, SignalAppend):
            self._alias[signal.dst].append(signal.key, signal.value, mirror=False)
        else:
            print("[ProcessingBus|{0}]: No data instructions for signal {1}".format(self.name, type(signal)))

    def process_host_signal(self, signal):
        """Signals for managing processing host itself"""
        if isinstance(signal, HostTerminate):
            # Terminate signal
            print(str("[ProcessingBus|{0}]: Terminating...").format(self.name))
            self._process.terminate()  # TODO: Shall be add at process creation by the Master host
        elif isinstance(signal, HostWait):
            time.sleep(signal.time())
        else:
            print("[ProcessingBus|{0}]: No host instructions for signal {1}".format(self.name, type(signal)))

    def distribute_inputs(self):
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
        while not self._terminate_request.is_set():
            print('#{1} [MainBus|{0}]: Start A-phase'.format(self.name, self.iteration))

            # Start ProcessHosts:
            for key in self._process_hosts.keys():
                self._a_finish_events[key].clear()
                self._a_start_events[key].set()

            # TODO: Stages goes here (but can also go at the end for some case i forgot)
            # Ah, yes. Depends on reverse-mirroring.

            # Wait for ProcessHosts
            for key in self._process_hosts.keys():
                self._a_finish_events[key].wait()

            print('#{1} [MainBus|{0}]: End A-phase'.format(self.name, self.iteration))

            # Routing phase I: Clear buffer
            for key in self._output_buffers:
                self._output_buffers[key].clear()

            # Routing phase II. Buffer input (and route)
            print('#{0} [MainBus|{1}]: Prerouting...'.format(self.iteration, self.name))
            for key in self._host_buses:
                bus = self._host_buses[key]
                print('#{0} [MainBus|{1}]: Prerouting bus {2}. Has elements: {3}'.format(self.iteration, self.name, bus, bus.poll()))
                while bus.poll():
                    signal = bus.recv()
                    print('#{0} [MainBus|{1}]: Prerouting signal {2}'.format(self.iteration, self.name, signal))
                    dst = signal.dst
                    if dst == self.name:
                        self.process_host_signal(signal)
                        # TODO: process_host handling for Master may differ
                    elif isinstance(signal, DataSignal):
                        # TODO: GhostNodes data updates
                        self.process_data_signal(signal)
                    else:
                        # TODO: Safe stuff and exception handling
                        self._output_buffers[self._routing[dst]].append(signal)

            # Routing phase III. Send back to nodes
            for key in self._process_hosts.keys():
                for msg in self._output_buffers[key]:
                    self._host_buses[key].send(msg)
                    print('#{2} [MainBus|{0}]: Send signal {1}'.format(self.name, msg, self.iteration))

            self.iteration += 1

            for key in self._alias:
                print("{0}'s counter = {1}".format(key, self._alias[key].get('exec_counter')))

        # When _terminate_request event is set, execution cycle ends and Master sends termination signals to hosts:
        for host in self._process_hosts.values():
            host.emit(HostTerminate(host.name, self.name))

    def emit(self, signal: Signal):
        self._bus.send(signal)
        # TODO: Thread lock?

    def run(self):
        print("[MainBus|{0}] Launching Processors ...".format(self.name))

        try:
            for proc_host in self._process_hosts:
                if not self._process_hosts[proc_host].get_process().is_alive():
                    self._processes[proc_host].start()
        except Exception:
            print("[MainBus|{0}] PANIC: Processor launching has interrupted!".format(self.name))
        else:
            print("[MainBus|{0}] Hosts launched!".format(self.name))

