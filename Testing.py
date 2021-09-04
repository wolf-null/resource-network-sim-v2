"""from lib.Node import Node
from lib.Host import Host
from lib.NetworkBuilders.BuildCompleteGraph import BuildCompleteGraph
from lib.NetworkBuilders.DropoutLimited import DropoutLimited
from lib.NetworkBuilders.BuildParametricalGraph import BuildParametricalGraph"""

"""nodes = 1000
goal = {2:0.2, 3:0.2, 4:0.6}

host = DropoutLimited(BuildParametricalGraph(structure=goal, goal_error=1), dropout=0.5).build(nodes)

result = host.graph_statistics_dict()
for k in result:
    result[k] = result[k] / nodes

host.print_data()
print("\nGoal: ", goal)
print("\nResult: ", result)
"""

from lib.NetworkBuilders.BuildParametricalGraph import BuildParametricalGraph
from lib.NetworkBuilders.DropoutLimited import DropoutLimited

goal = {2:0.2, 3:0.2, 4:0.6}
allowed_error = 1

network_generator = DropoutLimited(BuildParametricalGraph(structure=goal, goal_error=allowed_error), dropout=0.5)

n_nodes = 1000
network = network_generator.build(n_nodes)

# Normalize:
result = network.graph_statistics_dict()
norm_result = {r: result[r]/n_nodes for r in result}

print("\nGoal: ", goal)
print("\nResult: ", norm_result)

