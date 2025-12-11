# from scapy.all import *
# import os
#
# timeout = 60#读取数据包，数字以秒为单位
# packets = sniff(timeout=timeout)
# # packets = sniff(count=30)  # 捕获10个数据包
#     # 将捕获的数据包写入PCAP文件
# wrpcap('../data/output.pcap', packets)
# #pcap文件转换为csv文件
# current_path = os.getcwd() #不能有中文路径
# pcap_file = os.path.join(current_path,'../data/output.pcap')
# csv_dir = os.path.join(current_path,'../data')
# cic_dir = os.path.join(current_path,'../network sniffer/CICFlowMeter/bin')
# os.chdir(cic_dir)
# os.system(f'call cfm.bat "{pcap_file}" "{csv_dir}"')


# from scapy.all import sniff
#
#
# # 抓取所有接口的包
# def sniff_all_interfaces(packet_count):
#     packets = sniff(count=packet_count, iface=None)
#     return packets
#
#
# # 使用示例
# packets = sniff_all_interfaces(10)  # 抓取10个包
# for packet in packets:
#     print(packet.show())


from scapy.all import *
import os
print("开始捕获")
# timeout = 10#读取数据包，数字以秒为单位
# packets = sniff(timeout=timeout, filter="")
packets = sniff(count=200)  # 捕获10个数据包
    # 将捕获的数据包写入PCAP文件
print(packets)
wrpcap('../data/output.pcap', packets)
print("捕获到pcap流量包")
# pcap文件转换为csv文件
current_path = os.getcwd() #不能有中文路径
pcap_file = os.path.join(current_path,'../data/output.pcap')
csv_dir = os.path.join(current_path,'../data')
cic_dir = os.path.join(current_path,'../network sniffer/CICFlowMeter/bin')
# cic_dir = os.path.join(current_path,'CICFlowMeter/bin')
os.chdir(cic_dir)
os.system(f'call cfm.bat "{pcap_file}" "{csv_dir}"')
