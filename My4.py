from pymongo import MongoClient
import pandas as pd
from sklearn.ensemble import BaggingRegressor as BGR
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
con = MongoClient(host='192.168.43.91')
for i in range(1,11):
    v='zone'+str(i)
    print v
    db=con['zonesV2']
    df = pd.read_csv('T/finalData/T'+str(i)+'_train.csv')
    df1 = pd.read_csv('newFeature/vn{}.csv'.format(i))
    df = df.dropna()
    df['lasthr'] = df.load.shift(1)
    df = df[96:]
    df['prevload']=list(df1['feature'])
    df=df.reset_index(drop=True)
    val = {}
    for z in range(len(df)):
        val['temp']=float(df['Temp'][z])
        val['hour']=int(df['hour'][z])
        val['weekday']=int(df['weekday'][z])
        val['load']=float(df['load'][z])
        val['date']=str(df['date'][z])
        val['month']=int(df['month'][z])
        val['prevload']=float(df['prevload'][z])
        val['lasthr']=float(df['lasthr'][z])
        val['_id'] = str(val['date'])+str(val['hour'])
        db[v].insert(val)
    # df['a'] = df['Temp'] ** 2
    # df['hr1'] = df['hour'] ** 2
    # df['hr2'] = df['hour'] ** 3
    # df['hr3'] = df['hour'] ** 4
    # df['hr5'] = df['hour'] ** 5
    # df['months'] = df['month'] ** 2
    # train_y = np.asarray(df['load'])
    # train_x = np.array(df.drop(['date', 'load'], 1))
    # test_y = train_y[int(len(train_x) * 0.9):]
    # train_y = train_y[:int(len(train_y) * 0.9)]
    # train_x = preprocessing.scale(train_x)
    # test_x = train_x[int(len(train_x) * 0.9):]
    # train_x = train_x[:int(len(train_x) * 0.9)]
    # print mutual_info_regression(train_x, train_y)
    # x_train, x_test, y_train, y_test = cross_validation.train_test_split(train_x, train_y, test_size=0.2)
    # pc = PCA(n_components=1)
    # pc.fit_transform(x_train, y_train)
    # print pc.score(test_x, test_y)
    # print pc.score_samples(test_x)
    # clf = BGR()
    #
    # clf.fit(x_train, y_train)
    # print clf.score(test_x, test_y) * 100
