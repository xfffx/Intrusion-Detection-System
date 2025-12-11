import csv
import time

import numpy as np
import subprocess
import sys
import os
import shutil
import threading
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QFileDialog, \
    QMessageBox, \
    QMenuBar, QAction, QStackedWidget
from PyQt5.QtWidgets import QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtCore import QTimer
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
#拿到在另外一台计算机上执行程序代码所存储的文件路径。


#全局变量定义
select_pcap = 0#默认自动捕获流量
select_model = 0#默认决策树分类器模型
flag = True #停止执行的标志
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置窗口的窗体标题
        self.setWindowTitle('入侵检测系统')
        # 设置窗体的尺寸
        # self.resize(1228, 800)
        self.setFixedSize(1228, 800) #固定大小
        # 设置窗体的背景颜色
        # self.setStyleSheet("background-color: #fffff;")  # 这里以红色为例，你可以替换为你想要的颜色
        # 创建菜单栏
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('模型选择')
        menu_bar.setStyleSheet("QMenuBar { background-color: '#D4DBDF'; }")
        # file_menu.setStyleSheet("QMenu::item { font-size: 14pt; }")
        open_action1 = QAction('DesicionTree model',self)
        open_action1.triggered.connect(self.select_DecisionTree_mode)
        file_menu.addAction(open_action1)
        open_action2 = QAction('Multi-Stage detection', self)
        open_action2.triggered.connect(self.select_MutilSatge_model)
        file_menu.addAction(open_action2)
        file_menu = menu_bar.addMenu('界面切换')
        # file_menu = menu_bar.addMenu('文件')

        # 创建并设置中心部件
        # self.widget = MyWidget()
        # self.setCentralWidget(self.widget)
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.page1 = MyWidget()
        self.page2 = Page2()

        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)

        action_page1 = QAction('切换到检测界面', self)
        action_page1.triggered.connect(self.on_page1_triggered)
        file_menu.addAction(action_page1)

        action_page2 = QAction('切换到可视化界面', self)
        action_page2.triggered.connect(self.on_page2_triggered)
        file_menu.addAction(action_page2)

    def on_page1_triggered(self):
        self.stacked_widget.setCurrentIndex(0)

    def on_page2_triggered(self):
        self.stacked_widget.setCurrentIndex(1)

    def select_DecisionTree_mode(self):
        global select_model
        select_model = 0
    def select_MutilSatge_model(self):
        global select_model
        select_model = 1


class Page2(QWidget):
    import time
    def read_csv_file():
        global data
        while True:
            data = pd.read_csv('../data/attack.csv', encoding='gb2312')
            time.sleep(10)
    csv_thread = threading.Thread(target=read_csv_file)
    csv_thread.daemon = True  # 将线程设置为守护线程，以便程序退出时自动结束线程
    csv_thread.start()

    def __init__(self):
        global data
        super().__init__()
        # print(data)
        # 创建主布局
        self.main_layout = QHBoxLayout(self)

        # 创建饼图
        self.pie_fig = Figure()
        self.pie_ax = self.pie_fig.add_subplot(111, aspect='equal')  # 初始化 pie_ax
        self.pie_canvas = FigureCanvas(self.pie_fig)
        self.pie_chart_widget = QWidget()
        self.pie_chart_layout = QVBoxLayout(self.pie_chart_widget)
        self.pie_chart_layout.addWidget(self.pie_canvas)

        # 创建柱状图
        self.bar_fig = Figure()
        self.bar_ax = self.bar_fig.add_subplot(111)
        self.bar_canvas = FigureCanvas(self.bar_fig)
        self.bar_chart_widget = QWidget()
        self.bar_chart_layout = QVBoxLayout(self.bar_chart_widget)
        self.bar_canvas.resize(800, 600)  # 设置图形大小为800x600
        self.bar_chart_layout.addWidget(self.bar_canvas)
        # 将两个图表添加到主布局中
        self.main_layout.addWidget(self.bar_chart_widget)
        self.main_layout.addWidget(self.pie_chart_widget)
        # 初始化图表
        self.init_charts()

        # 启动定时器，每隔5秒更新一次图表
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_charts)
        self.timer.start(5000)  # 5000毫秒，即5秒

    def update_charts(self):
        self.show_pie_chart()
        self.show_bar_chart()

    def init_charts(self):
        # 初始化饼图
        self.show_pie_chart()
        # 初始化柱状图
        self.show_bar_chart()
    def show_pie_chart(self):
        global data
        # self.pie_ax = self.pie_fig.add_subplot(111, aspect='equal')
        self.pie_ax.clear()  # 清除旧图表
        column_data = data.iloc[:, 6]
        column_data = column_data[column_data != "BENIGN"]
        column_data = column_data[column_data != "Benign"]
        column_data = column_data[column_data != "Predictions"]
        labels, counts = np.unique(column_data, return_counts=True)
        colors = ['#c86f67', '#f1ccb8', '#b8d38f', '#ddff95', '#d9b8f1', '#b8f1ed', '#b8f1cc', '#c490a0',
                  '#ff8444']  # 根据类别数量自行设置颜色
        # 初始化饼图
        self.pie_fig = self.pie_canvas.figure
        # 绘制饼图
        self.pie_ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=180, colors=colors)
        ## 设置图例
