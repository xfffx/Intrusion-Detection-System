#注意scikit-learn版本必须是1.1.1

# Seed value
seed_value= 42

# 1. Set the `PYTHONHASHSEED` environment variable at a fixed value
import os
os.environ['PYTHONHASHSEED']=str(seed_value)

# 2. Set the `python` built-in pseudo-random generator at a fixed value
import random
random.seed(seed_value)

# 3. Set the `numpy` pseudo-random generator at a fixed value
import numpy as np
np.random.seed(seed_value)

import pandas as pd
from sklearn.preprocessing import QuantileTransformer
from sklearn.metrics import auc, roc_curve, accuracy_score, balanced_accuracy_score, f1_score, recall_score, confusion_matrix, classification_report
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.svm import OneClassSVM
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from tensorflow import keras

# test = pd.read_parquet("CIC/test.parquet/")
# print('mutil的当前路径',os.getcwd())
test = pd.read_csv("../data/output.pcap_Flow.csv", header=None, encoding='GB2312')
# print(test.shape)
# y = test["Y"].replace(["Heartbleed", "Infiltration"], "Unknown")
# x = test.drop(columns=['Y'])
# print(y.value_counts())
x = test.drop(0,axis=1)
x = x.drop(1,axis=1)
x = x.drop(2,axis=1)
x = x.drop(3,axis=1)
x = x.drop(4,axis=1)
x = x.drop(6,axis=1)
x = x.drop(37,axis=1)
x = x.drop(38,axis=1)
x = x.drop(39,axis=1)
x = x.drop(55,axis=1)
x = x.drop(61,axis=1)
x = x.drop(62,axis=1)
x = x.drop(63,axis=1)
x = x.drop(64,axis=1)
x = x.drop(65,axis=1)
x = x.drop(66,axis=1)
x = x.drop(83,axis=1)
# print(x.columns)
x = x.drop(x.index[0])#删除第1行的列名
x = x.astype(float)
# 删除 x 中的缺失值和无穷大值
x.dropna(inplace=True)
rows_with_inf = x[(x == np.inf) | (x == -np.inf)].any(axis=1)
x.drop(x[rows_with_inf].index, inplace=True)
filtered_index = x.index
filtered_index = filtered_index.drop_duplicates()#删除重复值
newtest = test.loc[filtered_index]

#调用脚本的时候路径是D:\intrusion detection system\interface
f = open("../model/stage1_ocsvm.p","rb")
stage1 = pickle.load(f)
f.close()
f = open("../model/stage2_rf.p","rb")
stage2 = pickle.load(f)
f.close()
# Individual feature scalers and classification models
f = open("../model/stage1_ocsvm_model.p","rb")
stage1_model = pickle.load(f)
f.close()
f = open("../model/stage1_ocsvm_scaler.p","rb")
stage1_scaler = pickle.load(f)
f.close()
f = open("../model/stage2_rf_model.p","rb")
stage2_model = pickle.load(f)
f.close()
f = open("../model/stage2_rf_scaler.p","rb")
stage2_scaler = pickle.load(f)
f.close()
# RF baseline model and feature scaler
f = open("../model/baseline_rf.p","rb")
baseline_rf = pickle.load(f)
f.close()
f = open("../model/baseline_rf_scaler.p","rb")
baseline_rf_scaler = pickle.load(f)
f.close()
# print("11") 应该是可以导入的
# Optimized models for Bovenzi et al.
sota_stage1 = keras.models.load_model("../model/sota_stage1.h5")
f = open("../model/sota_stage2.p","rb")
sota_stage2 = pickle.load(f)
f.close()

tau_m = 0.98
tau_u = 0.0040588613744241275
# tau_u = 0.006590265510403005
tau_b = -0.0002196942507948895
#阶段1：二分类为攻击和非攻击
proba_1 = -stage1.decision_function(x)
# print(proba_1)
pred_1 = np.where(proba_1 < tau_b, "Benign", "Attack").astype(object)
np.unique(pred_1, return_counts=True)
#阶段2：划分攻击类别
filtered_x = x[pred_1 == "Attack"]
if filtered_x.shape[0] > 0:
    proba_2 = stage2.predict_proba(filtered_x)
    pred_2 = np.where(
        np.max(proba_2, axis=1) > tau_m,
        stage2.classes_[np.argmax(proba_2, axis=1)],
        "Unknown")
    np.unique(pred_2, return_counts=True)
else:
    print("No samples labeled as 'Attack' found.")
#阶段3：零日攻击
if filtered_x.shape[0] > 0:
    proba_3 = proba_1[pred_1 == "Attack"][pred_2 == "Unknown"]
    pred_3 = np.where(proba_3 < tau_u, "Benign", "Unknown")
    np.unique(pred_3, return_counts=True)
else:
    print("No samples labeled as 'Unkown' found.")

#整合所有类别
y_pred = pred_1.copy()
if filtered_x.shape[0] > 0:
    y_pred[y_pred == "Attack"] = pred_2
    y_pred[y_pred == "Unknown"] = pred_3
np.unique(y_pred, return_counts=True)
df = pd.DataFrame(newtest.iloc[:, [1,2,3,4,5,6]])

# i = len(y_pred)
# predictions = ['' for _ in range(i+1)]  # 初始化为空字符串的数组
# while i>0:
#     predictions[i]=y_pred[i-1]
#     i=i-1
# predictions[0]='Predictions'
# predictions = pd.Series(predictions)
print(y_pred)
df.reset_index(drop=True, inplace=True) #重置df的索引
df['7'] = y_pred
# print(y_pred)
#要筛除没有攻击的流量数据
#模型检测已有数据是正常的，但是检测捕获转换的数据是错误的

# 将DataFrame保存到CSV文件，没有index，没有header
df.to_csv('../data/attack.csv',mode='a', index=False, header=False, encoding='gb2312')

