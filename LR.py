from sklearn import cross_validation
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import mutual_info_regression
import pandas as pd
from utils.function_schedular import FunSch
import numpy as np
from pymongo import MongoClient
from sklearn import preprocessing
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import datetime

con = MongoClient(host='192.168.0.230',port=27017)
db = con.one
df = pd.read_csv('T/finalData/T1_train.csv')

df['prev'] = df.load.shift(24)
df = df.dropna()
df = df[24:]
df['lasthr'] = df.load.shift(1)
df = df[1:]
df['a'] = df['Temp']**2
df['hr1'] = df['hour']**2
df['hr2'] = df['hour']**3
df['hr3'] = df['hour']**4
df['hr5'] = df['hour']**5
df['months'] = df['month']**2
train_y = np.asarray(df['load'])
train_x = np.array(df.drop(['date','load'],1))
test_y = train_y[int(len(train_x)*0.9):]
train_y = train_y[:int(len(train_y)*0.9)]
train_x = preprocessing.scale(train_x)
test_x = train_x[int(len(train_x)*0.9):]
train_x = train_x[:int(len(train_x)*0.9)]
print mutual_info_regression(train_x, train_y)
x_train, x_test, y_train, y_test = cross_validation.train_test_split(train_x,train_y,test_size=0.2)
pc = PCA(n_components=1)
pc.fit_transform(x_train,y_train)
print pc.score(test_x,test_y)
print pc.score_samples(test_x)
clf = LinearRegression()

clf.fit(x_train, y_train)
print clf.score(test_x, test_y)*100

no = datetime.datetime.now()
import time


def func(clf,db,test_x,no,test_y):
    pre = {}
    pred = clf.predict(test_x)
    for x in range(1, 25):
        pre['_id'] = str(no.day) + str(no.month) + str(no.year) + str(x)
        pre['prediction'] = pred[x - 1]
        pre['actual'] = test_y[x - 1]
        time.sleep(10)
        db.abc.insert_one(pre)
ob = FunSch()
ob.startNextHour(func, (clf,db,test_x,test_y))
#plt.plot(list(pred)[:20],list(test_y)[:20])
#plt.show()
