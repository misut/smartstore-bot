import pydantic

from bot.domain.base import Entity, ValueObject


class ProductOption(ValueObject):
    name: str
    price: int

    @pydantic.validator("price")
    def validate_price(cls, price: int) -> int:
        if price < 0:
            raise ValueError("Price must be positive")

        return price


class ProductOptions(ValueObject):
    name: str
    options: list[ProductOption] = []


class Product(Entity):
    name: str
    price: int
    store_name: str
    
    options_list: list[ProductOptions] = None

    @pydantic.validator("price")
    def validate_price(cls, price: int) -> int:
        if price < 0:
            raise ValueError("Price must be positive")
        
        return price
