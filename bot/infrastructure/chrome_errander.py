from typing import Any

import selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from bot.domain import Product, ProductOption, ProductOptions, SmartStoreErrander

_LOGIN_SCRIPT = """
(function execute(){{
    document.querySelector('#id').value = '{username}';
    document.querySelector('#pw').value = '{password}';
}})();
"""
_LOGIN_URL = "https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com"
_PRODUCT_URL = "https://smartstore.naver.com/{store_name}/products/{product_id}"


class ChromeSmartStoreErrander(SmartStoreErrander):
    username: str
    password: str

    driver: selenium.webdriver.chrome.webdriver.WebDriver = None

    class Config:
        arbitrary_types_allowed = True

    def __enter__(self) -> SmartStoreErrander:
        _option = selenium.webdriver.ChromeOptions()
        _option.add_argument("headless")
        _option.add_argument("window-size=1920x1080")
        _option.add_argument("disable-gpu")
        self.driver = selenium.webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=_option
        )

        login_script = _LOGIN_SCRIPT.format(
            username=self.username, password=self.password
        )
        self.driver.get(_LOGIN_URL)
        self.driver.execute_script(login_script)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, "log.login"))
        ).click()

        return super().__enter__()

    def __exit__(self, *args) -> None:
        super().__exit__(*args)

        self.driver.quit()

    def check_product(self, store_name: str, product_id: int) -> bool:
        product_url = _PRODUCT_URL.format(store_name=store_name, product_id=product_id)
        self.driver.get(product_url)

        buy_button = self.driver.find_element(
            by=By.XPATH,
            value="//*[@id='content']/div/div[2]/div[2]/fieldset/div[9]/div[1]/div/a",
        )
        if buy_button.text != "구매하기":
            return False

        return True

    def fetch_product(self, store_name: str, product_id: int) -> Product:
        product_url = _PRODUCT_URL.format(store_name=store_name, product_id=product_id)
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
        for idx in range(5, 8):
            try:
                options_button = self.driver.find_element(
                    by=By.XPATH,
                    value=f"//*[@id='content']/div/div[2]/div[2]/fieldset/div[{idx}]/div/a",
                )
                options_name = options_button.text

                options_button.click()
                options_listbox = self.driver.find_element(
                    by=By.XPATH,
                    value=f"//*[@id='content']/div/div[2]/div[2]/fieldset/div[{idx}]/div/ul",
                )
                options = []
                for option in options_listbox.find_elements(by=By.TAG_NAME, value="li"):
                    # TODO: 옵션 가격 가져오기
                    options.append(ProductOption(name=option.text, price=0))

                options_list.append(ProductOptions(name=options_name, options=options))
            except:
                break

        return Product(
            id=product_id,
            name=name,
            price=price,
            store_name=store_name,
            options_list=options_list,
        )

    def buy_product(self, product: Product) -> None:
        if not self.check_product(product.store_name, product.id):
            return

        buy_button = self.driver.find_element(
            by=By.XPATH,
            value="//*[@id='content']/div/div[2]/div[2]/fieldset/div[9]/div[1]/div/a",
        )
        buy_button.click()

        pay_button = self.driver.find_element(
            by=By.XPATH,
            value="//*[@id='orderForm']/div/div[7]/button",
        )
        pay_button.click()
