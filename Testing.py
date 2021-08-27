from lib.Node import Node
from lib.Host import Host

host = Host()

a, b, c, d = [Node() for k in range(4)]

host.add_nodes([a, b, c, d])

host.connect_n([[0,1],[1,2],[3,2]])

print(host.check_connectivity())
