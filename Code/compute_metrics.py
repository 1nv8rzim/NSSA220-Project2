def compute_metrics(capture, ip):
    request_sent = len(capture.lambda_filter(lambda cap: cap.source == ip and 'Echo (ping) request' in cap.info))
    request_recv = len(capture.lambda_filter(lambda cap: cap.destination == ip and 'Echo (ping) request' in cap.info))
    reply_sent = len(capture.lambda_filter(lambda cap: cap.source == ip and 'Echo (ping) reply' in cap.info))
    reply_recv = len(capture.lambda_filter(lambda cap: cap.destination == ip and 'Echo (ping) reply' in cap.info))
    
    request_bytes_sent = sum(packet.length for packet in capture.lambda_filter(lambda cap: cap.source == ip and 'Echo (ping) request' in cap.info).packets)
    request_bytes_recv = sum(packet.length for packet in capture.lambda_filter(lambda cap: cap.destination == ip and 'Echo (ping) request' in cap.info).packets)
    request_bytes_data_sent = sum(packet.length - 42 for packet in capture.lambda_filter(lambda cap: cap.source == ip and 'Echo (ping) request' in cap.info).packets)
    request_bytes_data_recv = sum(packet.length - 42 for packet in capture.lambda_filter(lambda cap: cap.destination == ip and 'Echo (ping) request' in cap.info).packets)
        
    rtt, data, payload = [], [], []
    for request, reply in zip(capture.lambda_filter(lambda cap: 'Echo (ping) request' in cap.info and ip == cap.source).packets, capture.lambda_filter(lambda cap: 'Echo (ping) reply' in cap.info and ip == cap.destination).packets):
        rtt.append((reply.time - request.time) * 1000)
        data.append(request.length)
        payload.append(request.length - 42)
        
    average_rtt = round(sum(rtt) / len(rtt), 2)
    request_throughput = round(sum(data) / sum(rtt), 1)
    request_goodput = round(sum(payload) / sum(rtt), 1)
    
    reply_delay = []
    for request, reply in zip(capture.lambda_filter(lambda cap: 'Echo (ping) request' in cap.info and ip == cap.destination).packets, capture.lambda_filter(lambda cap: 'Echo (ping) reply' in cap.info and ip == cap.source).packets):
        reply_delay.append((reply.time - request.time) * 1000)
    
    average_reply_delay = round(1000 * sum(reply_delay) / len(reply_delay), 2)
        
    hops = []
    for reply in capture.lambda_filter(lambda cap: 'Echo (ping) reply' in cap.info and ip == cap.destination).packets:
        hops.append(128 - int(reply.info.split('ttl=')[1].split(' (')[0]) + 1)
        
    average_hop_count = round(sum(hops) / len(hops), 2)
    print(f'Echo Requests Sent\t\t\t{request_sent}')
    print(f'Echo Requests Received\t\t\t{request_recv}')
    print(f'Echo Replies Sent\t\t\t{reply_sent}')
    print(f'Echo Replies Received\t\t\t{reply_recv}')
    print(f'Echo Request Bytes Sent\t\t\t{request_bytes_sent}')
    print(f'Echo Request Bytes Received\t\t{request_bytes_recv}')
    print(f'Echo Request Data Sent\t\t\t{request_bytes_data_sent}')
    print(f'Echo Request Data Received\t\t{request_bytes_data_recv}')
    print(f'Average RTT (ms)\t\t\t{average_rtt}')
    print(f'Echo Request Throughput (kB/sec)\t{request_throughput}')
    print(f'Echo Request Goodput (kB/sec)\t\t{request_goodput}')
    print(f'Average Reply Delay (us)\t\t{average_reply_delay}')
    print(f'Average Echo Request Hop Count\t\t{average_hop_count}')
    print()
    

def compute(node1, node2, node3, node4) :
    print('=================== Node 1 ===================')
    compute_metrics(node1, '192.168.100.1')
    print('=================== Node 2 ===================')
    compute_metrics(node2, '192.168.100.2')
    print('=================== Node 3 ===================')
    compute_metrics(node3, '192.168.200.1')
    print('=================== Node 4 ===================')
    compute_metrics(node4, '192.168.200.2')



