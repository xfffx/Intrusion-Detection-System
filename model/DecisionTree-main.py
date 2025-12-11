from joblib import dump, load
import pandas as pd
import numpy as np
from keras.models import load_model  # 确保您已经安装了 Keras
from sklearn.preprocessing import StandardScaler
import os

if __name__ == '__main__':
    # print(np.__version__)
    model = load('../model/Decision_model.joblib')
    #pcap转换为csv文件的编码方式是GB2312
    # test = pd.read_csv('../data/output.pcap_Flow.csv', header=None)#这里读取什么名字
    test = pd.read_csv('../data/output.pcap_Flow.csv', header=None, encoding='GB2312')
    # print(test)
    # test = test.drop(test.index[0])  # 删除第一行列名
    # print(test.info())
    # print(test.shape)

    # test = test.astype(float) #转换为float
    test = test.drop(test.index[0])#删除第一行的列名
    test = test.drop(83,axis=1)

    # test.dropna(inplace=True) #删除有缺失值的行
    # rows_with_inf = test[(test == np.inf) | (test == -np.inf)].any(axis=1)
    # test.drop(test[rows_with_inf].index,inplace=True)#删除有无穷大值的行

    # print(test.columns)
    # #不确定列名前有没有空格
    # cleaned_columns = [col.strip() for col in test.columns]
    # test.columns = cleaned_columns
    # print(test.columns)
    Dtest = test.drop(0,axis=1)
    Dtest = Dtest.drop(1,axis=1)
    Dtest = Dtest.drop(2,axis=1)
    Dtest = Dtest.drop(3,axis=1)
    Dtest = Dtest.drop(5,axis=1)
    Dtest = Dtest.drop(6,axis=1)
    Dtest = Dtest.astype(float)

    # 删除 Dtest 中的缺失值和无穷大值
    Dtest.dropna(inplace=True)
    rows_with_inf = Dtest[(Dtest == np.inf) | (Dtest == -np.inf)].any(axis=1)
    Dtest.drop(Dtest[rows_with_inf].index, inplace=True)
    # 现在，使用 Dtest 的索引来过滤 test
    # 注意：这里假设 test 的索引与 Dtest 的索引是相同的
    # 如果索引不同，你需要先确保它们的索引相同，或者使用其他方法来匹配行
    filtered_index = Dtest.index
    test = test.loc[filtered_index]

    Dtest.insert(loc=55, column='61', value=Dtest[40])
    # Dtest = Dtest.drop(Dtest.index[0])
    # print(Dtest.info())
    pred = model.predict(Dtest) #此处的数据要和模型训练的输入格式一样
    print(pred)
    class_names=['BENIGN', 'Bot', 'DDoS', 'DoS GoldenEye', 'DoS Hulk',
       'DoS Slowhttptest', 'DoS slowloris', 'FTP-Patator', 'Heartbleed',
       'Infiltration', 'PortScan', 'SSH-Patator', 'Web Attack Brute Force',
       'Web Attack Sql Injection', 'Web Attack XSS']
    prediction = [class_names[i] for i in pred]
    # print(prediction) #输出预测的结果————模型精度高，但是还是预测有较多错误，良性数据过多导致精度虚高
    #将信息存储在attack.csv文件里
    # print(test.columns)
    df = pd.DataFrame(test.iloc[:, [1,2,3,4,5,6]])

    # i= len(prediction)
    # predictions = ['' for _ in range(i+1)]  # 初始化为空字符串的数组
    # while i>0:
    #     predictions[i]=prediction[i-1]
    #     i=i-1
    # predictions[0]='Predictions'

    # predictions = pd.Series(predictions)
    df.reset_index(drop=True, inplace=True)  # 重置df的索引
    df['7'] = prediction
    # print(df)
    # 将DataFrame保存到CSV文件，没有index，没有header
    df.to_csv('../data/attack.csv',mode='a', index=False, header=False, encoding='gb2312')



# if __name__ == '__main__':
#     print(np.__version__)
#     model = load('Decision_model02.joblib')
#     test = pd.read_csv('../data/decision的表格格式.csv', header=None)#这里读取什么名字
#     test = test.drop(test.index[0])  # 删除第一行列名
#     print(test.info())
#     print(test.shape)
#
#     test = test.astype(float)
#     # 删除包含 NaN 的列
#     test.dropna(inplace=True)
#     # 删除包含无穷大值的行
#     rows_with_inf = test[(test == np.inf) | (test == -np.inf)].any(axis=1)
#     test.drop(test[rows_with_inf].index,inplace=True)
#     pred = model.predict(test)
#     class_names=['BENIGN', 'Bot', 'DDoS', 'DoS GoldenEye', 'DoS Hulk',
#        'DoS Slowhttptest', 'DoS slowloris', 'FTP-Patator', 'Heartbleed',
#        'Infiltration', 'PortScan', 'SSH-Patator', 'Web Attack Brute Force',
#        'Web Attack Sql Injection', 'Web Attack XSS']
#     prediction = [class_names[i] for i in pred]
#     df = pd.DataFrame(prediction, columns=['Predictions'])
#     # 将DataFrame保存到CSV文件，没有index，没有header
#     df.to_csv('../data/predictions-decision.csv', index=False, header=False)
