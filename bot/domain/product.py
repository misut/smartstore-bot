import pydantic

from bot.domain.base import Entity, ValueObject


ProductOption = tuple[str, int]


class ProductOptions(ValueObject):
    name: str
    options: list[ProductOption]


class Product(Entity):
    name: str
    price: int
    store_name: str
    
    options_list: list[ProductOptions] = None

    @pydantic.validator("price")
    def validate_price(cls, price: int) -> bool:
        if price < 0:
            raise ValueError("Price must be positive")
        
        return price
