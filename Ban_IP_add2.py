# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta, date, time as dt_time
from selenium import webdriver
#driver = webdriver.Firefox(executable_path='C:\geckodriver.exe')
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

url = 'https://accounts.google.com/signin'
url2 = 'https://ads.google.com/aw/settings/campaign/search?campaignId=98795004&ocid=64763724&__c=3808221676&__u=4249769236&authuser=0&__o=cues&lang=uk&loc=21125&device=30001'

login = 'devyatin5@gmail.com'
passw = 'D89devyatin'
BanedIP = ['109.87.22.101','37.73.217.26']

def autoriz(login):
    login_box = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id("identifierId"))

    print(len(login_box))
##    login_box = driver.find_element_by_name("login")
    login_box.send_keys(login)
    password_box = driver.find_element_by_css_selector("form.form-signin > input[name=\"pass\"]")
##    password_box = driver.find_element_by_name("pass")
    password_box.send_keys(passv)
    element = driver.find_element_by_xpath("//button[@type='submit']")
###    element = driver.find_element_by_name("ok")
    element.click()

while True:
    driver = webdriver.Chrome(executable_path='C:\chromedriver.exe')
    driver.set_window_size(500, 700)
    driver.get(url)
    time.sleep(1)
    try:
#        element = driver.find_element_by_xpath("//div...")
        elem = driver.find_elements_by_id("identifierId")
        elem[0].send_keys(login)
        driver.find_element_by_xpath("//*[@id='identifierNext']/content/span").click()
        time.sleep(2)
        elem = driver.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input")
        elem.send_keys(passw)
        time.sleep(20)
        cookie = {'name': 'foo', 'value': 'bar'}
        driver.add_cookie(cookie)
        all_cookies = driver.get_cookies()
        time.sleep(2)
        while True:
            driver.get(url2)
            time.sleep(3)
            print('open Url')
            try:
    # нажимаем Дополнительные настройки
                el = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath("//*[@id='cmExtensionPoint-id']/base-root/div/div[2]/div[1]/view-loader/search-campaign-settings-view/div/div/construction-layout/construction-layout-engine/div/div/div[11]/material-button/div/span"))
                el.click()
                time.sleep(2)
    # нажимает Исключение IP адресов
                el = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath("//*[@id='cmExtensionPoint-id']/base-root/div/div[2]/div[1]/view-loader/search-campaign-settings-view/div/div/construction-layout/construction-layout-engine/div/div/div[11]/div/div[4]/lazy-plugin/div/dynamic-component/ip-exclusions/material-expansionpanel/div/header/div/div[1]/p"))
                el.click()
                time.sleep(2)
    # Список IP
                textArea = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath("//*[@id='cmExtensionPoint-id']/base-root/div/div[2]/div[1]/view-loader/search-campaign-settings-view/div/div/construction-layout/construction-layout-engine/div/div/div[11]/div/div[4]/lazy-plugin/div/dynamic-component/ip-exclusions/material-expansionpanel/div/main/div/div/div/div/div[2]/div/div[1]/material-input/div[1]/div[1]/div/div[2]/textarea"))
                text = textArea.get_attribute('value')


                for i in range(len(BanedIP)):
                    textArea.send_keys(Keys.ENTER)
                    textArea.send_keys(BanedIP[i])


#                print(len(el3), el3)
            except:
                print('log')
                continue
#   //*[@id="passwordNext"]/content/span
        cookie = {'name' : 'foo', 'value' : 'bar'}
        driver.add_cookie(cookie)
        all_cookies = driver.get_cookies()
##        print(all_cookies)
    except:
        print(3, 'no_URL')
#        driver.quit()
        time.sleep(3)
        continue

##    elem = driver.find_element_by_xpath("//button[@type='submit']")

