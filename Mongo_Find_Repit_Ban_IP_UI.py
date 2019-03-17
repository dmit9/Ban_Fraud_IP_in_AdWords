import pymongo
import paho.mqtt.client as paho
import threading
from queue import Queue
import datetime
import time
from tkinter import *
from datetime import datetime, timedelta, date, time as dt_time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from constants import login, passw

root = Tk()
q = Queue()
q2 = Queue()
q3 = Queue()
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
urlKomRu39 = "https://ads.google.com/aw/settings/campaign/search?campaignId=1735226790&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001"
urlKomRu34 = 'https://ads.google.com/aw/settings/campaign/search?campaignId=1644471505&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001'
xpathSetting =  "//*[@id='cmExtensionPoint-id']//material-button//span"
xpathTextArea = "//*[@id='cmExtensionPoint-id']//textarea"
xpathBanIP = "//*[@id='cmExtensionPoint-id']//ip-exclusions/material-expansionpanel"
xpathSave = "//*[@id='cmExtensionPoint-id']//ip-exclusions/material-expansionpanel//material-yes-no-buttons/material-button[1]/material-ripple"
xpathCancel = "//*[@id='cmExtensionPoint-id']//ip-exclusions/material-expansionpanel//material-yes-no-buttons/material-button[2]/material-ripple"

def initAndLogin():
    driver.set_window_size(500, 700)
    driver.get(urlG)
    elem = WebDriverWait(driver, 10).until(lambda driver : driver.find_elements_by_id("identifierId"))
    elem[0].send_keys(login)
    driver.find_element_by_xpath("//*[@id='identifierNext']/content/span").click()
    elem = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath("//*[@id='password']//input"))
    elem.send_keys(passw)
    driver.find_element_by_xpath("//*[@id='passwordNext']/content/span").click()
    time.sleep(15)
    e = input("нажми E  ")
    print(e)
    cookie = {'name': 'foo', 'value': 'bar'}
    driver.add_cookie(cookie)
    all_cookies = driver.get_cookies()
#    print("Login OK")
    labelConsole['text'] = "Login OK"

def openSetting(URL):
    driver.get(URL)
    try:
       WebDriverWait(driver, 20).until(lambda driver : driver.find_element_by_xpath(xpathSetting))
#       print("open Setting URL OK!")
       labelConsole['text'] = "open Setting URL OK!"
    except Exception as e:
#        print("wait",e)
        labelConsole['text'] = "wait",e
    finally:
        print("finaly")
        labelConsole['text'] = "finaly"
    #    print('open Url OK')
    # нажимаем Дополнительные настройки
    WebDriverWait(driver, 15).until(lambda driver : driver.find_element_by_xpath(xpathSetting)).click()
    # нажимает Исключение IP адресов
    print(1)
    WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath(xpathBanIP)).click()
 # Список IP
    textArea = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(xpathTextArea))
#    print("add IP 1")
    print(2)
    textArea.send_keys(Keys.ENTER)
#    textArea.send_keys('37.73.241.179')
    print(3)
    driver.find_element_by_xpath(xpathCancel).click()     #  кликаем Отмена
    labelConsole['text'] = "openSetting()  OK"
#    print("openSetting()  OK")

def add_Ban_IP():
    try:
        driver.find_element_by_xpath(xpathSave).size['width'] != 0
        print("Size", driver.find_element_by_xpath(xpathSave).size['width'])
        driver.find_element_by_xpath(xpathSave).click()
    except:
        print("No Size")
    # нажимает Исключение IP адресов
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(xpathBanIP)).click()
#    print("click Ban IP")
    textArea = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(xpathTextArea))
#    print("finded TextArea")
    textArea.send_keys(Keys.ENTER)      #  идём в конец списка
    textArea.send_keys(IP)               #   вводим IP
#    print("add IP")
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(xpathSave)).click()  #  кликаем Сохранить
    labelConsole['text'] = "IP is added"
#    print("IP is added")

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
        # if (now.strftime("%H") >= "22"):
        #     mycol_tvremBanedToday.drop()
        #     print("mycol_tvremBanedToday  drop")
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
                if any(c in find_url for c in request):   #  Если пришел из поиска Гугл gclid
                    q2.put(IP)
                    q2.put(brouser)
                    for x in br:
                        count_repit_brouser = count_repit_brouser + 1
                        if (count_repit_brouser >= 1):
                            mycol.update_one({"_id" : x["_id"]}, { "$set": {"repBr" : count_repit_brouser}})
                    for y in ip:
                        count_repit_ip = count_repit_ip + 1
                        if (count_repit_ip >= 1):
                            mycol.update_one({"_id" : y["_id"]}, { "$set": {"repIP" : count_repit_ip}})
                    print(mydict["time"], "  ", brouser)
                    print("Повторов =", count_repit_brouser, "        IP =",  count_repit_ip, IP )
                    labelIP['text'] = (mydict["time"] + ' Повторов = ' + str(count_repit_brouser) + '    IP = ' + str(count_repit_ip),  str(IP))
                    labelBrouser['text'] = brouser
            except Exception as e:
                print("problem with logging ",e)
                continue

def worker2():
     urlTe = urlTel
     urlKo = urlKomRu39
     initAndLogin()
#     print("init")
     labelConsole['text'] = "init"
     while worker_flag:
        try:
            labelConsole['text'] = "tel", urlTe
            labelConsole['text'] = "ko", urlKo
