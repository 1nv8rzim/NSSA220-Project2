def compute_metrics(capture, ip):
    total = len(capture)
    
    request = len(capture.lambda_filter(lambda cap: 'Echo (ping) request' in cap.info))
    reply = len(capture.lambda_filter(lambda cap: 'Echo (ping) reply' in cap.info))
    request_sent = len(capture.lambda_filter(lambda cap: cap.source == ip and 'Echo (ping) request' in cap.info))
    request_recv = len(capture.lambda_filter(lambda cap: cap.destination == ip and 'Echo (ping) request' in cap.info))
    reply_sent = len(capture.lambda_filter(lambda cap: cap.source == ip and 'Echo (ping) reply' in cap.info))
    reply_recv = len(capture.lambda_filter(lambda cap: cap.destination == ip and 'Echo (ping) reply' in cap.info))
    
    print(total, request, request_sent, request_recv, reply, reply_sent, reply_recv)
    
    request_bytes_sent = sum(packet.length for packet in capture.lambda_filter(lambda cap: cap.source == ip and 'Echo (ping) request' in cap.info).packets)
    request_bytes_recv = sum(packet.length for packet in capture.lambda_filter(lambda cap: cap.destination == ip and 'Echo (ping) request' in cap.info).packets)
    request_bytes_data_sent = sum(packet.length - 42 for packet in capture.lambda_filter(lambda cap: cap.source == ip and 'Echo (ping) request' in cap.info).packets)
    request_bytes_data_recv = sum(packet.length - 42 for packet in capture.lambda_filter(lambda cap: cap.destination == ip and 'Echo (ping) request' in cap.info).packets)
    
    print(request_bytes_sent, request_bytes_recv, request_bytes_data_sent, request_bytes_data_recv)
    
    rtt, data, payload = [], [], []
    for request, reply in zip(capture.lambda_filter(lambda cap: 'Echo (ping) request' in cap.info and ip == cap.source).packets, capture.lambda_filter(lambda cap: 'Echo (ping) reply' in cap.info and ip == cap.destination).packets):
        rtt.append((reply.time - request.time) * 1000)
        data.append(request.length)
        payload.append(request.length - 42)
        
    average_rtt = sum(rtt) / len(rtt)
    request_throughput = sum(data) / sum(rtt)
    request_goodput = sum(payload) / sum(rtt)
    
    reply_delay = []
    for request, reply in zip(capture.lambda_filter(lambda cap: 'Echo (ping) request' in cap.info and ip == cap.destination).packets, capture.lambda_filter(lambda cap: 'Echo (ping) reply' in cap.info and ip == cap.source).packets):
        reply_delay.append((reply.time - request.time) * 1000)
    
    average_reply_delay = sum(reply_delay) / len(reply_delay)
    
    print(average_rtt, request_throughput, request_goodput, average_reply_delay)
    
    print()
    
    

    

def compute(node1, node2, node3, node4) :
	compute_metrics(node1, '192.168.100.1')
	compute_metrics(node2, '192.168.100.2')
	compute_metrics(node3, '192.168.200.1')
	compute_metrics(node4, '192.168.200.2')



