import pymongo


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["tvremont"]
mycol = mydb["tvrem"]
mycol2 = mydb["tvrem2"]

#for x in mycol2.find( { }, { "_id": 0, "IP": 1, "time": 1 } ):

#mydoc = mycol.find( { }, { "_id": 0, "IP": 1, "date": 1, "time": 1, "brouser": 1 } ).sort("IP")

mydoc = mycol.find( { }, { "_id": 0, "IP": 1, "date": 1, "time": 1, "brouser": 1 } ).sort("date")
#mydoc = mycol.find( { text: { $regex: 'находить'} }).explain()

for x in mydoc:
      print(x)

y = mycol.count_documents({})
print("Всего записей ", y)