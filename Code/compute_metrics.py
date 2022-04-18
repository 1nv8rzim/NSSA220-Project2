def compute_metrics(capture, ip):
    total = len(capture)
    
    request = len(capture.lambda_filter(lambda cap: 'Echo (ping) request' in cap.info))
    reply = len(capture.lambda_filter(lambda cap: 'Echo (ping) reply' in cap.info))
    request_sent = len(capture.lambda_filter(lambda cap: cap.source == ip and 'Echo (ping) request' in cap.info))
    request_recv = len(capture.lambda_filter(lambda cap: cap.destination == ip and 'Echo (ping) request' in cap.info))
    reply_sent = len(capture.lambda_filter(lambda cap: cap.source == ip and 'Echo (ping) reply' in cap.info))
    reply_recv = len(capture.lambda_filter(lambda cap: cap.destination == ip and 'Echo (ping) reply' in cap.info))
    
    print(total, request, request_sent, request_recv, reply, reply_sent, reply_recv)

def compute(node1, node2, node3, node4) :
	compute_metrics(node1, '192.168.100.1')
	compute_metrics(node2, '192.168.100.2')
	compute_metrics(node3, '192.168.200.1')
	compute_metrics(node4, '192.168.200.2')



