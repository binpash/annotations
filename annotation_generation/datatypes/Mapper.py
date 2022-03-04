from enum import Enum


class Mapper:

    def __init__(self, kind, cmd):
        self.kind = kind
        # for now, we also store if the mapper is the same to handle the cases similarly
        self.command = cmd

    def __repr__(self):
        return f'{self.kind}'

    @staticmethod
    def make_mapper_same_as_seq(cmd):
        return Mapper(MapperKindEnum.SAME_AS_SEQ, cmd)

    @staticmethod
    def make_mapper_custom(custom_cmd):
        return Mapper(MapperKindEnum.CUSTOM, custom_cmd)


class MapperKindEnum(Enum):
    SAME_AS_SEQ = 1
    CUSTOM = 2

