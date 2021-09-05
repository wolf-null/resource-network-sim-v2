from lib.NewtorkBuilder import NetworkBuilder
from random import choice
from lib.Node import Node
from lib.Host import Host


class Coloring(NetworkBuilder):
    def __init__(self, previous=None, color_variable='color'):
        super(Coloring, self).__init__(previous)
        self._color_variable = color_variable

    def building_operations(self, n=0):
        print('[Coloring]: Start')

        def no_color(data):
            return self._color_variable not in data

        def has_color(data):
            return self._color_variable in data

        unpainted = self._host.filter_indexes(no_color)

        first_painted = choice(unpainted)
        painted = [first_painted, ]
        unpainted.remove(first_painted)
        colors = [0, ]
        self._host.get_node(first_painted).set(self._color_variable, 0)

        while len(unpainted) != 0:
            front = self._host.filter_indexes(no_color, from_indexes=self._host.neighbors(painted))
            new_painted = choice(front)
            new_painted_neighbors = self._host.filter_indexes(has_color, from_indexes=self._host.neighbors([new_painted,]))
            used_colors = list(self._host.hist_values(self._color_variable, from_indexes=new_painted_neighbors).keys())
            available_colors = colors.copy()
            for color in used_colors:
                if color in available_colors:
                    available_colors.remove(color)

            if len(available_colors) == 0:
                # Create new color type
                new_painted_color = len(used_colors)
                used_colors.append(new_painted_color)
            else:
                new_painted_color = choice(available_colors)

            self._host.get_node(new_painted).set(self._color_variable, new_painted_color)
            painted.append(new_painted)
            unpainted.remove(new_painted)




