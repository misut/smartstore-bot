from loguru import logger

from bot.domain import StoreType
from bot.infrastructure import ChromeSmartStoreErrander


def test_check_product(errander: ChromeSmartStoreErrander) -> None:
    with errander:
        assert not errander.check_product(6490282859, "samlip", StoreType.BRAND)
        assert errander.check_product(5397361753, "_minix")


def test_fetch_product(errander: ChromeSmartStoreErrander) -> None:
    expected_name = "라인프렌즈 코니 베이비 앉은 인형 (35cm)"
    expected_price = 23000

    with errander:
        product = errander.fetch_product(4671768002, "linefriends")

    assert product.name == expected_name
    assert product.price == expected_price
    assert product.options_list[0].name == "사이즈"


def test_fetch_product_with_option_price(errander: ChromeSmartStoreErrander) -> None:
    with errander:
        product = errander.fetch_product(2166508785, "cjang")

    logger.info(
        f"{product.options_list[1].options[0].name}: {product.options_list[1].options[0].price}"
    )
    assert len(product.options_list) == 6
