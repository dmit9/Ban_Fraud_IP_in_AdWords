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

mydict=dict()
mydict["url"] = ""
mydict["date"] = ""
mydict["time"] = ""
mydict["IP"] = ""
mydict["page"] = ""
mydict["site"] = ""
mydict["brouser"] = ""

global w
#w = 0

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
        q.put(mydict)
def mongo(r):
    if (r == 1):
        x = mycol.insert_one(mydict)
        print('r',r)
    elif (r == 2):
        x = mycol2.insert_one(mydict)
        print('r',r)
def my_handler(m):
      w = 0
      for key in m.keys():
          if key == "url":
            a = str(m[key])
#            print(a.find("oni"))
            if ( a.find("gclid") >= 0):
                w = 1
                print("mycol")
                print(a)
            elif (a.find("oni") >= 0):
                w = 3
                print("mycol3")
            else:
                w = 2
                print("mycol2")
      print(w)
      if (w == 3):
        mongo(w)
        return True
      elif (w == 2):
        mongo(w)
        return False
##      if (q == 1):
##          x = mycol.insert_one(m)
##          q = 0
##      elif (q == 2):
##          x = mycol2.insert_one(m)
##          q = 0
def worker():
    w = 0
    while worker_flag:
        while not q.empty():
            mydict = q.get()
#            print(mydict)
            if mydict is None:
                 continue
            my_handler(mydict)

#               x = mycol2.insert_one(mydict)

#            if (w == 1):
#                x = mycol.insert_one(my)
#                w = 0
#            elif (w == 2):
#                x = mycol2.insert_one(my)
#                print("mycol222")
#                w = 0
#            tim = mydict["time"]
#            print("TIMEEE", tim)
#            print(my["time"])
            if mydict is None:
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
