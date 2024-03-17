from selenium import webdriver
import argparse
import time
import pandas as pd
from bs4 import BeautifulSoup
import base64
import ddddocr

driver = webdriver.Chrome()
driver.get("https://ipost.post.gov.tw/pst/home.html")
time.sleep(3)
login_msg = driver.find_element(
    "xpath",
    "//*[@id='modal']/div[2]/button"
)
login_msg.click()
id_login = driver.find_element(
    "xpath",
    "//*[@id='content_wh']/div[1]/div/ul/li[1]/a"
)
id_login.click()

id = driver.find_element(
    "xpath",
    "//*[@id='cifID']"
)
id.send_keys("ID")

username = driver.find_element(
    "xpath",
    "//*[@id='userID_1_Input']"
)
username.send_keys("USERNAME")

password = driver.find_element(
    "xpath",
    "//*[@id='userPWD_1_Input']"
)
password.send_keys("PWD")

def check_num(catch):
    for idx, val in enumerate(catch):
        if val not in ''.join(str(num) for num in range(10)):
            if val.lower() == 'o':
                catch = catch[:idx] + '0' + catch[idx+1:]
            else:
                return False
    return True

catch = ""
while len(catch) != 4 or not check_num(catch):
    img = driver.find_element(
        "xpath",
        "//*[@id='tab1']/div[14]/img"
    )
    img.screenshot("code.png")
    ocr = ddddocr.DdddOcr()
    with open("code.png", "rb") as fp:
        image = fp.read()
    catch = ocr.classification(image)
    print(catch)
code = driver.find_element(
    "xpath",
    "//*[@id='tab1']/div[11]/input"
)
code.send_keys(catch)
time.sleep(3)
login_button = driver.find_element(
    "xpath",
    "//*[@id='tab1']/div[12]/a"
)
login_button.click()
time.sleep(10)
cash = driver.find_element(
    "xpath",
    "//*[@id='css_table2']/div[2]/div[3]/span"
).text.replace(',', '').strip()
print(int(cash))
driver.close()