from lib.Node import Node
from random import choice, randint


class SimpleNode(Node):
    def __init__(self, index = -1, initial_wealth=0, **kwargs):
        super(SimpleNode, self).__init__(index, initial_wealth, **kwargs)
        if 'max_transaction' in kwargs:
            self._data['max_transaction'] = kwargs['max_transaction']
        else:
            self._data['max_transaction'] = 1
        self.delayed_outcome = 0
        self.remember()

    def remember(self):
        # Historical stuff
        if 'wealth_history' not in self:
            self.set('wealth_history', list())
        self.append('wealth_history', self.get('wealth'))

    def exec(self):
        my_input_buffer = self.pop_signal_stack()
        self.set('wealth', self.get('wealth') - self.delayed_outcome)

        total_income = 0
        for income in my_input_buffer:
            total_income += income[2]
        self.set('wealth', self.get('wealth') + total_income)

        send_amount = min(randint(1, self.get('max_transaction')), self.get('wealth'))
        dst = choice(self.get_connections()[0])

        self.send_signal(dst, send_amount)
        self.delayed_outcome = send_amount

        self.remember()

        return len(my_input_buffer) == 0

    def post_exec(self):
        pass

