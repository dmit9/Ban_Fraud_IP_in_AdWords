import pymongo
import paho.mqtt.client as paho
import threading
from queue import Queue
import datetime
import time
from tkinter import *
from tkinter import BOTH, END, HORIZONTAL, Tk, scrolledtext, ttk
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
urlLogin = 'https://accounts.google.com/signin'
urlCompany = "https://ads.google.com/aw/campaigns?ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001"
urlTel = 'https://ads.google.com/aw/settings/campaign/search?campaignId=98795004&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001'
urlTelRu = 'https://ads.google.com/aw/settings/campaign/search?campaignId=1699363337&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001'
urlTelRu49 = 'https://ads.google.com/aw/settings/campaign/search?campaignId=1636077101&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001'
urlTelRu39 = 'https://ads.google.com/aw/settings/campaign/search?campaignId=2001143663&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001'
urlTelOpt39 = 'https://ads.google.com/aw/settings/campaign/search?campaignId=1825915186&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001'
urlTelOpt49 = 'https://ads.google.com/aw/settings/campaign/search?campaignId=1740531111&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001'
urlTelOpt34 = 'https://ads.google.com/aw/settings/campaign/search?campaignId=1742888292&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001'
urlKomRu43 = 'https://ads.google.com/aw/settings/campaign/search?campaignId=1620167217&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001'
urlKomRu39 = 'https://ads.google.com/aw/settings/campaign/search?campaignId=1735226790&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001'
urlKomOpt39 = 'https://ads.google.com/aw/settings/campaign/search?campaignId=1643384377&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001'
urlKomRu34 = 'https://ads.google.com/aw/settings/campaign/search?campaignId=1644471505&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001'
urlKomOpt34 = 'https://ads.google.com/aw/settings/campaign/search?campaignId=1619439315&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001'
urlTelDict = {'телеф_34_опт': urlTelOpt34, 'телеф_49_опт': urlTelOpt49, 'телеф_39_опт': urlTelOpt39,'телеф_49_ручн': urlTelRu49,'телеф_39_ручн': urlTelRu39, 'телеф': urlTel, 'телеф_ручн': urlTelRu}
urlKomDict = {'комп_34_ручн': urlKomRu34, 'комп_34_опт': urlKomOpt34, 'комп_39_ручн': urlKomRu39, 'комп_43_ручн': urlKomRu43, 'комп_39_ опт': urlKomOpt39}
xpathLogEmail = "//*[@id='Email']"
xpathLogEmailBtn = "//*[@id='next']"
xpathLogPassw = "//*[@id='Passwd']"
xpathLogPasswBtn = "//*[@id='signIn']"
xpathSetting =  "//*[@id='cmExtensionPoint-id']//material-button//span"
xpathTextArea = "//*[@id='cmExtensionPoint-id']//textarea"
xpathBanIP = "//*[@id='cmExtensionPoint-id']//ip-exclusions/material-expansionpanel"
xpathSave = "//*[@id='cmExtensionPoint-id']//ip-exclusions/material-expansionpanel//material-yes-no-buttons/material-button[1]/material-ripple"
xpathCancel = "//*[@id='cmExtensionPoint-id']//ip-exclusions/material-expansionpanel//material-yes-no-buttons/material-button[2]/material-ripple"
xpathTableRow1 = "//*[@id='cmExtensionPoint-id']//div[2]//a"
xpathTableRow2 = "//*[@id='cmExtensionPoint-id']//div[3]//a"
xpathTableRow3 = "//*[@id='cmExtensionPoint-id']//div[4]//a"
xpathTableRow4 = "//*[@id='cmExtensionPoint-id']//div[5]//a"
#xpathSave = "//*[@id='cmExtensionPoint-id']//material-button[1]/material-ripple"
#xpathCancel = "//*[@id='cmExtensionPoint-id']//material-button[2]/material-ripple"
def initAndLogin():
    driver.set_window_size(500, 700)
    driver.get(urlLogin)
    elem = WebDriverWait(driver, 10).until(lambda driver : driver.find_elements_by_id("identifierId"))
    elem[0].send_keys(login)
#    driver.find_element_by_xpath("//*[@id='identifierNext']/content/span").click()
    driver.find_element_by_xpath("// *[ @ id = 'identifierNext'] / span / span").click()
    time.sleep(4)
    elem = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath("//*[@id='password']//input"))
    elem.send_keys(passw)
