from PacketCapture import PacketCapture

def filter(node1, node2, node3, node4): 
	node1 = node1.lambda_filter(lambda packet: "Echo (ping) request" in packet.info or "Echo (ping) reply" in packet.info, output='Code/filtered/Node1_filtered.txt')
	node2 = node2.lambda_filter(lambda packet: "Echo (ping) request" in packet.info or "Echo (ping) reply" in packet.info, output='Code/filtered/Node2_filtered.txt')
	node3 = node3.lambda_filter(lambda packet: "Echo (ping) request" in packet.info or "Echo (ping) reply" in packet.info, output='Code/filtered/Node3_filtered.txt')
	node4 = node4.lambda_filter(lambda packet: "Echo (ping) request" in packet.info or "Echo (ping) reply" in packet.info, output='Code/filtered/Node4_filtered.txt')
 
	return node1, node2, node3, node4