from PacketCapture import PacketCapture
def parse() :
	node1, node2, node3, node4 = PacketCapture('Captures/Node1.txt'), PacketCapture('Captures/Node2.txt'), PacketCapture('Captures/Node3.txt'), PacketCapture('Captures/Node4.txt')
	return node1, node2, node3, node4