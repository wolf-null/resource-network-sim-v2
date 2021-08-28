from lib.Node import Node
from lib.Host import Host
from lib.NetworkBuilders.BuildCompleteGraph import BuildCompleteGraph
from lib.NetworkBuilders.DropoutDesaturate import DropoutDesaturate

"""
host = Host()
a, b, c, d = [Node() for k in range(4)]
host.add_nodes([a, b, c, d])
host.connect_n([[0,1],[1,2],[3,2]])
print(host.check_connectivity())
"""

#host = BuildCompleteGraph().build(4)
# host = DropoutDesaturate(BuildCompleteGraph(), dropout=0.5).build(4)
host = BuildCompleteGraph().build(4)
print(host.print_data())
print("-------------------------------------")
host = DropoutDesaturate(dropout=0.5).build(host)
print(host.check_connectivity())
print(host.print_data())