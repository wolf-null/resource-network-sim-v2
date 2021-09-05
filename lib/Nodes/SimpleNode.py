from lib.Node import Node
from random import choice, randint


class SimpleNode(Node):
    def __init__(self, index = -1, initial_wealth=0, **kwargs):
        super(SimpleNode, self).__init__(index, initial_wealth, **kwargs)
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
        my_input_buffer = self.receive_stack_wealth()

        for income in my_input_buffer:
            self._data['wealth'] += income[2]

        send_amount = randint(1, self._data['max_transaction'])
        dst = choice(self.get_connections()[0])
        self.send_wealth(dst, send_amount)
        self._data['wealth'] -= send_amount

        self.remember()

