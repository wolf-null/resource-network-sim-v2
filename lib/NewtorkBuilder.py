from lib.Host import Host
from abc import ABC, abstractmethod


class NetworkBuilder:
    def __init__(self, previous=None):
        self._previous_builder = previous
        self._host = Host()

    def build(self, param):
        # An ugly solution for generalization of build() usage:
        if isinstance(param, Host):
            self._host = param

        if isinstance(self._previous_builder, NetworkBuilder):
            self._host = self._previous_builder.build(param)

        self.building_operations(param)
        return self._host

    @abstractmethod
    def building_operations(self, n=0):
        pass

