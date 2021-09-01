from lib.Node import Node
from lib.Host import Host
from lib.NetworkBuilders.BuildCompleteGraph import BuildCompleteGraph
from lib.NetworkBuilders.DropoutDesaturate import DropoutDesaturate
from lib.NetworkBuilders.BuildParametricalGraph import BuildParametricalGraph

"""
host = Host()
a, b, c, d = [Node() for k in range(4)]
host.add_nodes([a, b, c, d])
host.connect_n([[0,1],[1,2],[3,2]])
print(host.check_connectivity())
"""

#host = BuildCompleteGraph().build(4)
# host = DropoutDesaturate(BuildCompleteGraph(), dropout=0.5).build(4)

"""
host = BuildCompleteGraph().build(4)
print(host.print_data())
print("-------------------------------------")
host = DropoutDesaturate(dropout=0.5).build(host)
print(host.check_connectivity())
print(host.print_data())
"""

"""host = Host()
a0, a1, a2, a3, a4, a5 = [Node() for k in range(6)]
host.add_nodes([a0, a1, a2, a3, a4, a5])
host.connect_both_ways_n([(0,1), (1,2), (1,3), (1,4), (1,5), (2,3), (4,5)])
print(host.check_connectivity())
"""

# host = BuildParametricalGraph().build( [6, {1:1, 2:4, 3:0, 4:0, 5:1}])
# host = BuildParametricalGraph().build( [11, {1:6, 2:3, 3:1, 4:0, 5:1}])
host = BuildParametricalGraph().build( [8, {1:4, 2:0, 3:4}])
