from pymongo import MongoClient
import pandas as pd
con = MongoClient(host='192.168.0.223')
con.drop_database('tests')
for i in range(1,11):
    v='zone'+str(i)
    print v
    db=con['tests']
    df = pd.read_csv('T/finalData/T'+str(i)+'_test.csv')
    val = {}
    for z in range(len(df)):
        ls = list(con['test_zone'][v].find().sort([('$natural',-1)]).limit(24))
        val['temp']=float(df['Temp'][z])
        val['hour']=int(df['hour'][z])
        val['weekday']=int(df['weekday'][z])
        val['load']=float(df['load'][z])
        val['date']=str(df['date'][z])
        val['month']=int(df['month'][z])
        val['prevload']=float(ls[23]['load'])
        val['lasthr']=float(ls[0]['load'])
        val['_id'] = str(val['date'])+str(val['hour'])
        con['test_zone'][v].insert(val,{'ordered':True})
        db[v].insert(val)
con.drop_database('test_zone')
