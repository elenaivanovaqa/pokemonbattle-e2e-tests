from pages.pokemons_page import PokemonsPage
from pages.premium_page import PremiumPage
from pages.trainer_page import TrainerPage
from pages.payment_page import PaymentPage
import pytest
from data.test_card_data import CARD_CVV, CARD_NUMBER_INVALID, CARD_DATE_INVALID, CARD_CVV_INVALID, CARD_CVV_INSUFFICIENT


def test_main_page_to_trainer_page(driver, authorized_user):
    pokemons_page = PokemonsPage(driver)
    pokemons_page.open_page()
    pokemons_page.should_be_loaded()
    pokemons_page.go_to_trainer_page()

    trainer_page = TrainerPage(driver)
    trainer_page.should_be_loaded()
    assert driver.title == trainer_page.TITLE

def test_go_to_premium(driver, authorized_user):
    trainer_page = TrainerPage(driver)
    trainer_page.open_page()
    trainer_page.should_be_loaded()
    trainer_page.go_to_buy_premium()

    premium_page = PremiumPage(driver)
    premium_page.should_be_loaded()

@pytest.mark.no_headless
def test_achievement_active(driver, authorized_user):
    trainer_page = TrainerPage(driver)
    trainer_page.open_page()
    trainer_page.should_be_loaded()
    trainer_page.check_visible(trainer_page.ACHIEVEMENT_BEGINNING)

def test_buy_premium(driver, cancel_premium, authorized_user):
    premium_page = PremiumPage(driver)
    premium_page.open_page()
    premium_page.should_be_loaded()

    premium_page.buy_premium()
    payment_page = PaymentPage(driver)
    payment_page.go_back()
    premium_page.check_premium_active()

def test_cancel_premium(driver, enable_premium, authorized_user):
    premium_page = PremiumPage(driver)
    premium_page.open_page()
    premium_page.should_be_loaded()

    premium_page.cancel_premium()
    premium_page.open_page()
    assert not premium_page.is_premium_active() # или отдельный метод проверки что премиум отключен


@pytest.mark.parametrize("days,cost", [(1,100), (30, 95), (180, 90), (365, 85)])
def test_premium_costs(driver, cancel_premium, authorized_user, days, cost):
    """Дополнительное задание урока 1, пункт 1"""
    premium_page = PremiumPage(driver)
    premium_page.open_page()
    premium_page.should_be_loaded()
    premium_page.check_premium_days_cost(days, cost)


@pytest.mark.no_headless
def test_card_validation(driver, cancel_premium, authorized_user):
    """Дополнительное задание урока 1, пункт 2"""
    premium_page = PremiumPage(driver)
    premium_page.open_page()
    premium_page.should_be_loaded()
    premium_page.go_to_payment()
    payment_page = PaymentPage(driver) # нужно открывать именно через страницу покупки Премиума или Аватара, чтобы не появилось ошибки "Товар не найден"
    payment_page.open_page()
    payment_page.should_be_loaded()
    payment_page.enter_card_details(card_number=CARD_NUMBER_INVALID, card_date=CARD_DATE_INVALID)
    payment_page.check_visible(payment_page.INVALID_CARD_NUMBER_ERROR)
    payment_page.check_visible(payment_page.INVALID_CARD_DATE_ERROR)

@pytest.mark.parametrize("scenario,cvv", [("При оплате произошла ошибка", CARD_CVV_INSUFFICIENT), ("При оплате произошла ошибка", CARD_CVV_INVALID), ("Покупка прошла успешно", CARD_CVV)]) # можно и без параметризации, например перебор вариантов внутри теста циклом
def test_buy_premium_with_errors(driver, cancel_premium, authorized_user, scenario, cvv):
    """Дополнительное задание урока 1, пункт 3 (расширение обязательного теста)"""
    premium_page = PremiumPage(driver)
    premium_page.open_page()
    premium_page.should_be_loaded()

    premium_page.buy_premium({"card_cvv": cvv})
    payment_page = PaymentPage(driver)
    assert payment_page.get_payment_result() == scenario
    payment_page.go_back()
    if scenario == "Покупка прошла успешно": # такое или любое другое условие ветвления сценариев внутри теста - проверяем что Премиум подключается только когда оплата успешна
        premium_page.check_premium_active()
    else:
        assert not premium_page.is_premium_active() # проверяем что вернулись на предыдущий экран, а не на экран успеха покупки Премиума