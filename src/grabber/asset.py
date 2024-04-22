from selenium import webdriver
import time
import configparser

class Asset:
    def __init__(self, arg):
        info = self.information(arg)
        self.username = info.get("username")
        self.password = info.get("password")
        self.code = info.get("code", "")
        self.id = info.get("id")
        self.driver = webdriver.Chrome()

    def information(self, arg):
        cfg = configparser.ConfigParser()
        cfg.read("../config/info.ini")
        info = {}
        for option in cfg.options(arg):
            info[option] = cfg.get(arg, option)
        return info

    def sleep(self, range):
        time.sleep(range)

    def check_num(self, catch):
        for idx, val in enumerate(catch):
            if val not in ''.join(str(num) for num in range(10)):
                if val.lower() == 'o':
                    catch = catch[:idx] + '0' + catch[idx+1:]
                else:
                    return False
        return True

if __name__ == '__main__':
    scraper = asset()