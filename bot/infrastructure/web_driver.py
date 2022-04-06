from loguru import logger
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome import webdriver, service
from webdriver_manager.chrome import ChromeDriverManager


class ChromeWebDriver:
    driver: webdriver.WebDriver

    options: ChromeOptions
    service: service.Service

    def __init__(self, options: ChromeOptions = ChromeOptions()) -> None:
        self.options = options
        self.service = service.Service(ChromeDriverManager().install())

        self.driver = Chrome(
            options=self.options,
            service=self.service,
        )
        logger.debug("Chrome driver installed")
