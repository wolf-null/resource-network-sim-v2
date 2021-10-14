from lib.Host import Host


class Stage:
    def __init__(self, host=Host(), name=str(), enabled=True):
        self._host = host
        self._enabled = enabled
        self.name = name
        self._terminal = None  # multiprocessing.connection

    def set_host(self, host=Host()):
        self._host = host

    def run(self):
        if not self._enabled:
            return False
        return True

    def halt(self):
        pass