#    driver.find_element_by_xpath("//*[@id='passwordNext']/content/span").click()
    driver.find_element_by_xpath("// *[ @ id = 'passwordNext'] / span / span").click()
    time.sleep(25)
    # while inputValue != 1:
    #     labelConsole['text'] = "Нажми Login"
    #     time.sleep(2)
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

def changeURL(URL):
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


def add_Ban_IP():
    try:
        driver.find_element_by_xpath(xpathSave).size['width'] != 0  # Проверка на наличие кнопки Сохранить
        print("кнопка Сохранить", driver.find_element_by_xpath(xpathSave).size['width'])
        driver.find_element_by_xpath(xpathSave).click()             # Усли есть, то кликнуть
    except:
        labelConsole['text'] = "OK"
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
    elif message.topic=="name":
        global name
        name=(str(message.payload.decode("utf-8")))
        print(name)
    elif message.topic=="comment":
        global comment
        comment=(str(message.payload.decode("utf-8")))
        print(comment)
    elif message.topic=="brouser":
        global brouser
        brouser=(str(message.payload.decode("utf-8")))
        mydict = {"IP": IP, "time": time, "date":date, "url": url, "page": page, "site": site, "brouser": brouser }
        q.put(mydict)   # очередь для worker

def worker():   # обработка пришедших с сервера данных о посетителях сайта
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
                find_url = str(mydict["url"])
                br = mycol.find({"brouser" : brouser}, {"repIP" : 1, "repBr": 1, "IP": 1, "date": 1, "time": 1, "brouser": 1 })
                ip = mycol.find({"IP" : IP}, {"repIP" : 1,  "repBr": 1, "IP": 1, "date": 1, "time": 1, "brouser": 1 })
                request = ['gclid'] # , 'onas'
                if any(c in find_url for c in request):   #  Если пришел из поиска Гугл gclid
                    q2.put(IP)      # передаём в очередь для worker2
                    q2.put(brouser)
                    for x in br:
                        count_repit_brouser = count_repit_brouser + 1  # проверяем есть ли в базе такой brouser и сколько повторов
                        if (count_repit_brouser >= 1):
                            mycol.update_one({"_id" : x["_id"]}, { "$set": {"repBr" : count_repit_brouser}})
                    for y in ip:
                        count_repit_ip = count_repit_ip + 1  # проверяем есть ли в базе такой ip и сколько повторов
                        if (count_repit_ip >= 1):
                            mycol.update_one({"_id" : y["_id"]}, { "$set": {"repIP" : count_repit_ip}})
                    print(mydict["time"], "  ", brouser)
                    print("Повторов =", count_repit_brouser, "        IP =",  count_repit_ip, IP )
                    labelIP['text'] = (mydict["time"] + ' Повторов = ' + str(count_repit_brouser) + '    IP = ' + str(count_repit_ip),  str(IP))
                    scrollTextOut(brouser)
            except Exception as e:
                print("problem with logging ",e)
                continue

def worker2():  # работа с браузером
     initAndLogin()
     driver.switch_to.window(driver.window_handles[1])
     driver.get(urlCompany)
     row1 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(xpathTableRow1))
     row2 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(xpathTableRow2))
     rows = [row1, row2]
     for row in rows:
         for key in urlKomDict:
             if(row.text == key):
                urlKo = urlKomDict[key]
         for key in urlTelDict:
             if(row.text == key):
                 urlTe = urlTelDict[key]
     print(row1.text)
     print(row2.text)
#     urlTe = urlTel
#     urlKo = urlKomRu39
#     initAndLogin()
#     print("init")
     labelConsole['text'] = "init"
     while worker_flag:
        try:
            labelConsole['text'] = "tel", urlTe
            labelConsole['text'] = "ko", urlKo
            driver.switch_to.window(driver.window_handles[0])  # вернуться на предыдущую вкладку (с индексом 0)
            openSetting(urlTe)
            driver.switch_to.window(driver.window_handles[2])  # переключиться на новую вкладку (с индексом 1)
            openSetting(urlKo)
            while True:
                if q3.empty() != True:
                    urlChangeFlag = q3.get()    # очередь для смены url рабочей компании из интерфейса пользователя
                    if (urlChangeFlag == "Tel"):
                        urlTe = q3.get()
                        driver.switch_to.window(driver.window_handles[0])  # вернуться на предыдущую вкладку (с индексом 0)
                        changeURL(urlTe)
                    elif (urlChangeFlag == "Ko"):
                        urlKo = q3.get()
                        driver.switch_to.window(
                        driver.window_handles[2])  # переключиться на новую вкладку (с индексом 1)
                        changeURL(urlKo)

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
                        elif (brouser_str.find("Windows") >= 0):  #  Если пришел с компа
                            driver.switch_to.window(driver.window_handles[2])
                            add_Ban_IP()
                        else:                  #  Если пришел с ХЗ чего...
                            print("X3")
                except Exception as e:
                    print("ER add IP", e)
                    q2.put(IP)      #  Если ощибра добавления IP в бан, то сохраняем для повторного добавления
                    q2.put(brouser)
                    labelConsole['text'] = "break"