#            print("tel", urlTe)
#            print("ko", urlKo)
            driver.switch_to.window(driver.window_handles[0])  # вернуться на предыдущую вкладку (с индексом 0)
            openSetting(urlTe)
            driver.switch_to.window(driver.window_handles[1])  # переключиться на новую вкладку (с индексом 1)
            openSetting(urlKo)
            while True:
                if q3.empty() != True:
                    urlChangeFlag = q3.get()
                    if (urlChangeFlag == "Tel"):
                        urlTe = q3.get()
                        driver.switch_to.window(driver.window_handles[0])  # вернуться на предыдущую вкладку (с индексом 0)
                        openSetting(urlTe)
                    elif (urlChangeFlag == "Ko"):
                        urlKo = q3.get()
                        driver.switch_to.window(
                        driver.window_handles[1])  # переключиться на новую вкладку (с индексом 1)
                        openSetting(urlKo)

                try:
                    while not q2.empty():
                        IP = q2.get()
                        brouser = q2.get()
                        mycol_tvremBanedToday.update_one({"IP" : IP}, {"$set": {"IP": IP}}, upsert = True )
                        brouser_str = str(brouser)
                        request = ['Linux', 'iPhone']
                        if any(c in brouser_str for c in request): #  Если пришел с телефона
                            driver.switch_to.window(driver.window_handles[0])
                            add_Ban_IP()
 #                           print("Linux")
                        elif (brouser_str.find("Windows") >= 0):  #  Если пришел с компа
                            driver.switch_to.window(driver.window_handles[1])
                            add_Ban_IP()
#                           print("Windows")
                        else:                  #  Если пришел с ХЗ чего...
                            print("X3")
                except Exception as e:
                    print("ER add IP", e)
                    q2.put(IP)
                    q2.put(brouser)
                    labelConsole['text'] = "break"
#                    print("break")
                    break

        except Exception as e:
            print(3, 'no_Дополнительные настройки', e)
#             driver.quit()
            continue

def click_btnTel():
    btnTel.config(text="Tel_ON")
    btnTel49.config(text="Tel49")
    urlTe = urlTel
    urlChangeFlag = "Tel"
    q3.put(urlChangeFlag)
    q3.put(urlTe)
def click_btnTel49():
    btnTel49.config(text="Tel49_ON")
    btnTel.config(text="Tel")
    urlTe = urlTelRu49
    urlChangeFlag = "Tel"
    q3.put(urlChangeFlag)
    q3.put(urlTe)
def click_btnKom34():
    btnKom34.config(text="Kom34_ON")
    btnKom39.config(text="Kom39")
    btnKom43.config(text="Kom43")
    urlKo = urlKomRu34
    urlChangeFlag = "Ko"
    q3.put(urlChangeFlag)
    q3.put(urlKo)
def click_btnKom39():
    btnKom39.config(text="Kom39_ON")
    btnKom34.config(text="Kom34")
    btnKom43.config(text="Kom43")
    urlKo = urlKomRu39
    urlChangeFlag = "Ko"
    q3.put(urlChangeFlag)
    q3.put(urlKo)
def click_btnKom43():
    btnKom43.config(text="Kom43_ON")
    btnKom39.config(text="Kom39")
    btnKom34.config(text="Kom34")
    urlKo = urlKomRu43
    urlChangeFlag = "Ko"
    q3.put(urlChangeFlag)
    q3.put(urlKo)
def click_btnLogin():
    print("E")

def confirmExit():
    root.quit()
    root.destroy()

driver = webdriver.Chrome(executable_path = 'C:\chromedriver.exe')
# Открыть новую пустую вкладку
driver.execute_script("window.open('','_blank');")
# вернуться на предыдущую вкладку (с индексом 0)
driver.switch_to.window(driver.window_handles[0])

t = threading.Thread(target = worker) #start logger
worker_flag = True
#t.start() #start logging thread

t2 = threading.Thread(target = worker2)
worker2_flag = True
#t2.start()

client = paho.Client()
client.on_message = on_message
client.connect(broker)
client.subscribe(Topics)
client.loop_start()

#root = Tk()
root.title("банер IP")
root.geometry("800x200+20+800")

btnTel = Button(text="Tel_ON", padx="20", pady="8",command = click_btnTel)
btnTel.place(x=10, y=5,height=30, width=50)
btnTel49 = Button(text="Tel49", padx="20", pady="8",command = click_btnTel49)
btnTel49.place(x=70, y=5,height=30, width=50)
btnKom34 = Button(text="Kom34_ON", padx="20", pady="8",command = click_btnKom34)
btnKom34.place(x=140, y=5,height=30, width=50)
btnKom39 = Button(text="Kom39", padx="20", pady="8",command = click_btnKom39)
btnKom39.place(x=210, y=5,height=30, width=50)
btnKom43 = Button(text="Kom43", padx="20", pady="8",command = click_btnKom43)
btnKom43.place(x=280, y=5,height=30, width=50)
btnLogin = Button(text="Login", padx="20", pady="18",command = click_btnLogin)
btnLogin.place(x=500, y=5,height=30, width=50)

labelIP = Label(root,text = "IP")
labelIP.place(x=10, y=40)
labelBrouser = Label(root,text = "Brouser")
labelBrouser.place(x=10, y=60)
labelConsole = Label(root,text = "Print")
labelConsole.place(x=10, y=80)

t.start()
t2.start()
root.protocol('WM_DELETE_WINDOW', confirmExit)
root.mainloop()
try:
    while True:
        pass

except KeyboardInterrupt:
    print("interrrupted by keyboard")
    root.destroy()
