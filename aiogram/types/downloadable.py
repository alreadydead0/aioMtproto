from typing import Protocol, runtime_checkable


@runtime_checkable
class Downloadable(Protocol):
    @property
    def file_id(self) -> str: ...
