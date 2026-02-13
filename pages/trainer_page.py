import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class TrainerPage(BasePage):
    TITLE = 'Битва Покемонов'
    BUY_PREMIUM_BUTTON = (By.CLASS_NAME, "k_cart_trainer_premium")
    ACHIEVEMENT_BEGINNING = (By.CSS_SELECTOR, ".beginning-icon.active")
    TRAINER_STATS = (By.CLASS_NAME, "single_page_body_content_inner_box")
    TRAINER_CHAMPION_PREMIUM_BLOCK = (By.CLASS_NAME, "single_page_body_content_title_text")
    POKEBALLS_AMOUNT = (By.XPATH, "//span[text()='Покеболы']/following-sibling::span")
    LEVEL_AMOUNT = (By.XPATH, "//span[text()='Уровень']/following-sibling::span")
    SLIDE_POINTS = (By.CLASS_NAME, "single_page_body_content_inner_top_list_attr_one_slide_i")


    def __init__(self, driver):
        super().__init__(driver)
        self.URL = BasePage.BASE_URL + f"/trainer/{os.getenv("TEST_TRAINER_ID")}"
        self.TRAINER_CARD_ID = (By.XPATH, f"//div[@class='copy_number_id' and text()='{os.getenv("TEST_TRAINER_ID")}']")

    @allure.step("Проверяем загрузку страницы тренера")
    def should_be_loaded(self):
        self.check_visible(self.TRAINER_CARD_ID)

    @allure.step("Переходим к покупке Премиума")
    def go_to_buy_premium(self):
        self.check_clickable(self.BUY_PREMIUM_BUTTON).click()
        wait = WebDriverWait(self.driver, 2)
        wait.until(EC.url_to_be(f"{self.BASE_URL}/premium"))
