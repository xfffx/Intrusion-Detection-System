import os
current_path = os.getcwd() #不能有中文路径
pcap_file = os.path.join(current_path,'../data/output.pcap')
csv_dir = os.path.join(current_path,'../data')
# cic_dir = os.path.join(current_path,'CICFlowMeter\\bin')
cic_dir = os.path.join(current_path,'D:\intrusion detection system\\network sniffer\CICFlowMeter\\bin')

os.chdir(cic_dir)
os.system(f'call cfm.bat "{pcap_file}" "{csv_dir}"')
