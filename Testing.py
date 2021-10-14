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

from lib.Hosts.MasterBus import MasterBus
from lib.Nodes.HeartbeatNode import HeartbeatNode


if __name__ == '__main__':
    master = MasterBus(name='master')
    node_Alice = HeartbeatNode(index='Alice', heartbeat_dst=['Bob', 'Charlie'])
    node_Bob = HeartbeatNode(index='Bob', heartbeat_dst=['Alice', 'Charlie'])
    node_Charlie = HeartbeatNode(index='Charlie', heartbeat_dst=['Alice', 'Bob'])

    master.join([[node_Alice, ], [node_Bob, node_Charlie]])
    master.run()
    master.exec()

