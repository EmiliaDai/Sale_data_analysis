import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 50)
# 设置1000列的时候才换行
pd.set_option('display.width', 1000)

data=pd.read_csv('~/PycharmProjects/sale_time_data/201704_2018_04_month.csv')
#复购率
client_data = data.groupby('Client').nunique()['Order Number']
client_data = client_data.reset_index().rename(columns={ 'Order Number':'user_num'})
client_data.sort_values('user_num',ascending=False,inplace=True)
print('总复购率:',round( (len(client_data[client_data['user_num']>1])-1)/(len(client_data)-1),4)*100,"%")

y_m_data=data.groupby(['Sale_month','Client']).nunique()['Order Number'].reset_index()
data.head()
month_list=[]
mon_count_list=[]
for mon in y_m_data['Sale_month'].unique():
    print(mon)
    temp = y_m_data[y_m_data['Sale_month'] == mon]
    month_list.append(mon)
    filt_num=(len(temp[temp['Order Number']>1])-1)
    sum_num=(len(temp)-1)
    mon_count_list.append(round(filt_num/sum_num,4))

month_rate = {"year_month":month_list,'rate':mon_count_list}
month_rate = pd.DataFrame(month_rate)
month_rate.to_excel('./month_rate.xlsx',index=False)
#one month
data_201804 = y_m_data[y_m_data['Sale_month']=='2018-04']
data_201804.rename(columns={'Order Number':'buy_frequency'},inplace=True)
#分段
bins=[0,1,2,5,10,50,100,100000]
pre_frequency = pd.cut(data_201804['buy_frequency'],bins)
pre_frequency.value_counts()#每个bins 计数
pre_frequency.value_counts().plot(kind='var')

#RFM
RFM_data = data.groupby(['Sale_month','Client']).agg({'Order Number': 'nunique',
                                        'Sale Date Time': 'max',
                                        'Total': 'sum'})
RFM_data.head()
RFM_data.reset_index(inplace=True)
RFM_data.to_csv('RFM_data.csv',index=False)
RFM_data=pd.read_csv('~/PycharmProjects/sale_time_data/RFM_data.csv')
RFM_04_data = RFM_data[RFM_data['Sale_month']=='2018-04']
#
import datetime
#使R不等于0
reference_time = datetime.datetime.strptime('2018-05-01 23:59:59',"%Y-%m-%d %H:%M:%S")
#R
RFM_04_data['Sale Date Time'] = pd.to_datetime(RFM_04_data['Sale Date Time'])
RFM_04_data['R']=RFM_04_data['Sale Date Time'].apply(lambda x: (reference_time - x).days)
RFM_04_data.rename(columns={'Order Number':'F','Total':'M'},inplace=True)
RFM_04_data.head()

#检查异常值
RFM_04_data.sort_values('M',ascending=False).head()
#异常值处理
len(RFM_04_data)

#RFM_04_data=RFM_04_data[~ RFM_04_data['Client']=='Customer not informed']
ind = RFM_04_data['Client']!='Customer not informed'
RFM_04_data=RFM_04_data.loc[ind,]

RFM_04_data.to_csv('RFM_data_2018-04_filter.csv',index=False)
#提取
RFM_data = RFM_04_data[['R','F','M']]
#聚类
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

ss = StandardScaler()
train=ss.fit_transform(RFM_data)
#train
kmeans_model = KMeans(n_clusters=5)
kmeans_model.fit(train)
##查看聚类中心
test = pd.DataFrame(kmeans_model.cluster_centers_,columns=['R','F','M'])
test
#分群的结果合并到RFM_data
RFM_04_data['sk5_label']= kmeans_model.labels_
#挑出分群3、4的数据来看看
RFM_data[RFM_data['sk5_label']==3]
RFM_data[RFM_data['sk5_label']==4]

RFM_04_data.to_csv('RFM_data_cluster.csv',index=False)
#every month user
# 提取每个月的用户（去重）
every_month_user = data.groupby(['Sale_month','Client']).nunique ()['Order Number'].reset_index()
#every_month_user['Sale_month']=pd.to_datetime(every_month_user['Sale_month'])

year_month = every_month_user['Sale_month'].unique()
#year_month=year_month.sort_values(ascending=True)
list_month_rate = []
for i,mon in enumerate(year_month):
    if i>=1:#this month
        this_m_client = every_month_user[every_month_user['Sale_month']==mon]['Client']
        mon_pre=year_month[i-1]
        pre_m_client =  every_month_user[every_month_user['Sale_month']==mon_pre]['Client']
        #这里用的是上个月与当前月用户的交集个数/上个月的用户数（去重）
        len1=len(set(this_m_client)&set(pre_m_client))
        len2=len(pre_m_client)
        rate = round(len1/len2,2)
        b=[mon,rate]
        print(b)
        list_month_rate.append(b)
rate_data = pd.DataFrame(list_month_rate,columns=['year_month','rate'])
rate_data
rate_data.to_csv('month_retention_rate.csv',index=False)










