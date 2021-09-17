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
        self._host.print("exec")
        print("[HeartbeatNode|{0}]: Exec!".format(self.index))

        signals_got = self.pop_signal()
        for signal in signals_got:
            print("[HeartbeatNode|{0}] Received signal {1}".format(self.index, signal))

        print("[HeartbeatNode|{0}]: Signals received! Now sleep!".format(self.index))

        time.sleep(2)
        print("[HeartbeatNode|{0}]: Awake after sleep".format(self.index))

        for send_to in self.get('heartbeat_dst'):
            sig = SignalIsAlive(src=self.index, dst=send_to)
            print("[HeartbeatNode|{0}]: send signal {1}".format(self.index, sig))
            self._host.emit(sig)

        self.set('exec_counter', self.get('exec_counter') + 1)
        print("[HeartbeatNode|{0}]: exec() end".format(self.index))
