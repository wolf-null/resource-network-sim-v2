import random

from lib.Host import Host
from lib.Node import Node
from lib.Nodes.GhostNode import GhostNode
from lib.Errors import HostError_NoSuchNode
import multiprocessing
from multiprocessing import Process
from multiprocessing.synchronize import Event
from multiprocessing.connection import PipeConnection
from lib.Signals import Signal, DataSignal, HostSignal, HostTerminate
from typing import Mapping, Any


class ProcessingHost(Host):
    def __init__(self, host_bus: PipeConnection = None, a_start_event: Event = None, a_end_event: Event = None, this_process : Process = None, name : str = str()):
        super(ProcessingHost, self).__init__()
        self.__bus = host_bus
        self.__a_start_event = a_start_event
        self.__a_finish_event = a_end_event
        self.__alias = Mapping[Any, GhostNode]  # type:  Mapping[Any, GhostNode]
        self.__process = this_process
        if len(name) == 0:
            name = str(random.randint(0, 65535))
        self.name = name

    def update_alias(self):
        for node in self.__nodes:
            if node.index not in self.__alias:
                self.__alias[node.index] = node

    def belongs_here(self, index):
        return index in self.__alias

    def process_data_signal(self, signal):
        pass

    def process_host_signal(self, signal):
        if isinstance(signal, HostTerminate):
            print(str("[ProcessingHost|{1}]: Terminating...").format(self.name))
            self.__process.terminate()

    def distribute_inputs(self):
        while self.__bus.poll():
            signal = self.__bus.recv()
            if isinstance(signal, DataSignal):
                self.process_data_signal(signal)
            elif isinstance(signal, HostSignal):
                self.process_host_signal(signal)
            else:
                dst = signal.dst
                if self.belongs_here(dst):
                    self.__alias[dst].emit(signal)
                else:
                    raise HostError_NoSuchNode('The node {0} is not here!'.format(dst))

    def exec(self):
        self.__a_start_event.wait()
        self.distribute_inputs()
        for node in self.__alias:
            node.exec()
        self.__a_finish_event.set()

    def run(self):
        pass
