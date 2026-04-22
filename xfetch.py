import requests
import os
from bs4 import BeautifulSoup as bs
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager # the import one is important
import time

brave_path = r"C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

options = Options()
options.binary_location = brave_path

service = Service(ChromeDriverManager().install()) # the import ome get the webdriver_manager.chrome
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://x.com/i/flow/login")
time.sleep(7)
print("試運營")
cookie = driver.get_cookie()
driver.get("https://x.com/LimbusCompany_B")
# need to get cookie but i don't know how to do it
print(driver.title)
time.sleep(30)
driver.quit()