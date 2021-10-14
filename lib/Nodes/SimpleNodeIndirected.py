from lib.Node import Node
from random import choice, randint, random


class Transaction:
    pass


class StraightTransaction(Transaction):
    def __init__(self, amount):
        self.amount = amount


class ReverseTransaction(Transaction):
    def __init__(self, amount=0):
        self.amount = amount


class SimpleNodeIndirected(Node):
    def __init__(self, index = -1, initial_wealth=0, **kwargs):
        super(SimpleNodeIndirected, self).__init__(index, initial_wealth, **kwargs)
        if 'max_transaction' in kwargs:
            self._data['max_transaction'] = kwargs['max_transaction']
        else:
            self._data['max_transaction'] = 1

        if 'idle_threshold' in kwargs:
            self._idle_threshold = kwargs['idle_threshold']
        else:
            self._idle_threshold = -1
        self._idle_counter = 0
        self.set_idle(False)

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

        outcome_multiplier = 1
        total_income = 0
        self.delayed_outcome = 0

        # Explanation of the following code and the original problem is discussed in /Problems.md
        if self._idle_threshold > 0:
            if len(my_input_buffer) == 0:
                self._idle_counter += 1
            else:
                self._idle_counter = 0

            if self._idle_counter >= self._idle_threshold:
                if len(my_input_buffer) == 0:
                    self.set_idle(True)

        if self.is_idle():
            outcome_multiplier = 0

        for income in my_input_buffer:
            if isinstance(income[2], StraightTransaction):
                total_income += income[2].amount
            elif isinstance(income[2], ReverseTransaction):
                send_amount = min(randint(1, self.get('max_transaction')), self.get('wealth')) * outcome_multiplier
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
        return int(outcome_multiplier)

    def post_exec(self):
        pass

