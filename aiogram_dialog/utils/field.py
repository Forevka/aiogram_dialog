from typing import Generic, TypeVar

T = TypeVar('T')

class Field(Generic[T]):
    field_name: str
    def __init__(self, field_name: str):
        self.field_name = field_name

    def __str__(self) -> str:
        return self.field_name