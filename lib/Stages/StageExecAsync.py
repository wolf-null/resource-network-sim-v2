import random

from lib.Stage import Stage
from lib.Bus import Bus
from random import shuffle
import threading


class StageRequests:
    pass


class StageRequestHalt(StageRequests):
    def __init__(self):
        self._halt = False

    def is_halt(self):
        return self._halt

    def halt(self):
        self._halt = True


def pipeline_exec(nodes, halt_signal=StageRequestHalt(), random_order=True):
    tid = random.randint(0, 65535)
    print('[ExecAsync]: A thread {0} with {1} nodes is started!\n'.format(tid, len(nodes)))
    iteration = 0
    idle = 0
    while not halt_signal.is_halt():
        if random_order:
            # Shuffle if random execution order enabled.
            shuffle(nodes)

        for node in nodes:
            idle += node.exec()

        iteration += 1

    print('\n[ExecAsync]: {0} halted at #{1}. Idles: {2}. Efficiency: {3}% \n'.format(tid, iteration, idle, round(100*(1-idle/iteration/len(nodes)), 3)))


class StageExecAsync(Stage):
    def __init__(self, host=Bus(), name=str(), enabled=True, seek_color='color', random_order=True):
        super(StageExecAsync, self).__init__(name, enabled)
        self._first_start = True
        self._pipelines = list()
        self._seek_color = seek_color
        self._host = host
        self._threads = list()
        self._thread_halt_request = list()
        self._random_order = random_order

    def prepare_split_scheme(self):
        all_colors = list(self._host.hist_values(self._seek_color).keys())

        for color in all_colors:
            nodes_of_color = self._host.filter(lambda data: data[self._seek_color] == color)
            self._pipelines.append([nodes_of_color, ])

    def run(self):
        if not super(StageExecAsync, self).run():
            return False

        if self._first_start:
            self._first_start = False
            self.prepare_split_scheme()

            for pipeline in range(len(self._pipelines)):
                new_halt_request = StageRequestHalt()
                self._thread_halt_request.append(new_halt_request)
                new_thread = threading.Thread(target=pipeline_exec, args=(*self._pipelines[pipeline], new_halt_request, self._random_order))
                self._threads.append(new_thread)

                new_thread.start()

        return True

    def halt(self):
        for thread_halt in self._thread_halt_request:
            thread_halt.halt()

        for thread in self._threads:
            thread.join()
