import os

import dotenv
import pytest

from bot.infrastructure import ChromeSmartStoreErrander


@pytest.fixture(name="errander", scope="module")
def initialize_chrome_errander() -> ChromeSmartStoreErrander:
    dotenv.load_dotenv()

    return ChromeSmartStoreErrander(
        username=os.getenv("SMARTSTORE_USERNAME"),
        password=os.getenv("SMARTSTORE_PASSWORD"),
    )
