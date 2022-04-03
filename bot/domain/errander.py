from __future__ import annotations

import abc

from bot.domain.base import Service
from bot.domain.product import Product


class SmartStoreErrander(abc.ABC, Service):
    @abc.abstractmethod
    def __enter__(self) -> SmartStoreErrander:
        return super().__enter__()

    @abc.abstractmethod
    def __exit__(self, *args) -> None:
        super().__exit__()
    
    @abc.abstractmethod
    def fetch_product(self, store_name: str, product_id: int) -> Product:
        ...
    
    @abc.abstractmethod
    def buy_product(self, product: Product) -> None:
        ...
