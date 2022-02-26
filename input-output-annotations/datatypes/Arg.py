from enum import Enum


class Arg:

    """
    kind : ArgKindEnum
    data : depending on kind
    """
    def __init__(self, kind, data):
        self.kind = kind
        if kind == ArgKindEnum.FLAG:
            self.flag_name = data
        elif kind == ArgKindEnum.OPTION:
            self.option_name, self.option_arg = data
        else:
            raise Exception("Arg got unknown kind!")

    def __repr__(self):
        if self.kind == ArgKindEnum.FLAG:
            return self.flag_name
        elif self.kind == ArgKindEnum.OPTION:
            return f'{self.option_name} {self.option_arg}'
        else:
            raise Exception("Arg got unknown kind!")

    def get_name(self):
        if self.kind == ArgKindEnum.FLAG:
            return self.flag_name
        elif self.kind == ArgKindEnum.OPTION:
            return self.option_name
        else:
            raise Exception("Arg got unknown kind!")


def make_arg_simple(arg: list):
    
    if len(arg) == 1:
        ret = Arg(ArgKindEnum.FLAG, arg[0])
    elif len(arg) == 2:
        ret = Arg(ArgKindEnum.OPTION, arg)
    else:
        assert False
    
    return ret


class ArgKindEnum(Enum):
    FLAG = 1
    OPTION = 2
