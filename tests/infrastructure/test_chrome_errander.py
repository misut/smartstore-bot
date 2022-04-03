from bot.infrastructure import ChromeSmartStoreErrander


def test_check_product(errander: ChromeSmartStoreErrander) -> None:
    with errander:
        assert not errander.check_product("linefriends", 4671768002)
        assert errander.check_product("_minix", 5397361753)


def test_fetch_product(errander: ChromeSmartStoreErrander) -> None:
    expected_name = "라인프렌즈 코니 베이비 앉은 인형 (35cm)"
    expected_price = 23000

    with errander:
        product = errander.fetch_product("linefriends", 4671768002)

    assert product.name == expected_name
    assert product.price == expected_price
    assert product.options_list[0].name == "사이즈"
    assert product.options_list[0].options[0].name == "옵션없음 (품절)"
