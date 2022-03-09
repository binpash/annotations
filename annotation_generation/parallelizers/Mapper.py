from enum import Enum


class Mapper:

    def __init__(self, kind, cmd=None):
        self.kind = kind
        # for now, we also store if the mapper is the same to handle the cases similarly
        self.command = cmd

    def __eq__(self, other):
        return self.kind == other.kind and self.command == other.command

    def __repr__(self):
        return f'{self.kind} \t {self.command}'

    @staticmethod
    def make_mapper_seq():
        return Mapper(MapperKindEnum.SAME_AS_SEQ)

    @staticmethod
    def make_mapper_custom(custom_cmd):
        return Mapper(MapperKindEnum.CUSTOM, custom_cmd)


class MapperKindEnum(Enum):
    SAME_AS_SEQ = 1
    CUSTOM = 2

