class Packet:
    def __init__(self, raw_packet):
        self.raw_packet = raw_packet
        self.parse()
    
    def parse(self):
        self.header, self.raw = self.raw_packet.split('\n\n')
        header = self.header.split('\n')[1].strip()
        while '  ' in header:
            header = header.replace('  ', ' ')
        self.packet_no, self.time, self.source, self.destination, self.protocol, self.length, self.info = header.split(' ', 6)
        self.packet_no = int(self.packet_no)
        self.time = float(self.time)
        self.length = int(self.length)
    
    def __str__(self):
        return f'Packet({self.packet_no}, {self.time}, {self.source}, {self.destination}, {self.protocol}, {self.length}, {self.info})'

    def __repr__(self):
        return str(self)


class PacketCapture:
    def __init__(self, *files, packets=None):
        self.files = files
        if packets is None:
            self.packets = []
            self.read_files()
        else:
            self.packets = packets
    
    def read_files(self):
        for file in self.files:
            with open(file) as capture:
                raw_file = capture.read()
            raw_file = raw_file.split('\n\n')
            for header, raw in zip(raw_file[::2], raw_file[1::2]):
                self.packets.append(Packet('\n\n'.join((header, raw))))
        
    def __len__(self):
        return len(self.packets)
    
    def filter(self, output=None, **kwargs):
        packets = []
        for packet in self.packets:
            for arg, value in kwargs.items():
                if packet.__dict__[arg] == value:
                    packets.append(packet)
                    break
        if output is not None:
            with open(output, 'w') as file:
                for packet in packets:
                    file.write(f'{packet.raw_packet}\n\n')
        return PacketCapture(packets=packets)
    
    def lambda_filter(self, function, output=None):
        packets = []
        for packet in self.packets:
            if function(packet):
                packets.append(packet)
        if output is not None:
            with open(output, 'w') as file:
                for packet in packets:
                    file.write(f'{packet.raw_packet}\n\n')
        return PacketCapture(packets=packets)


if __name__ == '__main__':
    capture = PacketCapture('Captures/Node1.txt')
    print(len(capture.filter(protocol='ICMP', output='test.txt')))
    print(len(capture.lambda_filter(lambda x: x.protocol == 'ICMP')))