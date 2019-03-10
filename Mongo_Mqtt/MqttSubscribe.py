def main():
    pass

if __name__ == '__main__':
    main()

import paho.mqtt.client as paho

broker = "192.168.1.231"
url, time, IP, page, site, brouser = '2', '', '', '', '', ''
Topics = [("url",0), ("time",0), ("IP",0), ("page",0), ("site",0), ("brouser",0)]

def on_message(client, userdata, message):
    if message.topic=="url":
        global url
        url=(str(message.payload.decode("utf-8")))
        print(url)
    elif message.topic=="time":
        global time
        time=(str(message.payload.decode("utf-8")))
        print(time)
    elif message.topic=="IP":
        global IP
        IP=(str(message.payload.decode("utf-8")))
        print(IP)
    elif message.topic=="page":
        global page
        page=(str(message.payload.decode("utf-8")))
        print(page)
    elif message.topic=="site":
        global site
        site=(str(message.payload.decode("utf-8")))
        print(site)
    elif message.topic=="brouser":
        global brouser
        brouser=(str(message.payload.decode("utf-8")))
        print(brouser)

client=paho.Client()
client.on_message = on_message
client.connect(broker)
#client.loop_start()

client.subscribe(Topics)
print("1")
print(url)
client.loop_forever()
print("1")
print(url)