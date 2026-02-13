import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC

from pages.payment_page import PaymentPage


class PremiumPage(BasePage):
    URL = BasePage.BASE_URL + "/premium"
    TITLE = 'Битва Покемонов'

    PREMIUM_MAIN_PAGE = (By.CLASS_NAME, "k_page_main_premium")
    PREMIUM_DAYS_INPUT = (By.CLASS_NAME, "k_input_days")
    BUY_PREMIUM_BUTTON_ACTIVE = (By.CSS_SELECTOR, ".k_buy_premium.active")
    PREMIUM_ACTIVATED = (By.CLASS_NAME, "k_title_premium")
    CANCEL_PREMIUM_BUTTON = (By.CLASS_NAME, "k_cansel_premium")
    CANCEL_PREMIUM_BUTTON_NEXT = (By.CLASS_NAME, "k_cansel_go_premium")
    PREMIUM_CANCELLED_TITLE = (By.XPATH, "//div[contains(@class, 'k_pre_title_premium') and text()='Вы отменили подписку :(']")
    COST_DAYS = (By.CLASS_NAME, "k_skidka_premium")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Проверяем загрузку страницы премиума")
    def should_be_loaded(self):
        self.check_visible(self.PREMIUM_MAIN_PAGE)

    @allure.step("Дожидаемся что скидка полностью видна")
    def wait_discount_visible(self):
        self.wait.until(
            lambda d: d.find_element(*self.COST_DAYS).get_attribute("style").strip() == ""
        )

    @allure.step("Переходим к оплате")
    def go_to_payment(self):
        days_input = self.find(self.PREMIUM_DAYS_INPUT)
        days_input.send_keys("1")
        self.click(self.BUY_PREMIUM_BUTTON_ACTIVE)

    @allure.step("Покупаем Премиум")
    def buy_premium(self, card_details=None):
        self.go_to_payment()

        payment_page = PaymentPage(self.driver)
        payment_page.should_be_loaded()
        payment_page.complete_payment(card_details=card_details)

    def is_premium_active(self): # не обязательно, пригодится если расширять фикстуры подготовки тестов покупки/отмены
        return self.driver.find_elements(*self.PREMIUM_ACTIVATED)

    @allure.step("Проверяем что Премиум активен")
    def check_premium_active(self):
        self.wait.until(EC.text_to_be_present_in_element(self.PREMIUM_ACTIVATED, "Премиум успешно подключен!"))

    @allure.step("Отменяем Премиум")
    def cancel_premium(self):
        self.click(self.CANCEL_PREMIUM_BUTTON)
        self.click(self.CANCEL_PREMIUM_BUTTON_NEXT)
        self.find(self.PREMIUM_CANCELLED_TITLE)

    @allure.step("Проверяем стоимость Премиума")
    def check_premium_days_cost(self, days, cost):
        days_input = self.find(self.PREMIUM_DAYS_INPUT)
        days_input.send_keys(days)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, f'//span[text()="по {cost} ₽/день"]')))
