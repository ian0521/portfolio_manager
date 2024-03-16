from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
import time
import pandas as pd
from bs4 import BeautifulSoup

class cathy:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()

    def sleep(self, range):
        time.sleep(range)

    def login(self):
        self.driver.get("https://cathaybk.com.tw/MyBank/Quicklinks/Home/Login")
        self.sleep(2)
        check_button = self.driver.find_element(
            "xpath",
            "//*[@id='divSystemLoginMsg']/div/div/div[2]/div[2]/button"
        )
        check_button.click()

        id = self.driver.find_element(
            "xpath",
            "//*[@id='CustID']"
        )
        id.send_keys(self.id)

        uid = self.driver.find_element(
            "xpath",
            "//*[@id='UserIdKeyin']"
        )
        uid.send_keys(self.username)

        pwd = self.driver.find_element(
            "xpath",
            "//*[@id='PasswordKeyin']"
        )
        pwd.send_keys(self.password)

        self.driver.find_element(
            "xpath",
            "//*[@id='divCUBNormalLogin']/div[2]/button"
        ).click()

    def info(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "TD-balance"))
        )
        return int(element.text.replace(',', '').strip())

    def close_driver(self):
        self.driver.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("USER INFO")
    parser.add_argument("--id", type=str)
    parser.add_argument("--username", type=str)
    parser.add_argument("--password", type=str)
    args = parser.parse_args()

    scraper = cathy(args.id, args.username, args.password)
    scraper.login()
    asset = scraper.info()
    print(f"Total Asset on Cathy: {asset}")
    scraper.close_driver()