# plt.legend(labels, bbox_to_anchor=(1.1, 1.05))
        self.pie_ax.legend(labels,bbox_to_anchor=(1.1,1.05))
        self.pie_ax.set_title("攻击类别占比", fontproperties='SimHei', fontsize=16)
        self.pie_canvas.draw()

    def show_bar_chart(self):
        global data
        self.bar_ax.clear()  # 清除旧图表
        # 删除第7列为 "benign" 的行
        data_filtered = data[data.iloc[:, 6] != "Benign"]
        data_filtered = data[data.iloc[:, 6] != "BENIGN"]
        # 统计剩余数据中每个 IP 出现的次数
        ip_counts = data_filtered.iloc[:, 0].value_counts()
        top_five_ips = ip_counts.head(5)
        # 调整柱状图的宽度和间距
        bar_width = 0.6  # 柱子的宽度
        bar_spacing = 0.1  # 柱子之间的间距
        self.bar_ax.bar(top_five_ips.index, top_five_ips.values, width=bar_width, align='center', alpha=0.7)
        self.bar_ax.set_xticklabels(top_five_ips.index, rotation=16, ha="right")
        self.bar_ax.set_xlabel("Source IP") #攻击性源IP显示
        self.bar_ax.set_ylabel("Count")
        self.bar_ax.set_title("攻击来源及数量", fontproperties='SimHei', fontsize=16)
        self.bar_canvas.draw()

