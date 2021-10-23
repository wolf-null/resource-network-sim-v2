from lib.Nodes.CommittedNode import CommittedNode
from lib.Signals import SignalIsAlive
import random as rnd


class HeartbeatNode(CommittedNode):
    """
    Sends IsAliveSignal to all nodes listed in the heartbeat_dst at the exec()
    """

    def __init__(self, **kwargs):
        """
        :param heartbeat_dst: list <str> - a list of nodes to which IsAliveSignal to be sent at the exec()
        """
        super(HeartbeatNode, self).__init__(**kwargs)
        if 'heartbeat_dst' in kwargs:
            self.set('heartbeat_dst', kwargs['heartbeat_dst'], mirror=False)
        else:
            self.set('heartbeat_dst', list(), mirror=False)
        self.set('exec_counter', 0)

    def exec(self):
        self.print("Exec!")

        signals_got = self.pop_signals()
        for signal in signals_got:
            self.print("Received signal {0}".format(signal))

        for send_to in self.get('heartbeat_dst'):
            sig = SignalIsAlive(src=self.index, dst=send_to)
            self.print("send signal {0}".format(sig))
            self._host.emit(sig)

        self.set('exec_counter', self.get('exec_counter') + 1)
        self.print("exec() end")

        self.iteration += 1
