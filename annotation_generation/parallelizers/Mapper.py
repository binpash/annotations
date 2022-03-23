from __future__ import annotations
from typing import Optional

from enum import Enum



class Mapper:

    def __init__(self, kind: MapperKindEnum, cmd: Optional[str]=None) -> None:
        self.kind = kind
        # for now, we also store if the mapper is the same to handle the cases similarly
        self.command = cmd

    def __eq__(self, other: Mapper) -> bool:
        return self.kind == other.kind and self.command == other.command

    def __repr__(self) -> str:
        return f'{self.kind} \t {self.command}'

    @staticmethod
    def make_mapper_seq() -> Mapper:
        return Mapper(MapperKindEnum.SAME_AS_SEQ)

    @staticmethod
    def make_mapper_custom(custom_cmd: str) -> Mapper:
        return Mapper(MapperKindEnum.CUSTOM, custom_cmd)


class MapperKindEnum(Enum):
    SAME_AS_SEQ = 1
    CUSTOM = 2

