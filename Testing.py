from lib.Node import Node
from lib.Host import Host
from lib.NetworkBuilders.BuildCompleteGraph import BuildCompleteGraph
from lib.NetworkBuilders.DropoutDesaturate import DropoutDesaturate
from lib.NetworkBuilders.BuildParametricalGraph import BuildParametricalGraph

nodes = 1000
goal = {2:0.2, 3:0.2, 4:0.6}
host = BuildParametricalGraph().build([nodes, goal, 1])
result = host.graph_statistics_dict()
for k in result:
    result[k] = result[k] / nodes

host.print_data()
print("\nGoal: ", goal)
print("\nResult: ", result)
