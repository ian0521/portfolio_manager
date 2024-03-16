from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import argparse
import time
import pandas as pd
from bs4 import BeautifulSoup

class UsStock:
    def __init__(self, username, password, code):
        self.username = username
        self.password = password
        self.code = code
        self.driver = webdriver.Chrome()

    def sleep(self, range):
        time.sleep(range)

    def login(self):
        self.driver.get("https://www.firstrade.com/")
        # login
        login_button = self.driver.find_element(
            "xpath",
            "//*[@id='__next']/div/header/nav/div[2]/a[1]"
        )
        login_button.click()
        self.sleep(1)

        # enter info
        username = self.driver.find_element(
            "xpath",
            "//*[@id='username']"
        )
        username.send_keys(self.username)

        pwd = self.driver.find_element(
            "xpath",
            "//*[@id='password']"
        )
        pwd.send_keys(self.password)

        # login confirmation
        login_confirm_button = self.driver.find_element(
            "xpath",
            "//*[@id='loginButton']"
        )
        login_confirm_button.click()
        self.sleep(3)

        pin_button = self.driver.find_element(
            "xpath",
            "/html/body/div/main/div/div/div[3]/a"
        )
        pin_button.click()

        pin = self.driver.find_element(
            "xpath",
            "//*[@id='pin']"
        )
        pin.send_keys(self.code)
        self.sleep(1)

        login_pin_button = self.driver.find_element(
            "xpath",
            "//*[@id='form-pin']/div[2]/button"
        )
        login_pin_button.click()
        self.sleep(3)
    
    def info(self):
        self.driver.find_element(
            "xpath",
            "//*[@id='myaccount_link']/a"
        ).click()
        self.sleep(3)

        self.driver.find_element(
            "xpath",
            "//*[@id='myaccount_menu']/li[2]/a/span"
        ).click()
        self.sleep(3)

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        elem = soup.find("table", {"id": "positiontable"})
        df = pd.DataFrame()
        data = elem.find("tbody").find_all("tr")
        for row in data:
            dt = {
                "stock": row.find_all("td")[0].text,
                "qty": row.find_all("td")[1].text,
                "price": row.find_all("td")[2].text,
                "change_$": row.find_all("td")[3].text,
                "change_%": row.find_all("td")[4].text,
                "cap": row.find_all("td")[5].text,
                "unit_price": row.find_all("td")[6].text,
                "cost": row.find_all("td")[7].text,
                "pnl": row.find_all("td")[8].text,
                "pnl_%": row.find_all("td")[9].text,
            }
            df = df._append(dt, ignore_index=True)
        
        return df

    def calculate_total_pnl(self, df):
        total_pnl = 0
        for pnl in df["pnl"]:
            value = float(pnl[1:].replace(',', ''))
            if pnl[0] == '+':
                total_pnl += value
            else:
                total_pnl -= value
        return total_pnl
    
    def close_driver(self):
        self.driver.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("USER INFO")
    parser.add_argument("--username", type=str)
    parser.add_argument("--password", type=str)
    parser.add_argument("--code", type=str)
    args = parser.parse_args()

    scraper = UsStock(args.username, args.password, args.code)
    scraper.login()
    account_info = scraper.info()
    print(account_info)
    total_pnl = scraper.calculate_total_pnl(account_info)
    print(f"Total PnL: {total_pnl}")
    print(f"Total PnL %: {round(total_pnl / account_info.cost.str.replace(',', '').astype(float).sum() * 100, 2)}")
    scraper.close_driver()