class Signal:
    def __init__(self, dst=None, src=None):
        self.dst = dst
        self.src = src

# ----------------------------------------- DATA SIGNALS -----------------------------------------------


class DataSignal(Signal):
    pass


class SignalSet(DataSignal):
    def __init__(self, dst=None, src=None, key=None, value=None):
        super(SignalSet, self).__init__(src, dst)
        self.key = key
        self.value = value

    def key(self):
        return self.key()

    def value(self):
        return self.value()


class SignalAppend(DataSignal):
    def __init__(self, dst=None, src=None, key=None, value=None):
        super(SignalAppend, self).__init__(src, dst)
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
