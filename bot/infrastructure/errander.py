import re

from loguru import logger
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from bot.domain import (
    Product,
    ProductOption,
    ProductOptions,
    SmartStoreErrander,
    StoreType,
)

_LOGIN_SCRIPT = """
(function execute(){{
    document.querySelector('#id').value = '{username}';
    document.querySelector('#pw').value = '{password}';
}})();
"""
_LOGIN_URL = "https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com"
_PRODUCT_URL = "https://{store_type}.naver.com/{store_name}/products/{product_id}"


class ChromeSmartStoreErrander(SmartStoreErrander):
    driver: webdriver.WebDriver
    username: str
    password: str

    class Config:
        arbitrary_types_allowed = True

    def __enter__(self) -> SmartStoreErrander:
        login_script = _LOGIN_SCRIPT.format(
            username=self.username, password=self.password
        )
        self.driver.get(_LOGIN_URL)
        self.driver.execute_script(login_script)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, "log.login"))
        ).click()
        logger.debug("Login success")

        return super().__enter__()

    def __exit__(self, *args) -> None:
        super().__exit__(*args)

    def check_product(
        self,
        product_id: int,
        store_name: str,
        store_type: StoreType = StoreType.SMARTSTORE,
    ) -> bool:
        product_url = _PRODUCT_URL.format(
            product_id=product_id, store_name=store_name, store_type=store_type
        )
        self.driver.get(product_url)

        try:
            self.driver.find_elements(
                by=By.CLASS_NAME,
                value="_2-uvQuRWK5",
            )[0]
        except IndexError:
            return False

        return True

    def fetch_product(
        self,
        product_id: int,
        store_name: str,
        store_type: StoreType = StoreType.SMARTSTORE,
    ) -> Product:
        product_url = _PRODUCT_URL.format(
            product_id=product_id, store_name=store_name, store_type=store_type
        )
        self.driver.get(product_url)

        name = self.driver.find_element(
            by=By.XPATH,
            value="//*[@id='content']/div/div[2]/div[2]/fieldset/div[1]/div[1]/h3",
        ).text

        price = int(
            self.driver.find_element(
                by=By.XPATH,
                value="//*[@id='content']/div/div[2]/div[2]/fieldset/div[1]/div[2]/div/strong/span[2]",
            ).text.replace(",", "")
        )

        options_list = []
        try:
            options_button = self.driver.find_elements(
                by=By.CLASS_NAME, value="bd_1fhc9"
            )[0]
            options_name = options_button.text

            options_button.click()
            options_listbox = options_button.get_property("parentNode").get_property(
                "childNodes"
            )[1]
            option_buttons = options_listbox.get_property("childNodes")
            options = []
            for option_button in option_buttons:
                options.append(ProductOption(name=option_button.text, price=0))
            options_button.click()

            options_list.append(ProductOptions(name=options_name, options=options))
        except:
            logger.debug("No options found")

        try:
            options_buttons = self.driver.find_elements(
                by=By.CLASS_NAME, value="bd_2gVQ5"
            )
            options_buttons = options_buttons[: len(options_buttons) // 2]
            for options_button in options_buttons:
                options_name = options_button.text

                options_button.click()
                options_listbox = options_button.get_property(
                    "parentNode"
                ).get_property("childNodes")[1]
                option_buttons = options_listbox.get_property("childNodes")
                options = []
                for option_button in option_buttons:
                    regexp = re.search(r"\(\+[0-9,]+원\)", option_button.text)
                    option_name = option_button.text[: regexp.start()].strip(" \t\n\r")
                    option_price = int("".join(re.findall(r"[0-9]", regexp.group())))
                    options.append(ProductOption(name=option_name, price=option_price))
                options_button.click()

                options_list.append(ProductOptions(name=options_name, options=options))
        except:
            logger.debug("No additional options found")

        product = Product(
            id=product_id,
            name=name,
            price=price,
            store_name=store_name,
            store_type=store_type,
            options_list=options_list,
        )
        logger.debug(f"Product fetched successfully: ({product.name}: {product.price})")
        return product

    def buy_product(self, product: Product) -> None:
        if not self.check_product(product.id, product.store_name, product.store_type):
            return

        buy_button = self.driver.find_elements(
            by=By.CLASS_NAME,
            value="_2-uvQuRWK5",
        )[0]
        buy_button.click()

        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_all_elements_located(
                (By.CLASS_NAME, "btn_payment")
            )
        )[0].click()
