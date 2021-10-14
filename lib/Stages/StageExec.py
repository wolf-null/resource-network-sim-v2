from lib.Stage import Stage
from lib.Bus import Bus
from random import shuffle
import threading


def pipeline_exec(nodes):
    for node in nodes:
        node.exec()


class StageExec(Stage):
    def __init__(self, host=Bus(), name=str(), enabled=True, number_of_substages=1):
        super(StageExec, self).__init__(name, enabled)
        self._n_substages = number_of_substages
        self._host = host

    def run(self):
        if not super(StageExec, self).run():
            return False

        for substage in range(self._n_substages):
            order = list(range(self._host.size))
            shuffle(order)
            for node in order:
                self._host.get_node(node).exec()

            for node in order:
                self._host.get_node(node).post_exec()

        return True
