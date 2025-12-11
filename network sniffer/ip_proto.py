import csv

# 定义一个协议编号到协议名称的映射字典
protocol_map = {
    1: 'ICMP',
    2: 'IGMP',
    4: 'IPIP',
    5: 'ST',
    6: 'TCP',
    8: 'EGP',
    9: 'IGP',
    12: 'PUP',
    17: 'UDP',
    22: 'XNS-TDP',
    27: 'RDP',
    36: 'IPPI',
    41: 'IPv6',
    47: 'GRE',
    50: 'ESP',
    51: 'AH',
    88: 'ICOMP',
    89: 'SNMP',
    94: 'PLS-in-IP-ESP',
    98: 'IPSEC-ESP',
    103: 'PIM',
    108: 'L2TP',
    115: 'MOBILE-IP',
    118: 'ISIS over IPv4',
    132: 'SCTP',
    135: 'UDPLite',
    136: 'MPLS-in-UDP'
    # ... 其他协议映射 ...
}

# 假设你有一个 CSV 文件，其中包含 tshark 输出的 ip.proto 值
input_csv = 'output.csv'
output_csv = 'output1.csv'

# 读取 CSV 文件并映射协议编号
with open(input_csv, mode='r', newline='') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过标题行（如果存在的话）
    with open(output_csv, mode='w', newline='') as output_file:
        writer = csv.writer(output_file)
        for row in reader:
            try:
                proto_number = int(row[2])  # 假设 ip.proto 值在 CSV 文件的第三列
                protocol_name = protocol_map.get(proto_number, 'Unknown')
                writer.writerow([protocol_name])
            except ValueError as e:
                print(f"Error converting ip.proto to int: {e}")
                print(f"Row contents: {row}")
                # 可以选择跳过这一行，或者进行其他错误处理