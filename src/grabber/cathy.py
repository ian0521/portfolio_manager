from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
from bs4 import BeautifulSoup
from asset import Asset

class Cathy(Asset):
    def __init__(self, arg):
        super().__init__(arg)

    def login(self):
        self.driver.get("https://cathaybk.com.tw/MyBank/Quicklinks/Home/Login")
        self.sleep(1)
        check_button = self.driver.find_element(
            "xpath",
            "//*[@id='divSystemLoginMsg']/div/div/div[2]/div[2]/button"
        )
        if check_button.text:
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
        # cash
        html_cash = self.driver.page_source
        soup_cash = BeautifulSoup(html_cash, "html.parser")
        self.sleep(1)
        check_button = self.driver.find_element(
            "xpath",
            "//*[@id='_Cancel']"
        )
        if check_button.text:
            check_button.click()

        cash = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "TD-balance"))
        ).text.replace(",", "").strip()

        # stock
        self.driver.find_element(
            "xpath",
            "//*[@id='tabFUND']"
        ).click()
        html_stock = self.driver.page_source
        soup_stock = BeautifulSoup(html_stock, "html.parser")
        stock = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "FUND-balance"))
        ).text.replace(",", "").strip()

        return int(cash), int(stock)

    def close_driver(self):
        self.driver.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("USER INFO")
    args = parser.parse_args()
    section = "CATHY"
    scraper = Cathy(section)
    scraper.login()
    cash, stock = scraper.info()
    print(f"Total Cash on Cathy: {cash}")
    print(f"Total Stock on Cathy: {stock}")
    print(f"Total Asset on Cathy: {cash+stock}")
    scraper.close_driver()