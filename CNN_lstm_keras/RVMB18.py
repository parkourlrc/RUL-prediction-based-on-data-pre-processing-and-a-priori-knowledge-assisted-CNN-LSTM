from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
import missingno as msno
import math
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVR

df=pd.read_excel("./汇总/IMF1到RES/B18.xls")
print(df.head(6))   #输出前六行的内容


msno.matrix(df)

data = df.sort_index(ascending=True, axis=0)
##只使用股票的收盘价来进行拟合和预测
#dataset=data[['rongliang']].values
dataset=data.values

data.head()
data.shape
dataset.shape

                                                                                    #
#取80%的数据作为训练集
training_data_len=math.ceil(len(dataset)*.6)
train_data=dataset[0:training_data_len,:]
#取剩下的数据作为测试集
#在做预测时，余下的数据的第一个数据，需要前60*200轮的数据来预测，因此这倒溯了60*200天
test_data = dataset[training_data_len-60: , : ]
                                                                                    #

scaler = MinMaxScaler(feature_range=(0,1))
scaled_train = scaler.fit_transform(train_data)
scaled_test = scaler.fit_transform(test_data)
scaled_train
scaled_test.shape
scaled_train.shape

#训练集的重构
#1 分离x和y
x_train=[]
y_train=[]
                                                                        #
#for i in range(60,len(scaled_train)-10):
#    x_train.append(scaled_train[i-60:i,0])
#    y_train.append(scaled_train[i+10,0])
for i in range(60,len(scaled_train)):
    x_train.append(scaled_train[i-60:i,0])
    y_train.append(scaled_train[i,0])
                                                                        #
#2 将list类型数据转变成array数据
x_train,y_train=np.array(x_train),np.array(y_train)

#3 将二维数据变成三维数据
#x_train=np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1))

#x_train.shape

#测试集的重构
#1 分离x和y
x_test = []
                                                                        #
#y_test = dataset[training_data_len+10: , : ] 
#for i in range(60,len(scaled_test)-10):
#    x_test.append(scaled_test[i-60:i,0])
y_test = dataset[training_data_len: , : ] 
for i in range(60,len(scaled_test)):
    x_test.append(scaled_test[i-60:i,0])
                                                                        #
#2 将list类型数据转变成array数据
x_test = np.array(x_test)
#3 将二维数据变成三维数据
#x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))

#x_test.shape

# 创建 SVM 回归模型
svr = SVR(kernel='rbf', C=1.0, epsilon=0.2)

# 训练模型
svr.fit(x_train, y_train)

# 进行预测
y_pred = svr.predict(x_test)
predictions = []
for i in range(len(y_pred)):
    predictions.append([])
    predictions[i].append(y_pred[i])
print(predictions)
y_pred = scaler.inverse_transform(predictions)
print(y_pred)

# 计算均方误差
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

predictions_fail = 0
actual_fail = 0
for i in range(len(y_pred)):
    if y_pred[i][0] <=1.4:
        predictions_fail = i+1+len(dataset)-len(y_pred)
        break
for i in range(len(dataset)):
    if dataset[i][0] <=1.4:
        actual_fail= i+1
        break
  
ae = predictions_fail-actual_fail
mae = np.mean(np.abs(y_test - y_pred))*100
rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))*100
print('预测寿命为',predictions_fail,'实际寿命为',actual_fail,'AE=',ae,'MAE=',mae,'%','RMSE=',rmse,'%')
'''
# 创建RVM回归模型
RVM = rvm(kernel='rbf')

# 训练模型
RVM.fit(x_train, y_train)

# 进行预测
y_pred = RVM.predict(x_test)

# 计算均方误差
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)
'''