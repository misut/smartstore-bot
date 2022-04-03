from bot.infrastructure import ChromeSmartStoreErrander


def test_fetch_product(errander: ChromeSmartStoreErrander) -> None:
    expected_name = "라인프렌즈 코니 베이비 앉은 인형 (35cm)"
    expected_price = 23000

    with errander:
        product = errander.fetch_product("linefriends", 4671768002)

    assert product.name == expected_name
    assert product.price == expected_price
    assert product.options_list[0].name == "사이즈"
