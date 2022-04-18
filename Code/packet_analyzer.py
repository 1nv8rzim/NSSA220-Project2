from filter_packets import *
from packet_parser import *
from compute_metrics import *

node1, node2, node3, node4 = parse()
node1, node2, node3, node4 = filter(node1, node2, node3, node4)
compute(node1, node2, node3, node4)
