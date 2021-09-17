class Signal:
    def __init__(self, dst=None, src=None):
        self.dst = dst
        self.src = src

    def __repr__(self):
        return repr("<Signal:{0}| {1} --> {2} >".format(type(self).__name__, self.src, self.dst))

# ----------------------------------------- DATA SIGNALS -----------------------------------------------


class DataSignal(Signal):
    pass


class SignalSet(DataSignal):
    def __init__(self, dst=None, src=None, key=None, value=None):
        super(SignalSet, self).__init__(dst=dst, src=src)
        self.key = key
        self.value = value

    def key(self):
        return self.key()

    def value(self):
        return self.value()


class SignalAppend(DataSignal):
    def __init__(self, dst=None, src=None, key=None, value=None):
        super(SignalAppend, self).__init__(dst=dst, src=src)
        self.key = key
        self.value = value

    def key(self):
        return self.key()

    def value(self):
        return self.value()


# ----------------------------------------- HOST SIGNALS -----------------------------------------------


class HostSignal(Signal):
    pass


class HostTerminate(HostSignal):
    pass


class HostWait(HostSignal):
    def __init__(self, dst=None, src=None, time=0):
        super(HostWait, self).__init__(src=src, dst=dst)
        self._time = time

    def time(self):
        return self._time


# ----------------------------------------- NODE SIGNAL -----------------------------------------------

class NodeSignal(Signal):
    pass


class SignalIsAlive(NodeSignal):
    pass

