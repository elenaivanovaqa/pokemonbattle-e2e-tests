import pytest
import requests
from selenium.webdriver import Chrome
from dotenv import load_dotenv
import os
from selenium.webdriver.chrome.options import Options

from pages.login_page import LoginPage
from pages.pokemons_page import PokemonsPage

from pathlib import Path

import sys, io
from PIL import Image, ImageChops


def pytest_addoption(parser):
    parser.addoption(
        "--prepare-data",
        action="store_true",
        help="Создаст тестовые сущности для локального запуска",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "no_headless: mark test to run only on headed (visual) mode"
    )


def pytest_runtest_setup(item):
    if "no_headless" in item.keywords and item.config.getoption("--prepare-data"):
        pytest.skip("not running in headless mode")


@pytest.fixture(scope="session", autouse=True)
def create_session_data(request):
    load_dotenv()


@pytest.fixture
def driver(request):
    options = Options()

    # keep a stable viewport in both modes
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--force-device-scale-factor=1")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--disable-gpu")

    if request.config.option.prepare_data:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    driver = Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="session", autouse=True)
def load_envs():
    load_dotenv()


@pytest.fixture
def authorized_user(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.should_be_loaded()
    login_page.login()

    pokemons_page = PokemonsPage(driver)
    pokemons_page.should_be_loaded()
    yield driver


@pytest.fixture
def enable_premium(cancel_premium):
    load_dotenv()
    url = f"{os.getenv('LAVKA_URL')}/payments"
    headers = {
        "Accept": "*/*",
        "trainer_token": os.getenv("TEST_TRAINER_TOKEN"),
        "Content-Type": "application/json",
    }
    payload = {
        "order_type": "premium",
        "details": {
            "days": "1",
            "card_number": "4111111111111111",
            "card_name": "FREJA COLLIE",
            "card_actual": "12/26",
            "card_cvv": "125",
            "secure_code": "56456",
        },
    }
    resp = requests.post(url, json=payload, headers=headers)
    assert resp.status_code == 200


@pytest.fixture
def cancel_premium():
    load_dotenv()
    url = f"{os.getenv('LAVKA_URL')}/cancel_premium"
    headers = {
        "Accept": "*/*",
        "trainer_token": os.getenv("TEST_TRAINER_TOKEN"),
        "Content-Type": "application/json",
    }
    resp = requests.post(url, headers=headers)
    assert resp.status_code in (200, 400)


def hide_element(driver, locator):
    if hasattr(locator, "get_attribute"):
        elems = [locator]
    elif isinstance(locator, tuple):
        elems = driver.find_elements(*locator)
    else:
        raise Exception("Некорректный элемент/локатор!")
    for el in elems:
        driver.execute_script(
            "arguments[0].style.transition='none';"
            "arguments[0].style.opacity='0';",
            el,
        )


@pytest.fixture
def screenshot_test(assert_snapshot, request, browser_name):
    def run(
        driver,
        name: str,
        element=None,
        threshold: float = 0.05,
        baseline_dir: str = Path(request.node.fspath).parent.resolve()
        / "__snapshots__"
        / browser_name
        / sys.platform,
        diff_dir: str = "__screenshot_diffs__",
        mask: list = None,
    ):
        if mask:
            for loc in mask:
                try:
                    hide_element(driver, loc)
                except Exception:
                    pass

        if element is None:
            png = driver.get_screenshot_as_png()
        else:
            if isinstance(element, tuple):
                element = driver.find_element(*element)
            png = element.screenshot_as_png

        try:
            assert_snapshot(png, name=name, threshold=threshold)
            return
        except (AssertionError, ValueError):
            if not os.path.isdir(diff_dir):
                os.mkdir(diff_dir)

            baseline_path = os.path.join(baseline_dir, name)

            if name.lower().endswith(".png"):
                name = name[:-4]

            actual_path = os.path.join(diff_dir, f"{name}_actual.png")
            base_copy = os.path.join(diff_dir, f"{name}_baseline.png")
            diff_path = os.path.join(diff_dir, f"{name}_diff.png")

            actual = Image.open(io.BytesIO(png)).convert("RGBA")
            baseline = Image.open(baseline_path).convert("RGBA")

            actual.save(actual_path)
            baseline.save(base_copy)

            if actual.size != baseline.size:
                w = min(actual.width, baseline.width)
                h = min(actual.height, baseline.height)
                actual = actual.crop((0, 0, w, h))
                baseline = baseline.crop((0, 0, w, h))

            diff = ImageChops.difference(baseline, actual)
            mask_img = diff.convert("L").point(lambda v: 255 if v > 10 else 0, mode="1")
            red = Image.new("RGB", actual.size, (255, 0, 0))
            highlight = actual.convert("RGB").copy()
            highlight.paste(red, mask=mask_img)

            highlight.save(diff_path)
            pytest.fail(
                f"Snapshot mismatch for '{name}'. "
                f"See {actual_path}, {base_copy}, {diff_path}"
            )

    return run
