import pymongo
import paho.mqtt.client as paho
import threading
from queue import Queue
import os
import time

q=Queue()

broker = "192.168.1.231"
#url, date, tim, IP, page, site, brouser = '', '', '', '', '', '', ''
Topics = [("url",0), ("date",0), ("time",0), ("IP",0), ("page",0), ("site",0), ("brouser",0)]

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydatabase = myclient["tvremont"]
mycol = mydatabase["tvrem"]
mycol2 = mydatabase["tvrem2"]
mycol3 = mydatabase["tvrem3"]

mydict=dict()
mydict["_id_"] = ""
mydict["url"] = ""
mydict["date"] = ""
mydict["time"] = ""
mydict["IP"] = ""
mydict["page"] = ""
mydict["site"] = ""
mydict["brouser"] = ""

global w


def on_message(client, userdata, message):
    topic = message.topic
    m_decode = (str(message.payload.decode("utf-8")))
    message_handler(client,m_decode,topic)

def message_handler(client,message,topic):
##    mydict=dict()
    if topic=="url":
        mydict["url"] = message
    elif topic=="date":
        mydict["date"] = message
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
#        mydict["_id_"] = ""
        q.put(mydict)
#        mongo_flag = True
#        q.put(mongo_flag)
    return mongo_flag

def my_handler(m):
      w = 0
      for key in m.keys():
          if key == "url":
            a = str(m[key])
#            print(a.find("oni"))
            if ( a.find("gclid") >= 0):
                w = 1
#                print("mycol")
#                print(a)
            elif (a.find("oni") >= 0):
                w = 3
#                print("mycol3")
            else:
                w = 2
#                print("mycol2")
#      print(w)
      if (w == 1):
        return True
      elif (w == 2):
        return False

def worker():
    while worker_flag:
        while not q.empty():

            mydict = q.get()
#            flag = q.get(mongo_flag)
#            print(mydict)
            if mydict is None:
                 continue
            my_handler(mydict)
            print(my_handler(mydict))
            try:
                if (my_handler(mydict)):
                    time.sleep(0.1)
                    x = mycol.insert_one(mydict)
                    print(x.inserted_id)
                else:
                    print(mycol2.index_information())
#                    y = mycol2.drop_index("_id_")
#                    print(mycol2.index_information()  )
                    y = mycol2.insert_one(mydict)
                    print(y.inserted_id)
                    print("mycol222")
            except Exception as e:
                print("problem with logging ",e)
                continue


##            try:

##            except Exception as e:
##                print("problem with logging ",e)
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
