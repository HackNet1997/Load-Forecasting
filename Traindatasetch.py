from pymongo import MongoClient
from bson import Binary
import datetime

class FetchDataUnit:

    def __init__(self):
        self.client = MongoClient(host='192.168.0.223')

    def getTrainData(self,zone):
        client=self.client
        db = client.zones
        val = {'temp':[],'date':[],'hour':[],'month':[],'weekday':[],'load':[],'prevload':[],'lasthr':[]}
        curs=db['zone'+str(zone)].find()
        for doc in curs:
            val['temp'].append(doc['temp'])
            val['hour'].append(doc['hour'])
            val['weekday'].append(doc['weekday'])
            val['load'].append(doc['load'])
            val['date'].append(doc['date'])
            val['month'].append(doc['month'])
            val['prevload'].append(doc['prevload'])
            val['lasthr'].append(doc['lasthr'])
        return val

    def get_obj(self,name,zone):
        oid = str(name)
        db = self.client.picklestore
        col = db['zone' + str(zone)]
        dic = col.find({'_id':oid})
        return dic['obj'],dic['preprocessing'],dic['PCA']

    def storeObj(self, pickleobj, zone, acc, preobj,pca , name='{0}/{1}/{2}{3}'.format(datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year, datetime.datetime.now().hour)):
        db = self.client.picklestore
        col = db['zone' + str(zone)]
        dic = {'_id': name, 'obj': Binary(pickleobj), 'accuracy': acc,'preprocessing':preobj,'zone':zone,'PCA':pca}
        col.insert(dic)

    def setCurrentObj(self, obj, zone, name,preobj,pca,acc):
        db = self.client.picklestore
        col = db['currentWrkObj']
        col.update({'_id': zone}, {'$set': {'_id': zone, 'obj': Binary(obj), 'name': name,'preprocessing':preobj,'PCA':pca,'accuracy':acc}}, upsert=True)

    def get_current_obj(self,zone):
        db = self.client.picklestore
        col = db['currentWrkObj']
        val = col.find({'zone': zone})
        return val['obj'],val['preprocessing'],val['PCA']

    def predictstore(self,pred):
        db = self.client.one
        pre={}
        no=datetime.datetime.now()
        pre['_id'] = str(no.day) + str(no.month) + str(no.year) + str(no.hour)
        pre['prediction'] = pred['prediction']
        pre['actual'] = 0
        db.prediction.insert_one(pre)

    def gettestdata(self,dataid,zone):
        cl = MongoClient(host='192.168.0.223')
        db = cl.tests
        ls = list(db['zone{}'.format(zone)].find({'_id':dataid}).sort([('$natural', -1)]).limit(1))
        return ls[0]

if __name__ == '__main__':
    pass