#                    print("break")
                    break

        except Exception as e:
            print(3, 'no_Дополнительные настройки', e)
            continue

def click_btnTel():         #  Если нажали кнопку
    btnTel.config(fg="red")     # меняем цвет текста
    btnTelRu.config(fg="black")
    btnTelOpt39.config(fg="black")
    btnTel39.config(fg="black")
    btnTel49.config(fg="black")
    btnTelOpt49.config(fg="black")
    btnTelOpt34.config(fg="black")
    urlTe = urlTel              # меняем url рабочей компании
    urlChangeFlag = "Tel"
    q3.put(urlChangeFlag)
    q3.put(urlTe)               # отправляем в работу браузеру
def click_btnTelRu():
    btnTelRu.config(fg="red")
    btnTel.config(fg="black")
    btnTelOpt39.config(fg="black")
    btnTel39.config(fg="black")
    btnTel49.config(fg="black")
    btnTelOpt49.config(fg="black")
    btnTelOpt34.config(fg="black")
    urlTe = urlTelRu
    urlChangeFlag = "Tel"
    q3.put(urlChangeFlag)
    q3.put(urlTe)
def click_btnTel49():
    btnTel49.config(fg="red")
    btnTelOpt49.config(fg="black")
    btnTelOpt39.config(fg="black")
    btnTel39.config(fg="black")
    btnTelRu.config(fg="black")
    btnTel.config(fg="black")
    btnTelOpt34.config(fg="black")
    urlTe = urlTelRu49
    urlChangeFlag = "Tel"
    q3.put(urlChangeFlag)
    q3.put(urlTe)
def click_btnTel39():
    btnTel39.config(fg="red")
    btnTel49.config(fg="black")
    btnTelOpt49.config(fg="black")
    btnTelOpt39.config(fg="black")
    btnTelRu.config(fg="black")
    btnTel.config(fg="black")
    btnTelOpt34.config(fg="black")
    urlTe = urlTelRu39
    urlChangeFlag = "Tel"
    q3.put(urlChangeFlag)
    q3.put(urlTe)
def click_btnTelOpt49():
    btnTelOpt49.config(fg="red")
    btnTelOpt39.config(fg="black")
    btnTel39.config(fg="black")
    btnTelRu.config(fg="black")
    btnTel49.config(fg="black")
    btnTel.config(fg="black")
    btnTelOpt34.config(fg="black")
    urlTe = urlTelOpt49
    urlChangeFlag = "Tel"
    q3.put(urlChangeFlag)
    q3.put(urlTe)
def click_btnTelOpt39():
    btnTelOpt39.config(fg="red")
    btnTel39.config(fg="black")
    btnTelOpt49.config(fg="black")
    btnTelRu.config(fg="black")
    btnTel49.config(fg="black")
    btnTel.config(fg="black")
    btnTelOpt34.config(fg="black")
    urlTe = urlTelOpt39
    urlChangeFlag = "Tel"
    q3.put(urlChangeFlag)
    q3.put(urlTe)
def click_btnTelOpt34():
    btnTelOpt34.config(fg="red")
    btnTelRu.config(fg="black")
    btnTelOpt39.config(fg="black")
    btnTel39.config(fg="black")
    btnTelOpt49.config(fg="black")
    btnTel49.config(fg="black")
    btnTel.config(fg="black")
    urlTe = urlTelOpt34
    urlChangeFlag = "Tel"
    q3.put(urlChangeFlag)
    q3.put(urlTe)
def click_btnKom34():
    btnKom34.config(fg="red")
    btnKomOpt34.config(fg="black")
    btnKom39.config(fg="black")
    btnKomOpt39.config(fg="black")
    btnKom43.config(fg="black")
    urlKo = urlKomRu34
    urlChangeFlag = "Ko"
    q3.put(urlChangeFlag)
    q3.put(urlKo)
