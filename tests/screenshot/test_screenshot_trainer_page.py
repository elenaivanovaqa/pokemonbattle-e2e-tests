import pytest

from data.test_card_data import CARD_NUMBER, CARD_DATE, CARD_CVV, CARD_HOLDER
from pages.payment_page import PaymentPage
from pages.premium_page import PremiumPage
from pages.trainer_page import TrainerPage


@pytest.mark.skip('update screenshots')
@pytest.mark.no_headless
def test_screenshot_trainer_stats(driver, authorized_user, screenshot_test):
    trainer_page = TrainerPage(driver)
    trainer_page.open_page()
    trainer_page.should_be_loaded()
    screenshot_test(driver, element=TrainerPage.TRAINER_STATS, name="trainer_page.png",
                    mask=[TrainerPage.SLIDE_POINTS, TrainerPage.TRAINER_CHAMPION_PREMIUM_BLOCK, TrainerPage.POKEBALLS_AMOUNT, TrainerPage.LEVEL_AMOUNT],
                    threshold=0.05)

@pytest.mark.skip('update screenshots')
@pytest.mark.no_headless
@pytest.mark.parametrize("cost, days", [(100, 1), (95, 31), (90, 181)])
def test_screenshot_premium_cost(driver, cancel_premium, authorized_user, screenshot_test, cost, days):
    premium_page = PremiumPage(driver)
    premium_page.open_page()
    premium_page.should_be_loaded()

    days_input = premium_page.find(premium_page.PREMIUM_DAYS_INPUT)
    days_input.send_keys(days)
    premium_page.find(premium_page.COST_DAYS)
    premium_page.wait_discount_visible()

    screenshot_test(driver, element=premium_page.PREMIUM_MAIN_PAGE, name=f"premium_page_{cost}.png", threshold=0.05)

@pytest.mark.skip('update screenshots')
@pytest.mark.no_headless
@pytest.mark.parametrize("testcase, card_data", [("empty", {}), ("invalid_number", {'number': 1}), ("invalid_date", {"number": CARD_NUMBER, "date": 1}), ("full", {"number": CARD_NUMBER, "date": CARD_DATE, "cvv": CARD_CVV, "holder": CARD_HOLDER})]) # этот тест можно разделить на несколько разных, например на пустую форму и на заполнение валидными/невалидными данными
def test_screenshot_pay_form_conditions(driver, cancel_premium, authorized_user, screenshot_test, testcase, card_data):
    premium_page = PremiumPage(driver)
    premium_page.open_page()
    premium_page.should_be_loaded()
    premium_page.go_to_payment()
    payment_page = PaymentPage(driver)
    payment_page.open_page()
    payment_page.should_be_loaded()
    if card_data:
        payment_page.enter_card_details(card_number=card_data.get("number", ""), card_date=card_data.get("date", ""), card_cvv=card_data.get("cvv", ""), card_holder=card_data.get("holder", ""), manual_number="invalid" in testcase)
        if "invalid" in testcase:
            payment_page.wait_error_visible()
            payment_page.check_visible(payment_page.INPUT_ERROR)
        else:
            payment_page.check_invisible(payment_page.INPUT_ERROR) # важно для стабильности тестов этой формы

    screenshot_test(driver, element=payment_page.CARD_FORM, name=f"payment_form_{testcase}.png", threshold=0.05)
