import os
import time

import allure

from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    URL = f"{BasePage.BASE_URL}/login"
    TITLE = 'Битва Покемонов'

    LOGIN_INPUT = (By.ID, 'k_email')
    PASSWORD_INPUT = (By.ID, 'k_password')
    LOGIN_BUTTON = (By.CLASS_NAME, "k_form_send_auth")
    VERSION = (By.CLASS_NAME, "k_footer_container_version")

    def __init__(self, driver):
        super().__init__(driver)

    def open_page(self):
        self.open(self.URL)

    @allure.step("Проверяем загрузку страницы авторизации")
    def should_be_loaded(self):
        self.check_visible(self.LOGIN_BUTTON)
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(2)

    @allure.step("Авторизуемся тестовым пользователем")
    def login(self, user: str=None, pwd: str=None):
        # Вводим логин и пароль, нажимаем кнопку
        self.driver.find_element(*self.LOGIN_INPUT).send_keys(user or os.getenv('LOGIN'))
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(pwd or os.getenv('PASSWORD'))
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        # time.sleep(2)
