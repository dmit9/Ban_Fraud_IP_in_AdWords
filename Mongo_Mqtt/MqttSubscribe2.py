
def main():
    pass

if __name__ == '__main__':
    main()

import paho.mqtt.client as paho

broker = "192.168.1.231"
url, time, IP, page, site, brouser, name, comment = '2', '', '', '', '', '' , '' , ''
Topics = [("url",0), ("time",0), ("IP",0), ("page",0), ("site",0), ("brouser",0), ("name",0), ("comment",0)]

def on_message(client, userdata, message):
    if message.topic=="url":
        global url
        url=(str(message.payload.decode("utf-8")))
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
    elif message.topic=="name":
        global name
        name=(str(message.payload.decode("utf-8")))
 #       print(name)
    elif message.topic=="comment":
        global comment
        comment=(str(message.payload.decode("utf-8")))
#        print(comment)

client=paho.Client()
client.on_message = on_message
client.connect(broker)
client.subscribe(Topics)
client.loop_start()
while True:
    if IP != "":
        print(url, time, IP, "page", page, site, name, comment)
        IP = ""
#client.loop_forever()
