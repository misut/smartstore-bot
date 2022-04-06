import os

import dotenv
import pytest
from selenium import webdriver

from bot.infrastructure import ChromeSmartStoreErrander, ChromeWebDriver, SqlAlchemyDatabase, SqlAccountRepository

_DATABASE_URL = "sqlite:///:memory:?check_same_thread=False"


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

@pytest.fixture(name="database", scope="module")
def initialize_sqlalchemy_database() -> SqlAlchemyDatabase:
    database = SqlAlchemyDatabase(url=_DATABASE_URL)
    database.create_all()
    yield database
    database.drop_all()


@pytest.fixture(name="account_repo", scope="module")
def initialize_account_repository(database: SqlAlchemyDatabase) -> SqlAccountRepository:
    return SqlAccountRepository(database=database)
