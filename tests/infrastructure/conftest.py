import os

import dotenv
import pytest
import selenium
from selenium import webdriver

from bot.infrastructure import ChromeSmartStoreErrander, ChromeWebDriver


@pytest.fixture(name="webdriver", scope="module")
def initialize_chrome_web_driver() -> ChromeWebDriver:
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")
    return ChromeWebDriver(options=options)


@pytest.fixture(name="errander", scope="module")
def initialize_chrome_errander(webdriver: ChromeWebDriver) -> ChromeSmartStoreErrander:
    dotenv.load_dotenv()

    return ChromeSmartStoreErrander(
        driver=webdriver.driver,
        username=os.getenv("SMARTSTORE_USERNAME"),
        password=os.getenv("SMARTSTORE_PASSWORD"),
    )
