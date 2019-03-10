import pymongo
import paho.mqtt.client as paho

broker = "192.168.1.231"
url, date, time, IP, page, site, brouser = '', '', '', '', '', '', ''
Topics = [("url",0), ("date",0), ("time",0), ("IP",0), ("page",0), ("site",0), ("brouser",0)]

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["tvremont"]
mycol = mydb["tvrem"]
mycol2 = mydb["tvrem2"]
mydict = {"IP": IP, "time": time, "url": url, "page": page, "site": site, "brouser": brouser }

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
    mydict = {"IP": IP, "time": time, "url": url, "page": page, "site": site, "brouser": brouser }

client = paho.Client()
client.on_message = on_message
client.connect(broker)
client.subscribe(Topics)
client.loop_start()

while True:
    if date != "":
        mydict = {"IP": IP, "date": date, "time": time, "url": url, "page": page, "site": site, "brouser": brouser }
        a = str(url)
        if ( a.find("gclid") >= 0):
                print(mycol.index_information())
                x = mycol.insert_one(mydict)
                print(x.inserted_id)
                print("mycol")
        else:
                print(mycol2.index_information())
                x = mycol2.insert_one(mydict)
                print(x.inserted_id)
                print("mycol2")

        print( time, IP, url, page, brouser)
#        print(x.inserted_id)
        date = ""
        url, date, time, IP, page, site, brouser = '', '', '', '', '', '', ''