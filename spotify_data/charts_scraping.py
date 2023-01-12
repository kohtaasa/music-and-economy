from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--user-data-dir=/Users/kohtaasakura/Library/Application Support/Google/Chrome/")
chrome_options.add_argument("--profile-directory=Profile 2")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("window-size=1920,1080")

webdriver_service = Service("chromedriver/chromedriver")
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
driver.implicitly_wait(10)
driver.get('https://charts.spotify.com/home')
elem = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[2]/div/header/div/div[2]/a[3]')
elem.click()

try:
    fb = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/button[1]')
    fb.click()
    email = driver.find_element(By.XPATH, '//*[@id="email"]')
    email.send_keys('koh.0430.ta@gmail.com')
    password = driver.find_element(By.XPATH, '//*[@id="pass"]')
    password.send_keys('57XHdGb4f8G%RM')
    login = driver.find_element(By.XPATH, '//*[@id="loginbutton"]')
    login.click()
except:
    print('Already logged-in')

time.sleep(10)

date_range = pd.date_range(start='2022-12-23', end='2022-12-28', freq='D')
date_list = [i.strftime('%Y-%m-%d') for i in date_range]

for date in date_list:
    driver.get(f'https://charts.spotify.com/charts/view/regional-us-daily/{date}')
    wait = WebDriverWait(driver, 10)
    download = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[2]/div[3]/div/div/a/button')
    download.click()
    print(f'Downloaded CSV file for {date}')
    time.sleep(1)

print('Downloading Complete')
