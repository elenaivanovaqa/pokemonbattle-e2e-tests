import os

import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class PokemonsPage(BasePage):
    URL = BasePage.BASE_URL
    TITLE = 'Битва Покемонов'
    SEARCH_POKEMON_INPUT = (By.ID, 'filter_type_search_1')

    def __init__(self, driver):
        super().__init__(driver)
        self.TEST_POKEMON_CARD = (By.XPATH, f"//div[@data-id='{os.getenv("TEST_TRAINER_POKEMON_ID")}']")
        self.TRAINER_CARD_ID = (By.XPATH, f"//div[@class='header_card_trainer_id_num' and text()='{os.getenv("TEST_TRAINER_ID")}']")

    @allure.step("Проверяем загрузку страницы списка покемонов")
    def should_be_loaded(self):
        self.check_visible(self.TRAINER_CARD_ID)

    @allure.step("Ищем тестового покемона")
    def search_pokemon(self, search_string: str=os.getenv("TEST_TRAINER_POKEMON_ID")):
        search_input = self.check_clickable(self.SEARCH_POKEMON_INPUT)
        search_input.click()
        search_input.send_keys(search_string)

        found = self.find_all_visible_elements(self.TEST_POKEMON_CARD)
        return found

    @allure.step("Переходим на страницу тренера")
    def go_to_trainer_page(self):
        self.check_clickable(self.TRAINER_CARD_ID).click()
