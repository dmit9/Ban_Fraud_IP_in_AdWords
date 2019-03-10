import pymongo
import paho.mqtt.client as paho
import threading
from queue import Queue

q=Queue()

broker = "192.168.1.231"
Topics = [("url",0), ("date",0), ("time",0), ("IP",0), ("page",0), ("site",0), ("brouser",0)]

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydatabase = myclient["tvremont"]
mycol = mydatabase["tvrem"]
mycol2 = mydatabase["tvrem2"]


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

def my_handler(m):
      for key in m.keys():
          if key == "url":
            a = str(m[key])
            if ( a.find("gclid") >= 0):
                return True
            elif ( a.find("googlequicksearchbox") >= 0):
                return True
            else:
                return False

def worker():
    while worker_flag:
        while not q.empty():
            mydict = q.get()
            if mydict is None:
                 continue
            my_handler(mydict)
            print(my_handler(mydict))
            try:
                if (my_handler(mydict)):
                    x = mycol.insert_one(mydict)
#                    print(str(mydict[brouser]) )
                else:
                    y = mycol2.insert_one(mydict)
            except Exception as e:
                print("problem with logging ",e)
                continue


t = threading.Thread(target = worker) #start logger
worker_flag = True
t.start() #start logging thread

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
