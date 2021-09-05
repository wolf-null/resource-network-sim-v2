from lib.NewtorkBuilder import NetworkBuilder
from random import choice
from lib.Node import Node
from lib.Host import Host


class ColoringFaster(NetworkBuilder):
    def __init__(self, previous=None, color_variable='color', stages=1):
        super(ColoringFaster, self).__init__(previous)
        self._color_variable = color_variable

    def building_operations(self, n=0):
        print('[ColoringFaster]: Start')

        for k in range(self._host.size):
            self._host.get_node(k).set(self._color_variable, k)

        for k in range(self._host.size-1, -1, -1):
            neighbors = self._host.neighbors([k, ])
            near_colors = list(self._host.hist_values(self._color_variable, neighbors))
            new_color = 0
            while new_color in near_colors:
                new_color += 1
            self._host.get_node(k).set(self._color_variable, new_color)







