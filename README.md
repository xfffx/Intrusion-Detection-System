# Intrusion-Detection-System
Network Security IDS: Python-based system for detecting DDoS, PortScan, Web Attacks, etc. Combines traditional ML models with traffic analysis. Features: real-time detection, traffic visualization, multi-model support, attack categorization.
Requirements
Please make sure that you have the following requirements installed on your system:

Python (>= 3.7, lower 3.x versions may work but have not been tested)

Network interface monitoring permissions (requires admin/root privileges for traffic capture)

Additional Tools
Wireshark (for Windows/Linux)

CICFlowMeter (for feature extraction)

Installation
First clone the project.

bash
git clone https://github.com/yourusername/Intrusion-Detection-System.git
cd Intrusion-Detection-System
We recommend that you install the Python packages in a virtual environment. See the next section for how to do this, and then proceed with the rest of this section afterwards.

bash
pip install -r requirements.txt
Install Additional Tools
Windows:

Download and install Wireshark from https://www.wireshark.org/

Ensure Wireshark's tshark.exe is in your system PATH

Download CICFlowMeter from https://github.com/ahlashkari/CICFlowMeter

Place CICFlowMeter in the network sniffer/CICFlowMeter/ directory

Linux:

bash
sudo apt-get install wireshark tshark
# Then download CICFlowMeter as above
Virtual Environment (optional)
A virtual environment helps you to avoid that Python packages in this project do not conflict with other Python packages in your system.

bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# On Windows:
env\Scripts\activate
# On Linux/Mac:
source env/bin/activate

# Install requirements in the virtual environment
pip install -r requirements.txt

# Deactivate virtual environment when done
deactivate
Project Structure
text
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
├── requirements.txt         # Python dependencies
├── README.md               # This documentation
└── LICENSE                 # MIT License
Usage
Running the Application
With GUI (Recommended):

bash
python main.py
Command Line Tools:

Capture traffic and convert to features:

bash
python network_sniffer/pcap.py
Convert PCAP to CSV features:

bash
python network_sniffer/pcaptocsv.py
Run Decision Tree detection:

bash
python model/DecisionTree-main.py
Run Multi-Stage detection:

bash
python model/Multi-Stage-main.py
GUI Instructions
Start Detection: Click to begin real-time traffic monitoring

Select File: Upload a PCAP file for analysis

Model Selection: Choose between Decision Tree or Multi-Stage detection (from menu)

View Results: See detected attacks in the table

Visualization: Switch to visualization tab for attack statistics

Logs: View historical detection results

Supported Attack Types
BENIGN (Normal traffic)

Bot, DDoS, PortScan

DoS variants (GoldenEye, Hulk, slowloris, Slowhttptest)

FTP-Patator, SSH-Patator

Web Attacks (Brute Force, SQL Injection, XSS)

Heartbleed, Infiltration

Models
The system includes two main detection models:

Decision Tree Model: Traditional ML model trained on CICIDS2017 dataset

Multi-Stage Model: Advanced detection with zero-day attack identification

Notes
Requires administrator/root privileges for traffic capture

Models are pre-trained on CICIDS2017 dataset

Performance may vary in different network environments

Logs are automatically saved in the data/logs/ directory
