from scapy.all import *
import subprocess
import csv

    # 开始捕获网络流量
# packets = rdpcap('capture.pcap')  # 如果已经有一个PCAP文件，可以这样读取
    # 或者使用sniff函数捕获新的流量
# packets = sniff(count=10)  # 捕获10个数据包

timeout = 5#读取20秒的数据包，数字以秒为单位
packets = sniff(timeout=timeout)
    # 将捕获的数据包写入PCAP文件
wrpcap('output.pcap', packets)

# tshark的路径，确保这个路径是正确的
tshark_path = r'D:\jdk\Wireshark\tshark.exe'

# pcap文件的路径
pcap_file = 'output.pcap'

# 输出的csv文件的路径
csv_file = 'output.csv'

# 定义您想要的字段列表，包括列名
# 注意：这里需要根据实际的协议和字段来调整字段名
fields = [
    'frame.number',
    '-e', 'ip.src',
    '-e', 'ip.dst',
    '-e', 'tcp.srcport',
    '-e', 'tcp.dstport',
    '-e','frame.time_relative',
    '-e','ip.proto',
    '-e','ip.ttl',

    '-e','frame.time_delta',
    '-e','tcp.len',
    '-e','icmp','-e','udp','-e','tcp.analysis.flags',
    '-e','openflow_v4.type','-e','openflow_v4.length',
    '-E','occurrence=f'

    #id	dur	proto	service	state	spkts	dpkts	sbytes	dbytes
    # rate	sttl	dttl	sload	dload	sloss	dloss	sinpkt	dinpkt
    # sjit	djit	swin	stcpb	dtcpb	dwin	tcprtt	synack	ackdat
    # smean	dmean	trans_depth	response_body_len	ct_srv_src	ct_state_ttl
    # ct_dst_ltm	ct_src_dport_ltm	ct_dst_sport_ltm	ct_dst_src_ltm
    # is_ftp_login	ct_ftp_cmd	ct_flw_http_mthd	ct_src_ltm	ct_srv_dst
    # is_sm_ips_ports	attack_cat	label


    #以下字段的数据无法通过tshark直接得到
    # '-e','service',
    # '-e','state',
    # '-e','spkts',
    # '-e','dpkts',
    # '-e','sbytes',
    # '-e','dbytes',
    # '-e','rate',
    # '-e','sttl',
    # '-e','dttl',
    # '-e','sload'
    #service	state	spkts	dpkts	sbytes	dbytes	rate
    #sttl	dttl	sload	dload	sloss	dloss	sinpkt	dinpkt	sjit	djit	swin

    # ... 其他您需要的字段
    # 自定义字段或需要解析的协议字段可能需要额外的处理
]

# 构建完整的tshark命令
tshark_cmd = [
    tshark_path,
    '-r', pcap_file,
    '-T', 'fields',
    '-E', 'separator=,',  # 设置字段分隔符为逗号
    '-E', 'quote=d',  # 设置字段引用字符为双引号
    '-E', 'header=y',  # 包含列标题
    '-e', *fields  # 指定要输出的字段
]

# tshark命令列表，用于将pcap文件转换为csv
# 注意：这里使用的字段(-e)应该根据你的pcap文件内容进行调整
# tshark_cmd = [
#     tshark_path,
#     '-r', pcap_file,
#     '-T', 'fields',
#     '-E', 'separator=,',  # 设置字段分隔符为逗号
#     '-E', 'quote=d',  # 设置字段引用字符为双引号
#     '-e', 'frame.number',
#     '-e', 'frame.time_relative',
#     '-e', 'ip.src',
#     '-e', 'ip.dst',
#     '-e', 'tcp.srcport',
#     '-e', 'tcp.dstport',
#     # 添加你需要的其他字段...
#     #'>', csv_file  # 将输出重定向到csv文件
# ]

# 使用subprocess运行tshark命令，并将输出重定向到csv文件
try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as f_output:
        completed_process = subprocess.run(tshark_cmd, stdout=f_output, stderr=subprocess.PIPE)

        # 检查stderr是否有输出
        stderr_data = completed_process.stderr
        if stderr_data:
            print(f"Error occurred: {stderr_data.decode()}")
except Exception as e:
    print(f"An error occurred: {e}")

print(f"Conversion to CSV completed. File saved as {csv_file}")


###含有字段
# # tshark命令列表，用于将pcap文件转换为csv，并包含所需的字段
# # 请注意，字段的顺序和名称应与您想要的一致
# tshark_fields = [
#     'frame.number',
#     'frame.time_relative',
#     'ip.proto',
#     # ... 其他您需要的字段，比如服务、状态等，您可能需要自定义这些字段或使用tshark的显示过滤器
#     # 对于自定义字段或需要解析的协议字段，您可能需要编写额外的解析逻辑或使用tshark的显示过滤器功能
# ]
## 构建完整的tshark命令
# tshark_cmd = [
#                  tshark_path,
#                  '-r', pcap_file,
#                  '-T', 'fields',
#                  '-E', 'separator=,',  # 设置字段分隔符为逗号
#                  '-E', 'quote=d',  # 设置字段引用字符为双引号
#                  '-E', 'header=y',  # 包含列标题
#              ] + tshark_fields
#
# # 使用subprocess运行tshark命令，并将输出重定向到csv文件
# try:
#     with open(csv_file, 'w', newline='', encoding='utf-8') as f_output:
#         completed_process = subprocess.run(tshark_cmd, stdout=f_output, stderr=subprocess.PIPE)
#
#         # 检查stderr是否有输出
#         stderr_data = completed_process.stderr
#         if stderr_data:
#             print(f"Error occurred: {stderr_data.decode()}")
# except Exception as e:
#     print(f"An error occurred: {e}")
#
# print(f"Conversion to CSV completed. File saved as {csv_file}")