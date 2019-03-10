import pymongo
import datetime

now = datetime.datetime.now()
dateNow = str(now.strftime("%Y.%m.%d"))
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydatabase = myclient["tvremont"]
mycol = mydatabase["tvrem"]
mycol2 = mydatabase["tvrem2"]

a = mycol.find({"date" : dateNow}, { "_id": 0, "IP": 1, "date": 1, "time": 1, "brouser": 1 }).sort("brouser")
for x in a:
        print(x)