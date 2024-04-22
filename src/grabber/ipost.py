from selenium import webdriver
import argparse
from bs4 import BeautifulSoup
import base64
import ddddocr
from asset import Asset


class Ipost(Asset):
    def __init__(self, arg):
        super().__init__(arg)

    def login(self):
        self.driver.get("https://ipost.post.gov.tw/pst/home.html")
        self.sleep(3)
        login_msg = self.driver.find_element(
            "xpath",
            "//*[@id='modal']/div[2]/button"
        )
        login_msg.click()
        id_login = self.driver.find_element(
            "xpath",
            "//*[@id='content_wh']/div[1]/div/ul/li[1]/a"
        )
        id_login.click()

        id = self.driver.find_element(
            "xpath",
            "//*[@id='cifID']"
        )
        id.send_keys(self.id)

        username = self.driver.find_element(
            "xpath",
            "//*[@id='userID_1_Input']"
        )
        username.send_keys(self.username)

        password = self.driver.find_element(
            "xpath",
            "//*[@id='userPWD_1_Input']"
        )
        password.send_keys(self.password)

        catch = ""
        while len(catch) != 4 or not self.check_num(catch):
            img = self.driver.find_element(
                "xpath",
                "//*[@id='tab1']/div[14]/img"
            )
            img.screenshot("code.png")
            ocr = ddddocr.DdddOcr()
            with open("code.png", "rb") as fp:
                image = fp.read()
            catch = ocr.classification(image)
        code = self.driver.find_element(
            "xpath",
            "//*[@id='tab1']/div[11]/input"
        )
        code.send_keys(catch)
        self.sleep(3)
        login_button = self.driver.find_element(
            "xpath",
            "//*[@id='tab1']/div[12]/a"
        )
        login_button.click()
        self.sleep(10)

    def info(self):
        cash = self.driver.find_element(
            "xpath",
            "//*[@id='css_table2']/div[2]/div[3]/span"
        ).text.replace(',', '').strip()
        return int(cash)

    def close_driver(self):
        self.driver.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("USER INFO")
    args = parser.parse_args()
    section = "IPOST"
    scraper = Ipost(section)
    scraper.login()
    cash = scraper.info()
    print(f"Total Cash on Ipost: {cash}")
    scraper.close_driver()