'''
Created on Nov 13, 2017

@author: Mily
'''
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time


def init_driver(website):
    #driver = webdriver.Firefox(executable_path=r'C:\Program Files (x86)\geckodriver.exe')
    driver = webdriver.Chrome(executable_path=r'C:\...\chromedriver.exe')
    
    driver.wait = WebDriverWait(driver, 5)
    driver.get(website) #this will refresh the page..
    driver.set_page_load_timeout(30) #give up to 30 seconds to fully load the page
    return driver
 
def scroll_to_bottom(driver):
    SCROLL_PAUSE_TIME = 0.5
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    return
 
def login(driver): 
    login_df = pd.read_excel('C:\...\login_info.xlsx')
    
    user= login_df['email'][0]
    pwd= login_df['password'][0]
    
    driver.find_element_by_id("email").send_keys(user)
    driver.find_element_by_id("pass").send_keys(pwd)
    driver.find_element_by_id("loginbutton").click()
    
    driver.save_screenshot("facebook_login.png")
    
    #--------------------------deal with "Turn on FacebookNotifications" popup
    popup_txt = driver.find_element_by_css_selector("a.layerCancel._4jy0._4jy3._517h._51sy._42ft")
    if (popup_txt.is_displayed()):
        popup_txt.click()
    
    driver.find_element_by_class_name("_1vp5").click() #profile class name changes frequently   
    driver.save_screenshot("facebook_profile.png")
    return
 
 
 
def scroll_to_year(driver,year):
    driver.execute_script("window.scrollTo(0, 90000);") #scroll a bit until hidden element appears
    target = ".uiMenuItem.uiMenuItemRadio.uiSelectorOption a[data-key=year_" + str(year)
    
    el = driver.find_element_by_css_selector(".uiButtonGroupItem.selectorItem.lastItem") #click on recent
    el.click()
    el = driver.find_element_by_css_selector(target)
    el.click()
    
    return
 
 
if __name__ == "__main__":
    website = "http://facebook.com/"
    driver = init_driver(website)
    login(driver)
    scroll_to_bottom(driver)
    scroll_to_year(driver, 2007)

    #driver.quit()
