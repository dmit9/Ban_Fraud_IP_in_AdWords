import pymongo
import paho.mqtt.client as paho
import threading
from queue import Queue

q=Queue()

broker = "192.168.1.231"
url, date, time, IP, page, site, brouser = '', '', '', '', '', '', ''
Topics = [("url",0), ("date",0), ("time",0), ("IP",0), ("page",0), ("site",0), ("brouser",0)]

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["tvremont"]
mycol = mydb["tvrem"]
mycol2 = mydb["tvrem2"]

def on_message(client, userdata, message):
    topic = message.topic
    m_decode = (str(message.payload.decode("utf-8")))
    message_handler(client,m_decode,topic)

def message_handler(client,message,topic):
    mydict=dict()
    if topic=="url":
        mydict["url"] = message
    elif topic=="time":
        mydict["time"] = message
    elif topic=="IP":
        mydict["IP"] = message
    elif topic=="page":
        mydict["page"] = message
    elif topic=="site":
        mydict["site"] = message
    elif topic=="brouser":
        mydict["brouser"] = message
    q.put(mydict)

def worker():
    mydict=dict()
    while worker_flag:
        while not q.empty():
            mydict = q.get()
#            print(mydict)
            if mydict is None:
                continue
            try:
               url = mydict["url"]
               date = mydict["date"]
               time = mydict["time"]
               IP = mydict["IP"]
               site = mydict["site"]
               brouser = mydict["brouser"]
               print("url", url, "IP", time, brouser)
            except Exception as e:
                print("problem with logging ",e)
#            if data is None:
#                continue

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
