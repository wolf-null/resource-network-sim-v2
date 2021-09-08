from lib.NetworkBuilders.Coloring import Coloring
from lib.NetworkBuilders.BuildCompleteGraph import BuildCompleteGraph
from lib.NetworkBuilders.DropoutLimited import DropoutLimited
from lib.NetworkBuilders.BuildGridGraph import BuildGridGraph
from lib.NetworkBuilders.ColoringFaster import ColoringFaster
from lib.Stages.StageExecParallel import StageExecParallel
from lib.Stages.StageExec import StageExec
from lib.Nodes.SimpleNode import SimpleNode
from lib.Nodes.SimpleNodeIndirected import SimpleNodeIndirected
from lib.Stages.StagePlotGraph import StagePlotGraph
import time
import keyboard

if __name__ == '__main__':
    n = 20

    def save_stat(gt, st):
        st('sum_wealth', gt('sum_wealth', 0) + gt('wealth', 0))

    def color_rule(data):
        return (data['sum_wealth'] if 'sum_wealth' in data else 0, 0, 0)

    network = ColoringFaster(BuildGridGraph(node_initializer=lambda: SimpleNodeIndirected(initial_wealth=1000, max_transaction=10))).build(n)
    initial = network.hist_values('wealth')
    stage_exec = StageExec(network, 'exec_node', number_of_substages=100)
    stage_graplot = StagePlotGraph(network, color_rule=color_rule, bgcolor='darkgray', ground_normalize=False)

    print('start load')
    iteration = 0
    while not keyboard.is_pressed('ctrl+break'):
        stage_exec.run()
        if iteration % 20 == 0 and iteration >= 400:
            network.apply_get_set(save_stat)
        stage_graplot.run()
        hist = network.hist_values('wealth')
        summary = sum(network.apply(lambda data: data['wealth']))
        iteration += 1
        print('\riter: {0}'.format(iteration), end='')


