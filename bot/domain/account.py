import abc
from datetime import datetime

import pydantic

from bot.domain.base import Entity, Service


class Account(Entity):
    id: str
    password: str

    updated_at: datetime = pydantic.Field(default_factory=datetime.now)


class AccountRepository(abc.ABC, Service):
    @abc.abstractmethod
    def select(self) -> list[Account]:
        ...

    @abc.abstractmethod
    def get(self, entity_id: str) -> Account | None:
        ...

    @abc.abstractmethod
    def insert(self, entity: Account) -> None:
        ...

    @abc.abstractmethod
    def update(self, entity: Account) -> None:
        ...

    @abc.abstractmethod
    def delete(self, entity_id: str) -> None:
        ...
