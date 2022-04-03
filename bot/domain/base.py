from __future__ import annotations

import uuid
from datetime import datetime

import pydantic

ID = int


class ValueObject(pydantic.BaseModel):
    class Config:
        allow_mutation = False
        orm_mode = True


class Event(ValueObject):
    occured_at: datetime = pydantic.Field(default_factory=datetime.now)


class Entity(pydantic.BaseModel):
    id: ID

    class Config:
        orm_mode = True

 
class AggregateRoot(Entity):
    _event: Event | None


class Service(pydantic.BaseModel):
    launched_at: datetime | None

    def __enter__(self) -> Service:
        self.launched_at = datetime.now()

    def __exit__(self, *args) -> None:
        ...
