import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

class BasePage:
    load_dotenv()
    BASE_URL = os.getenv('BASE_URL')
    URL = None

    def __init__(self, driver, timeout=5):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.BASE_URL = os.getenv('BASE_URL')

    def open(self, url: str):
        self.driver.get(url)

    def open_page(self):
        if not self.URL:
            raise Exception("self.URL is not set!")
        else:
            self.open(self.URL)

    def find(self, by_locator: tuple[str, str]):
        """by_locator - это tuple из (by, locator)"""
        return self.wait.until(EC.presence_of_element_located(by_locator))

    def check_visible(self, by_locator: tuple[str, str]):
        target_element = self.wait.until(EC.visibility_of_element_located(by_locator))
        assert target_element.is_displayed(), f"Элемент по локатору {by_locator} не видим!"
        return target_element

    def check_invisible(self, by_locator: tuple[str, str], timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.invisibility_of_element_located(by_locator))

    def find_all_visible_elements(self, by_locator: tuple[str, str]) -> list:
        target_elements = self.wait.until(EC.visibility_of_all_elements_located(by_locator))
        return target_elements

    def check_clickable(self, by_locator: tuple[str, str], element_name="Элемент"):
        try:
            target_element = self.wait.until(EC.element_to_be_clickable(by_locator))
            return target_element
        except Exception:
            assert False, f"{element_name} по локатору {by_locator} не является кликабельным!"

    def click(self, by_locator: tuple[str, str]):
        elem = self.find(by_locator)
        elem.click()
        return elem

    def type(self, by_locator: tuple[str, str], text: str):
        elem = self.find(by_locator)
        elem.clear()
        elem.send_keys(text)
        return elem

    # def screenshot_test(self, locator):
    #     self.driver.get_screenshot_as_png(locator)
    #     assert_snapshot(screenshot, name="homepage")
