import numpy as np
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 50)
# 设置1000列的时候才换行
pd.set_option('display.width', 1000)

# read data
file_path = r'~/PycharmProjects/sale_time_data/sale_data/Sales Report.csv'
df = pd.read_csv(file_path, iterator=True,sep=';')
#data= df.get_chunk(6000000)
#data.info()
chunks=[]
loop = True
chunkSize = 3000000
while loop:
    try:
        chunk = df.get_chunk(chunkSize)
        chunks.append(chunk)
    except StopIteration:
        loop = False
        print("Iteration is stopped.")
data = pd.concat(chunks,ignore_index=True)
data.isnull().any() #null check
data.describe()
# remove outlier
len(data[data['Product Cost']<0])
data.drop(index=data[data['Product Cost']<0].index,inplace=True)
# duplicate
len(data[data.duplicated()])
data.drop(index=data[data.duplicated()].index,inplace=True)

# transform time
data['Sale Date Time'] = pd.to_datetime(data['Sale Date Time'])
data.info()
data.head()
data.tail()

# sale time ARIMA data
data.set_index('Sale Date Time', inplace=True,drop=True)
data.to_csv('D:\learn\kaggle\sale data\Sale_data_filter.csv')
day_data = data.resample('d').sum()['Total'] ##按天求和
day_data
#select
train_day_data = day_data[day_data.index >=  '2017-04-01']
train_day_data = train_day_data[train_day_data.index <= '2018-04-30']
train_day_data.tail()
train_day_data.to_excel('D:\learn\kaggle\sale_time_data\sale_data\Sale_Daily_data2017.xlsx')


#2017-2018
data = data[data.index >= '2017-04-01']
data = data[data.index <= '2018-04-30']
data['Total']= round(data['Total']/100000,4)
data.to_csv('~/PycharmProjects/sale_time_data/Sale_Daily_data201704_2018_04.csv')
data = pd.read_csv('~/PycharmProjects/sale_time_data/Sale_Daily_data201704_2018_04.csv')
data.head()

#top 10 clients
data_user_amount = data['Amount'].groupby(data['Client']).sum()
data_user_count = data['Amount'].groupby(data['Client']).count()
data_user_count.rename(columns={'Amount':'Count'},inplace=True)
data_user_amount.head()
data_user_amount = pd.DataFrame(data_user_amount)
data_user_count = pd.DataFrame(data_user_count)

#去除index
data_user_amount.index = data_user_amount.index.droplevel()
#data_user_plot = pd.merge(data_user_amount,data_user_count,on='Client')
data_user_plot = pd.concat([data_user_amount,data_user_count],axis=1)
#data_user_plot=data_user_amount.join(data_user_count)
data_user_plot =sorted(data_user_plot,key=['Amount'],reverse=True)
data_user_plot_sort=data_user_plot.sort_values(['Amount'],ascending=False).iloc[:10,]
data_user_plot_sort['Amount']= round(data_user_plot_sort['Amount']/100000,4)

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.figure(figsize=(12,6),dpi=256)
plt.subplots(2,1)
plt.bar(data_user_plot_sort.index,data_user_plot_sort['Amount'])
plt.bar(data_user_plot_sort.index,data_user_plot_sort['Count'])
#
#month rate
def tran_mon(data_time):
    if data_time.month <10:
        return str(data_time.year) +'-0'+ str(data_time.month)
    else:
        return str(data_time.year) +'-'+ str(data_time.month)
data=data.reset_index()
data['Sale_month']= data['Sale Date Time'].apply(tran_mon)
#data.to_csv('~/PycharmProjects/learn/kaggle/sale_time_data/sale_data/201704_2018_04_month.csv')
#