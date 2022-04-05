import os

import dotenv
import pytest
import selenium

from bot.infrastructure import ChromeSmartStoreErrander


@pytest.fixture(name="errander", scope="module")
def initialize_chrome_errander() -> ChromeSmartStoreErrander:
    dotenv.load_dotenv()

    option = selenium.webdriver.ChromeOptions()
    option.add_argument("headless")
    option.add_argument("window-size=1920x1080")
    option.add_argument("disable-gpu")

    return ChromeSmartStoreErrander(
        username=os.getenv("SMARTSTORE_USERNAME"),
        password=os.getenv("SMARTSTORE_PASSWORD"),
        option=option,
    )
