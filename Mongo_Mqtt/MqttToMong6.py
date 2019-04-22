import pymongo
import paho.mqtt.client as paho
import threading
from queue import Queue

q=Queue()

broker = "192.168.1.231"
Topics = [("url",0), ("date",0), ("time",0), ("IP",0), ("page",0), ("site",0), ("brouser",0), ("name",0), ("comment",0)]
comment, name = '',''
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydatabase = myclient["tvremont"]
mycol = mydatabase["tvrem"]
mycol2 = mydatabase["tvrem2"]
mycol_otziv = mydatabase["tvremOtziv"]

def on_message(client, userdata, message):
    if message.topic=="brouser":
        global brouser
        brouser=(str(message.payload.decode("utf-8")))
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
    elif message.topic=="name":
        global name
        name=(str(message.payload.decode("utf-8")))
    elif message.topic=="comment":
        global comment
        comment=(str(message.payload.decode("utf-8")))
    elif message.topic=="url":
        global url
        url=(str(message.payload.decode("utf-8")))
        mydict = {"IP": IP, "time": time, "date":date, "url": url, "page": page, "site": site, "brouser": brouser, "name": name, "comment": comment }
        q.put(mydict)
        comment, name = '',''

def worker():
    while worker_flag:
        while not q.empty():
            mydict = q.get()
            print('mydict',mydict)
            if mydict is None:
                 continue
            find_url =  str(mydict["url"])
            try:
                requestGugl = ['gclid', 'onas']
                requestOtziv = ['OTZIV']
                if any(c in find_url for c in requestGugl):   #  Если пришел из поиска Гугл gclid
                    x = mycol.insert_one(mydict)
                    print('G')
                elif any(c in find_url for c in requestOtziv):   #  Если пришел писатель отзыва
                    y = mycol_otziv.insert_one(mydict)
                    print('Otziv')
                else:
                    print('--', mydict["page"])
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

