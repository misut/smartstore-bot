from __future__ import annotations

from datetime import datetime

import pydantic


class ValueObject(pydantic.BaseModel):
    class Config:
        allow_mutation = False


class Event(ValueObject):
    occured_at: datetime = pydantic.Field(default_factory=datetime.now)


class Entity(pydantic.BaseModel):
    created_at: datetime = pydantic.Field(default_factory=datetime.now)
    
    class Config:
        orm_mode = True


class AggregateRoot(Entity):
    _event: Event | None

    def push_event(self, event: Event) -> None:
        if self._event:
            # TODO: 예외 이름 정하기
            raise Exception("Event has been already pushed")
        
        self._event = event

    def pop_event(self) -> Event:
        if not self._event:
            # TODO: 예외 이름 정하기
            raise Exception("Event should be pushed before popping")
        
        event, self._event = self._event, None
        return event


class Service(pydantic.BaseModel):
    exited_at: datetime | None
    launched_at: datetime | None

    def __enter__(self) -> Service:
        self.launched_at = datetime.now()

    def __exit__(self, *args) -> None:
        self.exited_at = datetime.now()