class MyWidget(QWidget):
    def __init__(self):
        # 用super 继承父类的初始化
        super().__init__()
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()  # 得到屏幕中间的位置信息
        qr.moveCenter(cp)  # 让我们的窗体移动到屏幕中间
        self.initUI()


    def initUI(self):
        layout = QVBoxLayout()
        layout.addLayout(self.init_form())  # 上传文件
        layout.addLayout(self.init_header())
        layout.addLayout(self.init_table())
        layout.addLayout(self.init_footer())
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_table)
        self.timer.start(5000)  # 每5秒钟刷新一次

    def init_menu_bar(self):
        # 创建菜单栏
        menu_bar = QMenuBar()

        # 创建一个文件菜单
        file_menu = menu_bar.addMenu('文件')

        # 在文件菜单中添加一些动作
        open_action = QAction('打开', self)
        file_menu.addAction(open_action)

        save_action = QAction('保存', self)
        file_menu.addAction(save_action)

        exit_action = QAction('退出', self)
        exit_action.triggered.connect(self.close)  # 连接退出动作到窗口的关闭方法
        file_menu.addAction(exit_action)

        # 可以继续添加其他菜单和动作...

        return menu_bar

    def init_header(self):
        # 1.顶部菜单布局
        header_layout = QHBoxLayout()  # 创建顶部菜单布局
        # 1.1 放入按钮
        btn_start = QPushButton("开始检测")  # 新建一个开始按钮
        btn_start.setFixedSize(200, 50)
        btn_start.setStyleSheet("""  
            QPushButton {  
                background-color: #D4DBDF; /* 浅蓝背景 */  
                color: black; /* 黑色文本 */  
                border-width: 3px; /* 边框宽度 */  
                border-style: solid; /* 边框样式（实线） */  
                border-color: #D8D8D8; /* 边框颜色 */
            }  
            QPushButton:hover {  
                background-color: #FFFFFF; /* 鼠标悬停时的背景色 */  
            }  
        """)
        btn_start.clicked.connect(self.start_detection)
        header_layout.addWidget(btn_start)  # 将开始按钮添加到顶部菜单布局
        btn_stop = QPushButton("停止检测")  # 新建一个开始按钮
        btn_stop.setFixedSize(200, 50)
        btn_stop.setStyleSheet("""  
            QPushButton {  
                background-color: #D4DBDF; /* 浅蓝背景 */  
                color: black; /* 黑色文本 */  
                border-width: 2px; /* 边框宽度 */  
                border-style: solid; /* 边框样式（实线） */  
                border-color: #D8D8D8; /* 边框颜色 */
            }  
            QPushButton:hover {  
                background-color: #FFFFFF; /* 鼠标悬停时的背景色 */  
            }  
        """)
        btn_stop.clicked.connect(self.stop_detection)
        header_layout.addStretch(1)
        header_layout.addWidget(btn_stop)  # 将开始按钮添加到顶部菜单布局
        # 1.2 加入弹簧
        header_layout.addStretch()

        return header_layout
    def stop_detection(self):
        global flag
        flag = False #停止执行
        source_file = '../data/attack.csv' #每次停止检测都保存一次结果到日志里
        target_folder = '../data/logs'
        current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        target_file = os.path.join(target_folder, f'attack_{current_datetime}.csv')
        os.makedirs(target_folder, exist_ok=True)# 创建目标文件夹（如果不存在）
        shutil.copy(source_file, target_file)
        msg_box = QMessageBox.information(None, '提示', '检测停止！')

    def init_form(self):
        # 2.添加内容布局
        form_layout = QHBoxLayout()  # 创建添加内容布局

        # 2.1 输入框
        txt_asin = QLineEdit()  # 新建一个输入框对象
        txt_asin.setText("1、点击“开始检测”自动捕获流量  2、上传.pcap格式文件进行检测")  # 设置默认的form数据
        # txt_asin.setPlaceholderText("请输入商品ID和价格，例如：B0818JJQQ8=88")  # 设置灰色的提示信息
        form_layout.addWidget(txt_asin)  # 将输入框加入到布局中

        # 2.2 添加按钮
        # btn_add = QPushButton("上传文件")  # 新建一个添加按钮
        # form_layout.addWidget(btn_add)  # 将添加按钮添加到form布局
        self.setGeometry(100, 100, 400, 300)
        self.button = QPushButton('选择文件', self)
        form_layout.addWidget(self.button)  # 将添加按钮添加到form布局
        self.button.clicked.connect(self.selectFile)

        return form_layout

    def selectFile(self):
        global select_pcap
        select_pcap=1
        filename, _ = QFileDialog.getOpenFileName(self, '选择文件', '/path/to/your/project')
        if filename:
            #上传的文件保存到db文件夹中
            target_path = '../data'
            self.saveFile(filename, target_path)

    def saveFile(self, filename, target_path):
        basename = os.path.basename(filename)
        target_file = os.path.join(target_path, basename)
        try:
            shutil.copy2(filename, target_file)
            self.rename_file("../data/"+basename,"../data/output.pcap")
            QMessageBox.information(self, '上传成功', f'文件 "{basename}" 上传成功。')
        except Exception as e:
            QMessageBox.critical(self, '上传失败', f'上传文件 "{basename}" 时发生错误: {e}')

    def rename_file(self,old_file,new_file):
        shutil.move(old_file,new_file)

    def init_table(self):
        # 3.表格数据展示布局
        table_layout = QHBoxLayout()
        # 3.1 创建表格
        self.table_widget = QTableWidget(0, 7)  # 新建一个0行7列的表格
        table_header = [
            {"field": "asin", "text": "源IP", 'width': 200},
            {"field": "title", "text": "源端口", 'width': 120},
            {"field": "url", "text": "目标IP", 'width': 200},
            {"field": "price", "text": "目标端口", 'width': 120},
            {"field": "status", "text": "协议类型", 'width': 120},
            {"field": "frequency", "text": "发生时间", 'width': 250},
            {"field": "frequency", "text": "攻击类型", 'width': 150},
        ]
        for idx, info in enumerate(table_header):
            item = QTableWidgetItem()
            item.setText(info['text'])
            self.table_widget.setHorizontalHeaderItem(idx, item)
            self.table_widget.setColumnWidth(idx, info['width'])

        table_layout.addWidget(self.table_widget)  # 把表格添加到表格布局中
        return table_layout

    def update_table(self):
        # 读取 attack 文件内容，需要刷新多次自动
        file_path = os.path.join(BASE_DIR, "../data", "attack.csv")
        import csv

        try:
            with open(file_path, mode='r', encoding='gb2312', newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                try:
                    next(csvreader)  # 跳过标题行
                except StopIteration:
                    print("CSV 文件为空或只包含标题行")
                    data_list = []
                else:
                    data_list = list(csvreader)
        except FileNotFoundError:
            print("找不到文件")

        self.table_widget.setRowCount(0)  # 清空表格内容

        for row_list in data_list:  # 每有一行json数据，我们就需要遍历一轮增加一行数据
            current_row_count = self.table_widget.rowCount()  # 当前表格有多少行
            self.table_widget.insertRow(current_row_count)  # 增加一行
            for i, ele in enumerate(row_list):  # enumerate中 i表示索引id，ele表示数据值
                cell = QTableWidgetItem(str(ele))  # 注意我们的数据格式转为str，比如说状态的数据可能本身是int类型
                self.table_widget.setItem(current_row_count, i, cell)  # 写入数据到指定单元格

    def clear_file(self):
        #清空之前先保存文件到日志里 清空好像不用保存，停止检测的时候保存就可以
        source_file = '../data/attack.csv'
        # 读取第一行数据
        with open(source_file, 'r') as file:
            first_line = file.readline()

        # 清空文件内容并写入第一行数据
        with open(source_file, 'w') as file:
            file.write(first_line)
        # 提示用户文件已清空
        msg_box = QMessageBox.information(None, '提示', '检测结果已经清空！')

    def init_footer(self):
        # 4.底部菜单
        footer_layout = QHBoxLayout()

        # label_status = QLabel("未检测", self)
        # footer_layout.addWidget(label_status)

        footer_layout.addStretch()  # 添加弹簧，更加美观

        # btn_reset = QPushButton("重新检测")
        # footer_layout.addWidget(btn_reset)

        btn_reset_count = QPushButton("清空检测结果")
        footer_layout.addWidget(btn_reset_count)
        btn_reset_count.clicked.connect(self.clear_file)

        btn_recheck = QPushButton("查看日志")
        footer_layout.addWidget(btn_recheck)
        btn_recheck.clicked.connect(self.show_logs)
        ###弹出文件管理器窗口，按照时间保存之前的json文件
        #日志要怎么保存呢，按照检测的次数，结束检测的时候存储一下，清空检测结果的时候保存一次

        # btn_delete = QPushButton("删除检测项")
        # footer_layout.addWidget(btn_delete)
        #
        # btn_alert = QPushButton("SMTP报警配置")
        # footer_layout.addWidget(btn_alert)
        #
        # btn_proxy = QPushButton("代理IP")
        # footer_layout.addWidget(btn_proxy)

        return footer_layout

    def show_logs(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))#获取绝对路径
        logs_path = os.path.join(script_dir, "../data/logs")
        logs_path = os.path.normpath(logs_path)
        if os.path.isdir(logs_path):#检查文件夹是否存在
            subprocess.Popen(f'explorer "{logs_path}"')
        else:
            print(f"The logs directory does not exist at: {logs_path}")

    def start_detection(self):
        global flag
        global select_pcap
        global select_model
        flag = True
        if select_pcap==1:
            try:
                pcaptocsv_thread = threading.Thread(target=self.pcaptocsv)  # pcap文件转换为csv文件
                pcaptocsv_thread.start()
                if select_model == 1 and flag:
                    MutilStage_thread = threading.Thread(target=self.MutilStage)
                    MutilStage_thread.start()
                elif select_model == 0 and flag:
                    DecisionTree_thread = threading.Thread(target=self.DecisionTree)
                    DecisionTree_thread.start()
                select_pcap=0
            except Exception as e:
                print("An error occurred:", e)
        elif select_pcap==0:#自动捕获       #只捕获了一次流量包,怎么能一直捕获流量包呢但是没有一直捕获流量包
            # while flag:
            #     if select_model == 1:
            #         pcap_thread = threading.Thread(target=self.pcap_and_MutilStage)  # 创建一个线程同时执行pcap和MutilStage
            #     elif select_model == 0:
            #         pcap_thread = threading.Thread(target=self.pcap_and_DecisionTree)  # 创建一个线程同时执行pcap和DecisionTree
            #     pcap_thread.start()
            #     pcap_thread.join()
            if select_model == 1:
                pcap_thread = threading.Thread(target=self.pcap_and_MutilStage)  # 创建一个线程同时执行pcap和MutilStage
            elif select_model == 0:
                pcap_thread = threading.Thread(target=self.pcap_and_DecisionTree)  # 创建一个线程同时执行pcap和DecisionTree
            pcap_thread.start()

            # if select_model == 1:
            #     pcap_thread = threading.Thread(target=self.pcap)  # 先捕获pcap包直接转换为csv文件
            #     pcap_thread.start()
            #     time.sleep(10)
            #     # print('pacp.py执行完毕')
            #     MutilStage_thread = threading.Thread(target=self.MutilStage)  # 然后检测
            #     MutilStage_thread.start()
            # elif select_model == 0:
            #     pcap_thread = threading.Thread(target=self.pcap)
            #     pcap_thread.start()
            #     time.sleep(10)
            #     # print('pacp.py执行完毕')
            #     DecisionTree_thread = threading.Thread(target=self.DecisionTree)
            #     DecisionTree_thread.start()
    def pcap_and_MutilStage(self):
        pcap_thread = threading.Thread(target=self.pcap)  # 创建一个线程执行pcap
        pcap_thread.start()
        if pcap_thread.is_alive():  # 检查线程是否已经开始执行
            pcap_thread.join()  # 等待pcap_thread线程执行完毕
            print('pcap线程开始执行')
        self.MutilStage()  # 执行MutilStage

    def pcap_and_DecisionTree(self):
        pcap_thread = threading.Thread(target=self.pcap)  # 创建一个线程执行pcap
        pcap_thread.start()
        if pcap_thread.is_alive():  # 检查线程是否已经开始执行
            pcap_thread.join()  # 等待pcap_thread线程执行完毕
            print('pcap线程开始执行')
        self.DecisionTree()  # 执行DecisionTree

    def pcaptocsv(self):
        subprocess.call(['python', '../network sniffer/pcaptocsv.py'])
    def pcap(self):
        print('调用了pcap脚本')
        subprocess.call(['python', '../network sniffer/pcap.py'])

    def MutilStage(self):
        subprocess.call(['python','../model/Multi-Stage-main.py'])
    def DecisionTree(self):
        subprocess.call(['python', '../model/DecisionTree-main.py'])
if __name__ == '__main__':
    # 清空attack文件内容
    # file_path = '../data/attack.csv'
    # with open(file_path, 'w', newline='', encoding='gb2312') as file:
    #     pass
    # data_row = ['1', '2', '3','4','5','6','7']
    # with open(file_path, 'a', newline='', encoding='gb2312') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(data_row)
    # print(data)
    app = QApplication(sys.argv)  # 实例化一个Application应用，所有的窗口均在其下运行
    window = MainWindow()  # 实例化窗口对象
    window.show()  # 窗口展示
    sys.exit(app.exec_())
