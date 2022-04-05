from __future__ import annotations

from collections.abc import Callable
from typing import Any


class Handler:
    mapping: dict[Any, Callable] = {}

    def __init__(self) -> None:
        pass

    def handle(self, command: Any) -> None:
        command_type = type(command)
        if command_type not in self.mapping:
            raise Exception(f"Not registered type of a command: {command.__name__}")

        func = self.mapping[command_type]
        func(command)

    def include_handler(self, handler: Handler) -> None:
        self.mapping.update(handler.mapping)

    def on(self, command: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            params = list(func.__annotations__)
            command_type = func.__annotations__[params[0]]
            self.mapping[command_type] = func
            return func
        
        return decorator
