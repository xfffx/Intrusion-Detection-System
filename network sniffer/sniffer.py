import scapy.all as scapy
from scapy.layers import http
import csv

def sniffing(interface):
    scapy.sniff(iface = interface, store = False, prn = process_packet)

def process_packet(packet):
    print(packet.show())
    if packet.haslayer(http.HTTPRequest):
        print(packet[http.HTTPRequest].Host)

# def sniffing(interface):
#     # 创建一个CSV文件用于保存数据
#     with open('sniffed_data.csv', 'w', newline='') as csvfile:
#         # 创建CSV writer对象
#         writer = csv.writer(csvfile)
#         # 写入CSV文件的标题行
#         writer.writerow(['Packet Summary', 'Host'])
#         # 开始嗅探
#         scapy.sniff(iface=interface, store=False, prn=process_packet_with_csv)
#
# def process_packet_with_csv(packet):
#     # 打印包的信息
#     print(packet.show())
#     # 检查包是否包含HTTP请求层
#     if packet.haslayer(HTTPRequest):
#         # 获取主机名
#         host = packet[HTTPRequest].Host
#         # 打开（或重新打开）CSV文件以追加数据
#         with open('sniffed_data.csv', 'a', newline='') as csvfile:
#             writer = csv.writer(csvfile)
#             # 写入数据包概要和主机名
#             writer.writerow([packet.summary(), host])


