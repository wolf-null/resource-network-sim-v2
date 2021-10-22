from lib.Nodes.GhostNode import GhostNode
from lib.Signals import SignalIsAlive
import time
import random as rnd

class HeartbeatNode(GhostNode):
    class Broadcast:
        pass

    def __init__(self, **kwargs):
        super(HeartbeatNode, self).__init__(**kwargs)
        if 'heartbeat_dst' in kwargs:
            self.set('heartbeat_dst', kwargs['heartbeat_dst'], mirror=False)
        else:
            self.set('heartbeat_dst', list(), mirror=False)
        self.set('exec_counter', 0)

    def exec(self):
        self.print("Exec!")

        signals_got = self.pop_signal()
        for signal in signals_got:
            self.print("Received signal {0}".format(signal))

        self.print("Signals received! Now sleep!")

        bench = [rnd.random() for k in range(1000000)]
        rnd.shuffle(bench)
        for k in range(len(bench)-1):
            bench[k+1] = bench[k] * bench[k+1]
        self.print("Sum = {0}".format(sum(bench)))

        self.print("Awake after sleep")

        for send_to in self.get('heartbeat_dst'):
            sig = SignalIsAlive(src=self.index, dst=send_to)
            self.print("send signal {0}".format(sig))
            self._host.emit(sig)

        self.set('exec_counter', self.get('exec_counter') + 1)
        self.print("exec() end")

        self.iteration += 1
