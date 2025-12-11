# Intrusion-Detection-System
Network Security IDS: Python-based system for detecting DDoS, PortScan, Web Attacks, etc. Combines traditional ML models with traffic analysis. Features: real-time detection, traffic visualization, multi-model support, attack categorization.

# Requirements
Please make sure that you have the following requirements installed on your system:

Python (>= 3.7, lower 3.x versions may work but have not been tested)

Network interface monitoring permissions (requires admin/root privileges for traffic capture)

# Installation
First clone the project.

```
git clone https://github.com/xfffx/Intrusion-Detection-System.git
cd Intrusion-Detection-System
```
After cloning the project, download CICFlowMeter to the network sniffer/ directory. Refer to [the CSDN tutorial](https://blog.csdn.net/weixin_35757704/article/details/144826273)  for detailed download and configuration instructions.


# Project Structure
```
Intrusion-Detection-System/
├── data/                    # Data storage
│   ├── output.pcap          # Captured traffic
│   ├── attack.csv           # Detection results
│   └── logs/                # Historical logs
├── model/                   # ML models and training scripts
│   ├── DecisionTree-main.py
│   ├── Multi-Stage-main.py
│   └── trained_models/      # Pre-trained models
├── network sniffer/         # Traffic capture and processing
│   ├── pcap.py
│   ├── pcaptocsv.py
│   ├── wireshark.py
│   ├── ip_proto.py
│   ├── sniffer.py
│   └── CICFlowMeter/        # Feature extractor
├── interface/               # GUI application
│   └── main.py
└──README.md               # This documentation
```
# Usage
```
python main.py
```
# GUI Instructions
Start Detection: Click to begin real-time traffic monitoring

Select File: Upload a PCAP file for analysis

Model Selection: Choose between Decision Tree or Multi-Stage detection (from menu)

View Results: See detected attacks in the table

Visualization: Switch to visualization tab for attack statistics

Logs: View historical detection results

# Supported Attack Types
BENIGN (Normal traffic)

Bot, DDoS, PortScan

DoS variants (GoldenEye, Hulk, slowloris, Slowhttptest)

FTP-Patator, SSH-Patator

Web Attacks (Brute Force, SQL Injection, XSS)

Heartbleed, Infiltration

# Models
The system includes two main detection models:

Decision Tree Model: Traditional ML model trained on CICIDS2017 dataset

Multi-Stage Model: Advanced detection with zero-day attack identification

# Notes
Requires administrator/root privileges for traffic capture

Models are pre-trained on CICIDS2017 dataset

Performance may vary in different network environments

Logs are automatically saved in the data/logs/ directory
