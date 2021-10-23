from utils.Stage import Stage
from lib.Bus import Bus
import networkx
import matplotlib.pyplot as plt


def default_color_rule(data):
    return (data['wealth'], 0, 0)


class StagePlotGraph(Stage):
    def __init__(self, host=Bus(), name=str(), enabled=True, axes=None, color_rule=default_color_rule, normalize=True, ground_normalize=True,
                 replot_on=1, bgcolor='white'):
        super(StagePlotGraph, self).__init__(host, name, enabled)
        self._host = host
        self._enabled = enabled
        self.name = name
        if axes is None:
            self._fig = plt.figure(0)
            self._axes = self._fig.add_axes((0, 0, 1, 1))
        else:
            self._axes = axes
        self._is_first_run = True
        self._graph = None
        self._netx = None
        self._color_rule = color_rule
        self._normalize = normalize
        self._replot_on = replot_on
        self._stage = 0
        self._ground_norm = ground_normalize
        self._bgcolor = bgcolor

    def _first_run(self):
        self._graph = networkx.Graph()
        nodes, links = self._host.save_structure()
        self._graph.add_nodes_from(nodes)
        self._graph.add_edges_from(links)
        colors = [(0, 0, 0) for node in range(len(nodes))]
        self._netx = networkx.draw_networkx(self._graph, ax=self._axes, with_labels=False, node_size=42,
                                            edge_color='gray', node_color=colors, pos=networkx.kamada_kawai_layout(self._graph))
        plt.draw()
        plt.ioff()
        self._axes.set_facecolor(self._bgcolor)
        self._fig.canvas.manager.window.attributes('-topmost', 0)

    def run(self):
        if not super(StagePlotGraph, self).run():
            return False

        if self._is_first_run:
            self._is_first_run = False
            self._first_run()

        if self._stage % self._replot_on != 0:
            return True

        colors = self._host.apply(self._color_rule)
        if self._normalize:
            # This too enlarged code is for min/max bug in python
            channels = [[float(colors[rec][ch]) for rec in range(len(colors))]for ch in range(3)]

            if self._ground_norm:
                min_color = [0, 0, 0]
            else:
                min_color = [min(channels[ch]) for ch in range(3)]

            max_color = [max(channels[ch]) for ch in range(3)]

            delta_color = [max_color[ch] - min_color[ch] if max_color[ch] != min_color[ch] else 1 for ch in range(3)]

            colors = list(map(lambda color:
                              list(map(lambda ch: (color[ch] - min_color[ch]) / delta_color[ch], range(3)))
                              , colors))

        # Update node colors
        self._axes.collections[0].set_facecolor(colors)

        plt.pause(0.1)
        self._stage += 1

        return True
