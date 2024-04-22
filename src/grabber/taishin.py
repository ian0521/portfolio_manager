from asset import Asset
import base64
import ddddocr
import argparse

class Taishin(Asset):
    def __init__(self, arg):
        super().__init__(arg)

    def login(self):
        self.driver.get("https://richart.tw/WebBank/users/login?lang=zh-tw")
        self.sleep(5)
        
        id = self.driver.find_element(
            "xpath",
            "//*[@id='userId']/input"
        )
        id.send_keys(self.id)

        username = self.driver.find_element(
            "xpath",
            "//*[@id='userName']/input"
        )
        username.send_keys(self.username)
 
        password = self.driver.find_element(
            "xpath",
            "/html/body/app-root/div/app-users/div/app-login/main/div/div[1]/div/div[2]/div[1]/div[1]/form/div[1]/div/div[3]/div/input"
        )
        password.send_keys(self.password)

        catch = ""
        while not catch or not self.check_num(catch):
            img = self.driver.find_element(
                "xpath",
                "/html/body/app-root/div/app-users/div/app-login/main/div/div[1]/div/div[2]/div[1]/div[1]/form/div[1]/div/div[4]/div/div[2]/div"
            )
            img.screenshot("code.png")
            ocr = ddddocr.DdddOcr()
            with open("code.png", "rb") as fp:
                image = fp.read()
            catch = ocr.classification(image)
        code = self.driver.find_element(
            "xpath",
            "/html/body/app-root/div/app-users/div/app-login/main/div/div[1]/div/div[2]/div[1]/div[1]/form/div[1]/div/div[4]/div/div[1]/div/input"
        )
        code.send_keys(catch)
        self.sleep(3)
        login_button = self.driver.find_element(
            "xpath",
            "/html/body/app-root/div/app-users/div/app-login/main/div/div[1]/div/div[2]/div[1]/div[1]/form/div[2]/button"
        )
        login_button.click()
        self.sleep(3)

    def info(self):
        show_number = self.driver.find_element(
            "xpath",
            "//*[@id='toggleShowAmount']/i[1]"
        )
        show_number.click()

        cash = self.driver.find_element(
            "xpath",
            "//*[@id='first-element-introduction']/div[1]/div[2]/div"
        ).text.replace(",", "").strip()[1:]
        return int(cash)

    def close_driver(self):
        logout_button = self.driver.find_element(
            "xpath",
            "/html/body/app-root/div/app-dashboard/richart-header/header/div/div/nav/div[2]/div/a"
        )
        logout_button.click()
        comfirm_buttom = self.driver.find_element(
            "xpath",
            "/html/body/ngb-modal-window/div/div/app-modal/div[2]/div[2]/button"
        )
        comfirm_buttom.click()
        self.driver.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("USER INFO")
    args = parser.parse_args()
    section = "TAISHIN"
    scraper = Taishin(section)
    scraper.login()
    cash = scraper.info()
    print(f"Total Cash on Taishin: {cash}")
    scraper.close_driver()