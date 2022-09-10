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
    driver.get(link) #Opens the automated browser
    NunPages = driver.find_element(by=By.XPATH,value=r'//*[@id="__next"]/main/div[2]/div/div[1]/nav/ul/li[8]/button').text
    #gets the maximun number of pages
    try:
        for pages in range(1,int(NunPages)+1): #Looping to read all pages
            
            driver.get("https://www.pichau.com.br/hardware/placa-de-video?page={}".format(str(pages)))
            
            #-----------get GPU names------------------------------------------------------------------------------------------------------#
            list_path = driver.find_elements(by=By.XPATH,value = r'//*[@id="__next"]/main/div[2]/div/div[1]/div[2]/div/a/div/div[2]/h2') #generate a list with all xpaths
            list_driver_name = [na.text for na in list_path] #extract the text of each xpath
            f_name_list.extend(list_driver_name) #add to the list
            #------------------------------------------------------------------------------------------------------------------------------#
            
            #----------get GPU prices--------------------------------------------------------------------------------------------------------------------------------#
            list_path = driver.find_elements(by=By.XPATH,value = r"//main/div/div/div/div/div/a/div/div/div/div[1]/div/div")
            list_driver_price = [nb.text.replace("R$","").replace(".","").replace(",",".").replace(" ","") for nb in list_path if "de" not in nb.text]
            #filter texts in the GPU value

            for letters in string.ascii_letters+":":
                list_driver_price = [xil.replace(letters,"") for xil in list_driver_price] #filter every latter and : from the prices value
            f_price_discount_list.extend(list_driver_price) #add to the list
            
            list_path = driver.find_elements(by=By.XPATH,value =r"//main/div/div/div/div/div/a/div/div/div/div[3]/div/div")
            list_driver_price_full = [float(nc.text.replace("R$ ","").replace(".","").replace(",",".")) for nc in list_path if "sem juros no cartão" not in nc.text]
            f_price_full_list.extend(list_driver_price_full)
            #--------------------------------------------------------------------------------------------------------------------------------------------------------#
            print(len(f_name_list),len(f_price_discount_list),len(f_price_full_list)) #print the size of each list (name, discounted price and price)
            if len(f_name_list) != len(f_price_discount_list): #if a list has diferent size stops the program
                break
            
        dtset = pd.DataFrame({"name":f_name_list[:len(f_price_discount_list)],"Price Discounted":f_price_discount_list,"Price Full":f_price_full_list}) #unify all lists in a dataframe
        dtset.to_csv("GPU_price.csv",index=False)# save dataframe in csv
        driver.quit() #close the driver browser
    except Exception as E:
        print(E)

    
    
    


main()