from asset import Asset
import base64
import ddddocr
import argparse

class Taishin(Asset):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id")

    def check_num(self, catch):
        for idx, val in enumerate(catch):
            if val not in ''.join(str(num) for num in range(10)):
                if val.lower() == 'o':
                    catch = catch[:idx] + '0' + catch[idx+1:]
                else:
                    return False
            return True

    def login(self):
        self.driver.get("https://my.taishinbank.com.tw/TIBNetBank/")
        self.sleep(3)
        
        id = self.driver.find_element(
            "xpath",
            "//*[@id='app']/div/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/div"
        )
        id.send_keys(self.id)

        username = self.driver.find_element(
            "xpath",
            "//*[@id='app']/div/div[2]/div[2]/div[1]/div/div/div[1]/div[3]/div/input"
        )
        username.send_keys(self.username)

        password = self.driver.find_element(
            "xpath",
            "//*[@id='app']/div/div[2]/div[2]/div[1]/div/div/div[1]/div[4]/div/input"
        )
        password.send_keys(self.password)

        catch = ""
        while len(catch) != 6 or self.check_num(catch):
            img = self.driver.find_element(
                "xpath",
                "//*[@id='verify']/div/div/span/img"
            )
            img.screenshot("code.png")
            ocr = ddddocr.classification(img)
            with open("code.png", "rb") as fp:
                image = fp.read()
            catch = ocr.classification(image)
        code = self.driver.find_element(
            "xpath",
            "//*[@id='verify']/div/input"
        )
        code.send_keys(catch)
        self.sleep(3)
        login_button = self.driver.find_element(
            "xpath",
            "//*[@id='loginBtn']"
        )
        login.button.click()
        self.sleep(3)

        notify_button = self.driver.find_element(
            "xpath",
            "//*[@id='__BVID__15___BV_modal_body_']/div[2]/div/button[2]"
        )
        notify_button.click()
        self.sleep(3)

    def info(self):
        cash = int(self.driver.find_element(
            "xpath",
            "//*[@id='app']/div/div[3]/div/div[4]/table/tbody/tr/td[1]"
        ))
        return cash

    def close_driver(self):
        self.driver.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("USER INFO")
    parser.add_argument("--id", type=str)
    parser.add_argument("--username", type=str)
    parser.add_argument("--password", type=str)
    args = parser.parse_args()

    scraper = Taishin(
        id=args.id,
        username=args.username,
        password=args.password
    )
    scraper.login()
    cash = scraper.info()
    print(f"Total Cash on Taishin: {cash}")
    scraper.close()