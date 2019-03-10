# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta, date, time as dt_time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

urlG = 'https://accounts.google.com/signin'
urlG2 = 'https://ads.google.com/aw/settings/campaign/search?campaignId=98795004&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001'
xpath_1 = "//*[@id='cmExtensionPoint-id']/base-root/div/div[2]/div[1]/view-loader/search-campaign-settings-view/div/div/construction-layout/construction-layout-engine/div/div/div[11]/material-button/div/span"
xpath_2 = "//*[@id='cmExtensionPoint-id']/base-root/div/div[2]/div[1]/view-loader/search-campaign-settings-view/div/div/construction-layout/construction-layout-engine/div/div/div[11]/div/div[4]/lazy-plugin/div/dynamic-component/ip-exclusions/material-expansionpanel/div/header/div/div[1]/p"
xpath_3 = "//*[@id='cmExtensionPoint-id']/base-root/div/div[2]/div[1]/view-loader/search-campaign-settings-view/div/div/construction-layout/construction-layout-engine/div/div/div[11]/div/div[4]/lazy-plugin/div/dynamic-component/ip-exclusions/material-expansionpanel/div/main/div/div/div/div/div[2]/div/div[1]/material-input/div[1]/div[1]/div/div[2]/textarea"
xpath_4 = "//*[@id='cmExtensionPoint-id']/base-root/div/div[2]/div[1]/view-loader/search-campaign-settings-view/div/div/construction-layout/construction-layout-engine/div/div/div[11]/div/div[4]/lazy-plugin/div/dynamic-component/ip-exclusions/material-expansionpanel/div/main/div/material-yes-no-buttons/material-button[1]/material-ripple"
xpath_5 = "//*[@id='cmExtensionPoint-id']/base-root/div/div[2]/div[1]/view-loader/search-campaign-settings-view/div/div/construction-layout/construction-layout-engine/div/div/div[11]/div/div[4]/lazy-plugin/div/dynamic-component/ip-exclusions/material-expansionpanel/div/header/div/div[2]/div"
login = 'devyatin5@gmail.com'
passw = 'D89devyatin'
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
    driver.find_element_by_xpath("//*[@id='passwordNext']/content/span").click()
    time.sleep(15)
    e = input("нажми E  ")
    print(e)
    cookie = {'name': 'foo', 'value': 'bar'}
    driver.add_cookie(cookie)
#    all_cookies = driver.get_cookies()

def openSetting():
    driver.get(urlG2)
    try:
       el = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath(xpath_1))
       print("OK!")
    except Exception:
        driver.implicitly_wait(20)
        print("wait")
    else:
        print("else")
    finally:
        print("finaly")
    print('open Url')
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
    driver.find_element_by_xpath(xpath_4).click()

def add_Ban_IP():
    return "dfdd"
    # нажимает Исключение IP адресов
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(xpath_5)).click()
    textArea = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(xpath_3))
    print("add IP")
    textArea.send_keys(Keys.ENTER)
    textArea.send_keys(BanedIP)
    driver.find_element_by_xpath(xpath_4).click()
    print("OK add IP")
    return False

driver = webdriver.Chrome(executable_path='C:\chromedriver.exe')
#initAndLogin()
while True:
    try:
#        openSetting()
        while True:
            try:
                print(3)
                add_Ban_IP()
            except Exception:
                print("ER add IP")
                break

    except Exception:
        print(3, 'except no_URL')
#        driver.quit()
        time.sleep(3)
        continue


