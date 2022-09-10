import os
from unicodedata import name
import time
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta as td
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import string


def asserting(tittle,tim=1000):
    
    tittle = str(tittle)
    
    for y in range(0, tim+1):
        try:
            assert tittle in driver.title
            break
        except:
            time.sleep(0.1)
            pass

def check_exists_by_xpath(driver,xpath):
    try:
        driver.find_element(by=By.XPATH,value=xpath)
    except NoSuchElementException:
        return False
    return True


def check_timer_click(driver,xpath, timer, tes="", click=0, send=0):

    for i in range(0, (timer+1)*2):
        if check_exists_by_xpath(driver=driver,xpath=xpath):
            if click == 1:
                driver.find_element(by=By.XPATH,value=xpath).click()
            if send == 1:
                driver.find_element(by=By.XPATH,value=xpath).send_keys(tes)
            break
        time.sleep(0.5)

def main():
    
    f_name_list = []
    f_price_discount_list = []
    f_price_full_list = []
    link = r"https://www.pichau.com.br/hardware/placa-de-video?page=1"

    driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    driver.get(link)
    NunPages = driver.find_element(by=By.XPATH,value=r'//*[@id="__next"]/main/div[2]/div/div[1]/nav/ul/li[8]/button').text
    try:
        for pages in range(1,int(NunPages)+1):
            driver.get("https://www.pichau.com.br/hardware/placa-de-video?page={}".format(str(pages)))
            list_path = driver.find_elements(by=By.XPATH,value = r'//*[@id="__next"]/main/div[2]/div/div[1]/div[2]/div/a/div/div[2]/h2')
            list_driver_name = [na.text for na in list_path]
            f_name_list.extend(list_driver_name)
            
            list_path = driver.find_elements(by=By.XPATH,value = r"//main/div/div/div/div/div/a/div/div/div/div[1]/div/div")
            list_driver_price = [nb.text.replace("R$","").replace(".","").replace(",",".").replace(" ","") for nb in list_path if "de" not in nb.text]

            for letters in string.ascii_letters+":":
                list_driver_price = [xil.replace(letters,"") for xil in list_driver_price]
            f_price_discount_list.extend(list_driver_price)
            
            list_path = driver.find_elements(by=By.XPATH,value =r"//main/div/div/div/div/div/a/div/div/div/div[3]/div/div")
            list_driver_price_full = [float(nc.text.replace("R$ ","").replace(".","").replace(",",".")) for nc in list_path if "sem juros no cartão" not in nc.text]
            f_price_full_list.extend(list_driver_price_full)
            
            print(len(f_name_list),len(f_price_discount_list),len(f_price_full_list))
            if len(f_name_list) != len(f_price_discount_list):
                break
            
        dtset = pd.DataFrame({"name":f_name_list[:len(f_price_discount_list)],"Price Discounted":f_price_discount_list,"Price Full":f_price_full_list})
        dtset.to_csv("GPU_price.csv",index=False)
        driver.quit()
    except Exception as E:
        print(E)

    
    
    


main()