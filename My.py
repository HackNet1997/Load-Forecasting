from pymongo import MongoClient
import pandas as pd
con = MongoClient(host='192.168.43.91')
for i in range(1,2):
    v='zone'+str(i)
    print v
    db=con['zones']
    df = pd.read_csv('T/finalData/T'+str(i)+'_train.csv')
    df['lasthr'] = df.load.shift(1)
    df['prevload'] = df.load.shift(24)
    df=df[24:]
    val = {}
    for z in range(24,len(df)+24):
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