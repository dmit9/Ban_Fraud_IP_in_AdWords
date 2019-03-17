import pymongo
import paho.mqtt.client as paho
import threading
from queue import Queue
import datetime

q=Queue()
q2 = Queue()

broker = "192.168.1.231"
Topics = [("url",0), ("date",0), ("time",0), ("IP",0), ("page",0), ("site",0), ("brouser",0)]

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydatabase = myclient["tvremont"]
mycol = mydatabase["tvrem"]
mycol_tvremNotGoogl = mydatabase["tvremNotGoogl"]
mycol_tvremBanedForever = mydatabase["tvremBanedForever"]
mycol_tvremBanedToday = mydatabase["tvremBanedToday"]

BanIP = []

def on_message(client, userdata, message):
    if message.topic=="url":
        global url
        url=(str(message.payload.decode("utf-8")))
    elif message.topic=="date":
        global date
        date=(str(message.payload.decode("utf-8")))
    elif message.topic=="time":
        global time
        time=(str(message.payload.decode("utf-8")))
    elif message.topic=="IP":
        global IP
        IP=(str(message.payload.decode("utf-8")))
    elif message.topic=="page":
        global page
        page=(str(message.payload.decode("utf-8")))
    elif message.topic=="site":
        global site
        site=(str(message.payload.decode("utf-8")))
    elif message.topic=="brouser":
        global brouser
        brouser=(str(message.payload.decode("utf-8")))
        mydict = {"IP": IP, "time": time, "date":date, "url": url, "page": page, "site": site, "brouser": brouser }
        q.put(mydict)

def worker():
    while worker_flag:
        while not q.empty():
            mydict = q.get()
            if mydict is None:
                 continue
            try:
                count_repit_brouser = 0
                count_repit_ip = 0
                brouser = mydict["brouser"]
                IP = mydict["IP"]
                find_url =  str(mydict["url"])
                br = mycol.find({"brouser" : brouser}, {"repIP" : 1, "repBr": 1, "IP": 1, "date": 1, "time": 1, "brouser": 1 })
                ip = mycol.find({"IP" : IP}, {"repIP" : 1,  "repBr": 1, "IP": 1, "date": 1, "time": 1, "brouser": 1 })
                request = ['gclid', 'onas']
                if any(c in find_url for c in request):
                    q2.put(IP)
                    q2.put(brouser)
                    for x in br:
                        count_repit_brouser = count_repit_brouser + 1
                        if (count_repit_brouser > 1):
                            mycol.update_one({"_id" : x["_id"]}, { "$set": {"repBr" : count_repit_brouser}})
#                            print(x["_id"])
                    for y in ip:
                        count_repit_ip = count_repit_ip + 1
                        if (count_repit_ip > 1):
                            mycol.update_one({"_id" : y["_id"]}, { "$set": {"repIP" : count_repit_ip}})
#                        print(y)
                    print(mydict["time"], "  ", brouser)
                    print("Повторов =", count_repit_brouser, "        IP =",  count_repit_ip, IP )
            except Exception as e:
                print("problem with logging ",e)
                continue

def worker2():
     while worker_flag:
        while not q2.empty():
            IP = q2.get()
            brouser = q2.get()
            mycol_tvremBanedToday.update_one({"IP" : IP}, {"$set": {"IP": IP}}, upsert = True )
            brouser_str = str(brouser)
            if (brouser_str.find("Linux") >= 0):
                print("Linux")
            elif (brouser_str.find("iPhone") >= 0):
                print("iPhone")
            elif (brouser_str.find("Windows") >= 0):
                print("Windows")
            else:
                print("X3")




t = threading.Thread(target = worker) #start logger
worker_flag = True
t.start() #start logging thread

t2 = threading.Thread(target = worker2)
worker2_flag = True
t2.start()

client = paho.Client()
client.on_message = on_message
client.connect(broker)
client.subscribe(Topics)
client.loop_start()

try:
    while True:
        pass

except KeyboardInterrupt:
    print("interrrupted by keyboard")
