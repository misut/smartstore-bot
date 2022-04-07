from __future__ import annotations

import abc

from bot.domain.base import Service
from bot.domain.product import Product, StoreType


class SmartStoreErrander(abc.ABC, Service):
    @abc.abstractmethod
    def __enter__(self) -> SmartStoreErrander:
        return super().__enter__()

    @abc.abstractmethod
    def __exit__(self, *args) -> None:
        super().__exit__()

    @abc.abstractmethod
    def check_product(
        self,
        product_id: int,
        store_name: str,
        store_type: StoreType = StoreType.SMARTSTORE,
    ) -> bool:
        ...

    @abc.abstractmethod
    def fetch_product(
        self,
        product_id: int,
        store_name: str,
        store_type: StoreType = StoreType.SMARTSTORE,
    ) -> Product:
        ...

    @abc.abstractmethod
    def buy_product(self, product: Product) -> None:
        ...
