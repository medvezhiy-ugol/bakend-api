from pydantic import BaseModel
from typing import Type, TypeVar

T = TypeVar("T", bound=BaseModel)


def serialize_models(raw: list[Type], model: Type[T]) -> list[T]:
    return [model.from_orm(elem) for elem in raw]
