import pymongo
import paho.mqtt.client as paho
import threading
from queue import Queue
import datetime
import time
from datetime import datetime, timedelta, date, time as dt_time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from constants import login, passw

q=Queue()
q2 = Queue()
# MQTT Setting
broker = "192.168.1.231"
Topics = [("url",0), ("date",0), ("time",0), ("IP",0), ("page",0), ("site",0), ("brouser",0)]
# Mongo Setting
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydatabase = myclient["tvremont"]
mycol = mydatabase["tvrem"]
mycol_tvremNotGoogl = mydatabase["tvremNotGoogl"]
mycol_tvremBanedForever = mydatabase["tvremBanedForever"]
mycol_tvremBanedToday = mydatabase["tvremBanedToday"]
# Goodl Setting
urlG = 'https://accounts.google.com/signin'
urlTel = 'https://ads.google.com/aw/settings/campaign/search?campaignId=98795004&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001'
urlTelRu49 = 'https://ads.google.com/aw/settings/campaign/search?campaignId=1636077101&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001'
urlKomRu43 = 'https://ads.google.com/aw/settings/campaign/search?campaignId=1620167217&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001'
urlKomRu34 = 'https://ads.google.com/aw/settings/campaign/search?campaignId=1644471505&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001'
xpath_1 = "//*[@id='cmExtensionPoint-id']/base-root/div/div[2]/div[1]/view-loader/search-campaign-settings-view/div/div/construction-layout/construction-layout-engine/div/div/div[11]/material-button/div/span"
xpath_2 = "//*[@id='cmExtensionPoint-id']/base-root/div/div[2]/div[1]/view-loader/search-campaign-settings-view/div/div/construction-layout/construction-layout-engine/div/div/div[11]/div/div[4]/lazy-plugin/div/dynamic-component/ip-exclusions/material-expansionpanel/div/header/div/div[1]/p"
xpath_3 = "//*[@id='cmExtensionPoint-id']/base-root/div/div[2]/div[1]/view-loader/search-campaign-settings-view/div/div/construction-layout/construction-layout-engine/div/div/div[11]/div/div[4]/lazy-plugin/div/dynamic-component/ip-exclusions/material-expansionpanel/div/main/div/div/div/div/div[2]/div/div[1]/material-input/div[1]/div[1]/div/div[2]/textarea"
xpathSave = "//*[@id='cmExtensionPoint-id']/base-root/div/div[2]/div[1]/view-loader/search-campaign-settings-view/div/div/construction-layout/construction-layout-engine/div/div/div[11]/div/div[4]/lazy-plugin/div/dynamic-component/ip-exclusions/material-expansionpanel/div/main/div/material-yes-no-buttons/material-button[1]/material-ripple"
xpath_5 = "//*[@id='cmExtensionPoint-id']/base-root/div/div[2]/div[1]/view-loader/search-campaign-settings-view/div/div/construction-layout/construction-layout-engine/div/div/div[11]/div/div[4]/lazy-plugin/div/dynamic-component/ip-exclusions/material-expansionpanel/div/header/div/div[2]/div"
xpathCancel = "//*[@id='cmExtensionPoint-id']/base-root/div/div[2]/div[1]/view-loader/search-campaign-settings-view/div/div/construction-layout/construction-layout-engine/div/div/div[11]/div/div[4]/lazy-plugin/div/dynamic-component/ip-exclusions/material-expansionpanel/div/main/div/material-yes-no-buttons/material-button[2]/material-ripple"

BanedIP = '37.73.217.26'

def initAndLogin():
    driver.set_window_size(500, 700)
    driver.get(urlG)
    time.sleep(1)
    elem = WebDriverWait(driver, 10).until(lambda driver : driver.find_elements_by_id("identifierId"))
    elem[0].send_keys(login)
    driver.find_element_by_xpath("//*[@id='identifierNext']/content/span").click()
    time.sleep(2)
    elem = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input"))
    elem.send_keys(passw)
    time.sleep(2)
    ele = driver.find_element_by_xpath("//*[@id='passwordNext']/content/span").click()
    time.sleep(15)
    e = input("нажми E  ")
    print(e)
    cookie = {'name': 'foo', 'value': 'bar'}
    driver.add_cookie(cookie)
    all_cookies = driver.get_cookies()

def openSetting(URL):
    driver.get(URL)
    try:
       el = WebDriverWait(driver, 15).until(lambda driver : driver.find_element_by_xpath(xpath_1))
       print("OK!")
    except Exception:
        driver.implicitly_wait(20)
        print("wait")
    finally:
        print("finaly")
    print('open Url OK')
    # нажимаем Дополнительные настройки
    WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath(xpath_1)).click()
    time.sleep(2)
    # нажимает Исключение IP адресов
    WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath(xpath_2)).click()
    time.sleep(2) # Список IP
    textArea = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(xpath_3))
    print("add IP 1")
    textArea.send_keys(Keys.ENTER)
    textArea.send_keys('37.73.241.179')
    driver.find_element_by_xpath(xpathSave).click()
    print("openSetting()  OK")

def add_Ban_IP():
    # нажимает Исключение IP адресов
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(xpath_5)).click()
    textArea = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(xpath_3))
#    print("add IP")
    textArea.send_keys(Keys.ENTER)
    textArea.send_keys(IP)
    driver.find_element_by_xpath(xpathSave).click()
#    print("OK add IP")

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
                if (find_url.find("gclid") >= 0):   #  gclid
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
     initAndLogin()
     print(1)
     while worker_flag:
        print(2)
        try:
            print(3)
            driver.switch_to.window(driver.window_handles[0])
            openSetting(urlTelRu49)
            driver.switch_to.window(driver.window_handles[1])
            openSetting(urlKomRu34)
            while True:
                while not q2.empty():
                    IP = q2.get()
                    brouser = q2.get()
                    mycol_tvremBanedToday.update_one({"IP" : IP}, {"$set": {"IP": IP}}, upsert = True )
                    brouser_str = str(brouser)
                    if (brouser_str.find("Linux") >= 0):
                        driver.switch_to.window(driver.window_handles[0])
                        try:
                           add_Ban_IP()
                           print("Linux")
                           driver.find_element_by_xpath(xpathCancel).click()
                        except Exception:
                           print("ER add IP")
                           driver.find_element_by_xpath(xpathCancel).click()
                           continue
                    elif (brouser_str.find("iPhone") >= 0):
                        driver.switch_to.window(driver.window_handles[0])
                        try:
                           add_Ban_IP()
                           print("iPhone")
                        except Exception:
                           print("ER add IP")
                           driver.find_element_by_xpath(xpathCancel).click()
                           continue
                    elif (brouser_str.find("Windows") >= 0):
                        driver.switch_to.window(driver.window_handles[1])
                        try:
                           add_Ban_IP()
                           print("Windows")
                        except Exception:
                           print("ER add IP")
                           driver.find_element_by_xpath(xpathCancel).click()
                           continue
                    else:
                       print("X3")

        except Exception:
            print(3, 'no_Дополнительные настройки')
#             driver.quit()
            time.sleep(3)
            continue

driver = webdriver.Chrome(executable_path='C:\chromedriver.exe')
# Открыть новую пустую вкладку
driver.execute_script("window.open('','_blank');")
# переключиться на новую вкладку (с индексом 1)
#driver.switch_to.window(driver.window_handles[1])
# вернуться на предыдущую вкладку (с индексом 0)
driver.switch_to.window(driver.window_handles[0])

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
