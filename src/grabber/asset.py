from selenium import webdriver
import time

class Asset:
    def __init__(self, **kwargs):
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.driver = webdriver.Chrome()

    def sleep(self, range):
        time.sleep(range)

if __name__ == '__main__':
    scraper = asset()