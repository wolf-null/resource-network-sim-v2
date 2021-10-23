from lib.Nodes.CommittedNode import CommittedNode
from random import choice, randint, random


class Transaction:
    pass


class StraightTransaction(Transaction):
    def __init__(self, amount):
        self.amount = amount


class ReverseTransaction(Transaction):
    def __init__(self, amount=0):
        self.amount = amount


class SimpleNodeIndirected(CommittedNode):
    def __init__(self, index = -1, initial_wealth=0, **kwargs):
        super(SimpleNodeIndirected, self).__init__(index, initial_wealth, **kwargs)
        if 'max_transaction' in kwargs:
            self._state['max_transaction'] = kwargs['max_transaction']
        else:
            self._state['max_transaction'] = 1

        self.delayed_outcome = 0
        self.remember()

    def remember(self):
        # Historical stuff
        if 'wealth_history' not in self:
            self.set('wealth_history', list())
        self.append('wealth_history', self.get('wealth'))

    def exec(self):
        my_input_buffer = self.pop_signals()
        self.set('wealth', self.get('wealth') - self.delayed_outcome)

        total_income = 0
        self.delayed_outcome = 0

        for income in my_input_buffer:
            if isinstance(income[2], StraightTransaction):
                total_income += income[2].amount
            elif isinstance(income[2], ReverseTransaction):
                send_amount = min(randint(1, self.get('max_transaction')), self.get('wealth'))
                dst = income[1]
                self.send_signal(dst, StraightTransaction(send_amount))
                self.delayed_outcome += send_amount
            else:
                total_income += income[2].amount
        self.set('wealth', self.get('wealth') + total_income)

        dst = choice(self.get_connections()[0])
        if random() >= 0.5:
            send_amount = min(randint(1, self.get('max_transaction')), self.get('wealth'))
            self.send_signal(dst, StraightTransaction(send_amount))
            self.delayed_outcome += send_amount
        else:
            self.send_signal(dst, ReverseTransaction())

        self.remember()
        return 1

    def post_exec(self):
        pass

