
import pandas as pd

data = pd.read_excel('~/PycharmProjects/sale_time_data/Sale_Daily_data2017.xlsx')
data.rename(columns={'Sale Date Time':'data1',0:'Total'},inplace=True)
#data.columns = ['data1','Total']
data['Total']= round(data['Total']/100000,4)
import matplotlib.pyplot as plt
plt.rcParams['fron.sans-serif']='SimHei'
#时序图
plt.figure(figsize=(18,8),dpi=256)
data['Total'][:-30].plot()
#剩余作为test
#自相关图
from statsmodels.graphics.tsaplots import plot_acf
plt.figure(figsize=(18,8),dpi=256)
plot_acf(data['Total'][:-30])
#ListLinePlot[data, PlotStyle -> Dashed, PlotMarkers -> {"o", 8}]
#单位与检验
from statsmodels.tsa.stattools import adfuller as ADF
print(ADF(data['Total'][:-30]))
#这里的p值等于0.976多，大于0.05，属于不平稳序列，需要进行差分后，再检验是否属于平稳序列。
D_data = data['Total'][:-30].diff().dropna()
print(ADF(D_data))
plot_acf(D_data)
#p value <0.05  stable 使用差分后平稳序列的模型ARIMA进行预测，预测前还得进行白噪声检验。

from statsmodels.stats.diagnostic import acorr_ljungbox
print('白噪声检验结果：',acorr_ljungbox(D_data,lags=1))
#白噪声检验的p值(输出的第二个参数）远小于0.05，一阶差分后的时间序列属于平稳非白噪声的时间序列
#ARIMA模型进行预测
from statsmodels.tsa.arima_model import ARIMA
from datetime import datetime
from itertools import product
ps = range(0,5)
qs =range(0,5)
parameters = product(ps,qs)
parameters_list = list(parameters) #组合
best_aic = float('Inf')
results=[]
for param in parameters_list:
    try:
        model = ARIMA(data['Total'][:-30],order=(param[0],1,param[1])).fit()
    except ValueError:
        print('参数错误：',param)
        continue
    aic = model.aic
    if aic < best_aic:
        best_model = model
        best_aic = aic
        best_param =param
    results.append([param,model.aic])
result_table = pd.DataFrame(results)
result_table.columns = ['Parameters','aic']
print('best model',best_model.summary)
best_model.forecast(30)[0]
#模型评价
from sklearn.metrics import mean_squared_error
pre_y = best_model.forecast(30)[0] # forecast 还原差分结果
test_y = data['Total'][-30:].values
mean_squared_error(test_y,pre_y) #根据业务确定误差
#plot
plt.figure(figsize=(14,7),dpi=256)
plt.plot(data['data1'][-30:],test_y,label='Acture')
plt.plot(data['data1'][-30:],pre_y,label='Predict')
plt.xticks(data['data1'][-30:],rotation=70)
plt.legend(loc=3)
