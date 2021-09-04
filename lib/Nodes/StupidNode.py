from lib.Node import Node
from random import choice, randint


class StupidNode(Node):
    def __init__(self, index = -1, initial_wealth=0, **kwargs):
        super(StupidNode, self).__init__(index, initial_wealth, **kwargs)
        if 'max_transaction' in kwargs:
            self._data['max_transaction'] = kwargs['max_transaction']
        else:
            self._data['max_transaction'] = 1
        self.remember()

    def remember(self):
        # Historical stuff
        if 'wealth_history' in self._data:
            self._data['wealth_history'].append(self._data['wealth'])
        else:
            self._data['wealth_history'] = [self._data['wealth'], ]

    def exec(self):
        for income in self._input_buffer:
            self._data['wealth'] += income[2]
        self._input_buffer.clear()

        self.send_wealth(choice(self.get_connections()[0]), randint(1, self._data['max_transaction']))

        self.remember()

