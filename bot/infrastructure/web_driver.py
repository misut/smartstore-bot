from loguru import logger
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome import service, webdriver
from webdriver_manager.chrome import ChromeDriverManager


class ChromeWebDriver:
    driver: webdriver.WebDriver

    options: ChromeOptions
    service: service.Service

    def __init__(self, hidden: bool = False) -> None:
        self.options = ChromeOptions()
        if hidden:
            self.options.add_argument("headless")
            self.options.add_argument("window-size=1920x1080")
            self.options.add_argument("disable-gpu")

        self.service = service.Service(ChromeDriverManager().install())

        
        logger.debug("Chrome driver installed")

    def __enter__(self) -> webdriver.WebDriver:
        self.driver = Chrome(
            service=self.service,
            options=self.options,
        )

    def __exit__(self, *args) -> None:
        self.driver.quit()