def click_btnKomOpt34():
    btnKomOpt34.config(fg="red")
    btnKom34.config(fg="black")
    btnKom39.config(fg="black")
    btnKomOpt39.config(fg="black")
    btnKom43.config(fg="black")
    urlKo = urlKomOpt34
    urlChangeFlag = "Ko"
    q3.put(urlChangeFlag)
    q3.put(urlKo)
def click_btnKom39():
    btnKom39.config(fg="red")
    btnKomOpt39.config(fg="black")
    btnKom34.config(fg="black")
    btnKomOpt34.config(fg="black")
    btnKom43.config(fg="black")
    urlKo = urlKomRu39
    urlChangeFlag = "Ko"
    q3.put(urlChangeFlag)
    q3.put(urlKo)
def click_btnKomOpt39():
    btnKomOpt39.config(fg="red")
    btnKom39.config(fg="black")
    btnKom34.config(fg="black")
    btnKomOpt34.config(fg="black")
    btnKom43.config(fg="black")
    urlKo = urlKomOpt39
    urlChangeFlag = "Ko"
    q3.put(urlChangeFlag)
    q3.put(urlKo)
def click_btnKom43():
    btnKom43.config(fg="red")
    btnKom39.config(fg="black")
    btnKomOpt39.config(fg="black")
    btnKom34.config(fg="black")
    btnKomOpt34.config(fg="black")
    urlKo = urlKomRu43
    urlChangeFlag = "Ko"
    q3.put(urlChangeFlag)
    q3.put(urlKo)

def click_btnLogin():
    global inputValue
    inputValue = 1

def confirmExit():
    root.quit()
    root.destroy()

def scrollTextOut(txt):
    console.configure(state='normal')  # enable insert
    console.insert(END, txt + '\n')
    console.yview(END)  # autoscroll
    console.configure(state='disabled')  # disable editing

driver = webdriver.Chrome(executable_path = 'C:\chromedriver.exe')
# Открыть новую пустую вкладку
driver.execute_script("window.open('','_blank');")
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
root.title("банер по IP")
root.geometry("1200x150+20+800")

btnTel = Button(text="Tel", padx="20", pady="8",command = click_btnTel)
btnTel.place(x=10, y=5,height=30, width=50)
btnTelRu = Button(text="TelRu", padx="20", pady="8",command = click_btnTelRu)
btnTelRu.place(x=70, y=5,height=30, width=50)
btnTel49 = Button(text="Tel49", padx="20", pady="8",command = click_btnTel49)
btnTel49.place(x=140, y=5,height=30, width=50)
btnTelOpt49 = Button(text="TelOp49", padx="20", pady="8",command = click_btnTelOpt49)
btnTelOpt49.place(x=210, y=5,height=30, width=50)
btnTel39 = Button(text="Tel39", padx="20", pady="8",command = click_btnTel39)
btnTel39.place(x=280, y=5,height=30, width=50)
btnTelOpt39 = Button(text="TelOp39", padx="20", pady="8",command = click_btnTelOpt39)
btnTelOpt39.place(x=350, y=5,height=30, width=50)
btnTelOpt34 = Button(text="TelOp34", padx="20", pady="8",command = click_btnTelOpt34)
btnTelOpt34.place(x=420, y=5,height=30, width=50)
btnKom34 = Button(text="Kom34", padx="20", pady="8",command = click_btnKom34)
btnKom34.place(x=490, y=5,height=30, width=50)
btnKomOpt34 = Button(text="KomOp34", padx="20", pady="8",command = click_btnKomOpt34)
btnKomOpt34.place(x=560, y=5,height=30, width=50)
btnKom39 = Button(text="Kom39", padx="20", pady="8",command = click_btnKom39)
btnKom39.place(x=630, y=5,height=30, width=50)
btnKomOpt39 = Button(text="KomOp39", padx="20", pady="8",command = click_btnKomOpt39)
btnKomOpt39.place(x=700, y=5,height=30, width=50)
btnKom43 = Button(text="Kom43", padx="20", pady="8",command = click_btnKom43)
btnKom43.place(x=770, y=5,height=30, width=50)
btnLogin = Button(text="Login", padx="20", pady="18",command = click_btnLogin)
btnLogin.place(x=870, y=5,height=30, width=50)

labelIP = Label(root,text = "IP")
labelIP.place(x=10, y=40)
labelConsole = Label(root,text = "Print")
labelConsole.place(x=300, y=40)
console = scrolledtext.ScrolledText(root, state='disable')
console.place(x=10, y=60, width  = 1190)

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
