from lib.Hosts.MainBus import MainBus
from lib.Nodes.HeartbeatNode import HeartbeatNode


if __name__ == '__main__':
    master = MainBus(name='master')
    node_Alice = HeartbeatNode(index='Alice', heartbeat_dst=['Bob', 'Charlie'])
    node_Bob = HeartbeatNode(index='Bob', heartbeat_dst=['Alice', 'Charlie'])
    node_Charlie = HeartbeatNode(index='Charlie', heartbeat_dst=['Alice', 'Bob'])

    master.join([[node_Alice, ], [node_Bob, node_Charlie]])
    master.run()
    master.exec()

