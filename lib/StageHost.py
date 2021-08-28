from lib.Host import Host


class StageHost(Host):
    def __init__(self):
        super(StageHost, self).__init__()
        self.stages = list()

    def run_epoch(self):
        for stage in self.stages:
            stage.run()
