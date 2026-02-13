import allure
from selenium.webdriver.common.by import By

from data.test_card_data import CARD_NUMBER, CARD_DATE, CARD_CVV, CARD_HOLDER, SMS_CODE
from pages.base_page import BasePage

class PaymentPage(BasePage):
    URL = BasePage.BASE_URL + "/payment/0"
    TITLE = 'Битва Покемонов'

    PAGE_LOGO = (By.CLASS_NAME, "payment_header_content_logo")
    CARD_NUMBER_INPUT = (By.CLASS_NAME, "card_number")
    INPUT_ERROR = (By.CLASS_NAME, "style_1_base_input_error")
    CARD_DATE_INPUT = (By.CLASS_NAME, "card_date")
    CARD_CSV_INPUT = (By.CLASS_NAME, "card_csv")
    CARD_NAME_INPUT = (By.CLASS_NAME, "card_name")
    PAY_BUTTON = (By.XPATH,
                  "//button[text()='Оплатить' and not(contains(@class, 'disable'))]")
    THREEDS_NUMBER_INPUT = (By.CLASS_NAME, "threeds_number")
    BACK_LINK = (By.CLASS_NAME, "link_back")
    INVALID_CARD_NUMBER_ERROR = (By.XPATH, '//span[text()="Неверный номер карты"]')
    INVALID_CARD_DATE_ERROR = (By.XPATH, '//span[text()="Неверный срок"]')
    PAYMENT_STATUS_TOP_TITLE = (By.CLASS_NAME, 'payment_status_top_title')
    CARD_FORM = (By.CLASS_NAME, "payment_form_card_form")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Проверяем загрузку страницы оплаты")
    def should_be_loaded(self):
        self.check_visible(self.PAGE_LOGO)

    @allure.step("Вводим данные карты")
    def enter_card_details(self, card_number=CARD_NUMBER, card_date=CARD_DATE, card_cvv=CARD_CVV, card_holder=CARD_HOLDER, manual_number=False):
        if manual_number:
            self.type(self.CARD_NUMBER_INPUT, card_number)
        else:
            number_input = self.find(self.CARD_NUMBER_INPUT)
            self.driver.execute_script("arguments[0].value = arguments[1];", number_input, card_number)
        self.find(self.INPUT_ERROR)
        self.type(self.CARD_DATE_INPUT, card_date)
        self.type(self.CARD_CSV_INPUT, card_cvv)
        self.type(self.CARD_NAME_INPUT, card_holder)
        self.check_invisible(self.INPUT_ERROR)

    def wait_error_visible(self):
        self.wait.until(
            lambda d: d.find_element(*self.INPUT_ERROR).get_attribute("style").strip() == ""
        )

    @allure.step("Выполняем оплату")
    def complete_payment(self, card_details=None, sms_code=SMS_CODE): # можно и в один метод, тут нагляднее
        self.enter_card_details(**card_details if card_details else {})
        self.click(self.PAY_BUTTON)

        self.type(self.THREEDS_NUMBER_INPUT, sms_code)
        self.click(self.PAY_BUTTON)

    @allure.step("Получаем результат оплаты")
    def get_payment_result(self):
        return self.check_visible(self.PAYMENT_STATUS_TOP_TITLE).text

    @allure.step("Нажимаем Назад")
    def go_back(self):
        return self.click(self.BACK_LINK)
