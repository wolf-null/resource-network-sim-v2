from lib.Nodes.GhostNode import GhostNode
from lib.Signals import SignalIsAlive
import time


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
        print("[GhostNode|{0}]: pop input".format(self.index))

        signals_got = self.pop_signal()
        for signal in signals_got:
            print("[HeartbeatNode|{0}] Received signal {1}".format(self.index, signal))

        print("[GhostNode|{0}]: send signal".format(self.index))

        time.sleep(2)
        print("[GhostNode|{0}]: awake".format(self.index))

        for send_to in self.get('heartbeat_dst'):
            sig = SignalIsAlive(src=self.index, dst=send_to)
            print("[GhostNode|{0}]: send signal {1}".format(self.index, sig))
            self.emit(sig)

        print("[GhostNode|{0}]: update counter".format(self.index))
        self.set('exec_counter', self.get('exec_counter') + 1)
        print("[GhostNode|{0}]: exec() end".format(self.index))
