from lib.NetworkBuilders.Coloring import Coloring
from lib.NetworkBuilders.BuildCompleteGraph import BuildCompleteGraph
from lib.NetworkBuilders.DropoutLimited import DropoutLimited
from lib.NetworkBuilders.BuildGridGraph import BuildGridGraph
from lib.NetworkBuilders.ColoringFaster import ColoringFaster
from lib.Stages.StageExec import StageExec
from lib.Nodes.SimpleNode import SimpleNode

if __name__ == '__main__':
    n = 3
    network = ColoringFaster(BuildGridGraph(node_initializer=lambda: SimpleNode(initial_wealth=10))).build(n)
    print('colors: ', network.hist_values('color'))

    initial = network.hist_values('wealth')
    print(initial)
    print(sum(map(lambda key: key * initial[key], initial)))

    stage_exec = StageExec(network, 'exec_node')
    stage_exec.run()

    final = network.hist_values('wealth')
    print(final)
    print(sum(map(lambda key: key*final[key], final)))
