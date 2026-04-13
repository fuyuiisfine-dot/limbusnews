import requests
import os
from bs4 import BeautifulSoup as bs
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

brave_path = r"C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

options = Options()
options.binary_location = brave_path

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.google.com")
print(driver.title)
driver.quit()

##wrong path 