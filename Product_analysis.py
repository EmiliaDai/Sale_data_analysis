import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', 100)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 50)
# 设置1000列的时候才换行
pd.set_option('display.width', 1000)

data=pd.read_csv('~/PycharmProjects/sale_time_data/201704_2018_04_month.csv')

product_data = data.groupby(['Sale_month','Product']).agg({'Product Cost':'mean','Order Number':'nunique','Total':'sum'})

product_data.reset_index(inplace=True)
product_data.rename(columns={'Product Cost':'C','Order Number':'F','Total':'M'},inplace=True)
product_data.to_csv('Product_data.csv',index=False)
product_data = pd.read_csv('~/PycharmProjects/sale_time_data/Product_data.csv')
product_04 = product_data[product_data['Sale_month']=='2018-04']

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

ss=StandardScaler()
train = product_04[['C','F','M']]
#标准化
train=ss.fit_transform(train)
model=DBSCAN(min_samples=4)
#train
model.fit(train)
# 将聚类的结果合并到原数据集上。
product_04['label'] =model.labels_
product_04['label'].value_counts()

product_04.to_csv('product_CFM.csv',index=False)