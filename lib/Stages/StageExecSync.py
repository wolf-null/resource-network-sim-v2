from lib.Stage import Stage
from lib.Host import Host
from random import shuffle
import threading


def pipeline_exec(nodes):
    for node in nodes:
        node.exec()


class StageExecSync(Stage):
    def __init__(self, host=Host(), name=str(), enabled=True, seek_color='color', number_of_substages=1):
        super(StageExecSync, self).__init__(name, enabled)
        self._first_start = True
        self._pipelines = list()
        self._seek_color = seek_color
        self._substages = number_of_substages
        self._host = host

    def prepare_split_scheme(self):
        all_colors = list(self._host.hist_values(self._seek_color).keys())

        for color in all_colors:
            nodes_of_color = self._host.filter(lambda data: data[self._seek_color] == color)
            self._pipelines.append([nodes_of_color, ])

    def run(self):
        if not super(StageExecSync, self).run():
            return False

        if self._first_start:
            self._first_start = False
            self.prepare_split_scheme()

        for substage in range(self._substages):
            for pipeline in range(len(self._pipelines)):
                shuffle(self._pipelines)

                threads = list()
                for pipeline in range(len(self._pipelines)):
                    new_thread = threading.Thread(target=pipeline_exec, args=(*self._pipelines[pipeline],))
                    threads.append(new_thread)
                    new_thread.start()

                for thread in threads:
                    thread.join()

        return True
