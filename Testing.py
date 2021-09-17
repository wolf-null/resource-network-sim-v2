from lib.NetworkBuilders.Coloring import Coloring
from lib.NetworkBuilders.BuildCompleteGraph import BuildCompleteGraph
from lib.NetworkBuilders.DropoutLimited import DropoutLimited
from lib.NetworkBuilders.BuildGridGraph import BuildGridGraph
from lib.NetworkBuilders.ColoringFaster import ColoringFaster
from lib.Stages.StageExecSync import StageExecSync
from lib.Stages.StageExec import StageExec
from lib.Nodes.SimpleNode import SimpleNode
from lib.Nodes.SimpleNodeIndirected import SimpleNodeIndirected
from lib.Stages.StagePlotGraph import StagePlotGraph
from lib.Stages.StageExecAsync import StageExecAsync
from lib.NetworkBuilders.SameSegments import SameSegments
import time
import keyboard
import multiprocessing as mlproc

from lib.Hosts.MasterHost import MasterHost
from lib.Nodes.HeartbeatNode import HeartbeatNode

if __name__ == '__main__':
    mlproc.set_start_method('forkserver')
    master = MasterHost(name='master')
    node_Alice = HeartbeatNode(heartbeat_dst=['Bob', ], index='Alice')
    node_Bob = HeartbeatNode(heartbeat_dst=['Alice', ], index='Bob')
    master.join([[node_Alice, ], [node_Bob, ]])
    master.run()


    '''
    n = 20

    def save_stat(gt, st):
        st('sum_wealth', gt('sum_wealth', 0) + gt('wealth', 0))

    def color_rule(data):
        return (data['sum_wealth'] if 'sum_wealth' in data else 0, 0, 0)

    network = SameSegments(BuildGridGraph(node_initializer=lambda: SimpleNodeIndirected(initial_wealth=1000, max_transaction=10, idle_threshold=-1)), n_segments=2, random_order=False).build(n)
    initial = network.hist_values('wealth')
    stage_exec = StageExecAsync(network)
    stage_graplot = StagePlotGraph(network, color_rule=color_rule, bgcolor='black', ground_normalize=False)

    print('start load')
    iteration = 0
    while not keyboard.is_pressed('ctrl+break'):
        network.apply_get_set(save_stat)
        stage_graplot.run()
        stage_exec.run()
        hist = network.hist_values('wealth')
        iteration += 1
        print('\riter: {0}'.format(iteration), end='')
        time.sleep(0.1)

    stage_exec.halt()

    time.sleep(0.5)
    stage_graplot.run()
    time.sleep(0.5)

    while keyboard.is_pressed('ctrl+break'):
        pass
    print("press [ ] to exit")
    while not keyboard.is_pressed(' '):
        time.sleep(0.1)
    '''
