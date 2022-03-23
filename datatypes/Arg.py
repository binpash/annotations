from __future__ import annotations

from enum import Enum
from typing import Optional

class Arg:

    """
    kind : ArgKindEnum
    data : depending on kind
    """
    def __init__(self, kind: ArgKindEnum, name: str, arg: Optional[str] = None) -> None:
        self.kind = kind
        if kind == ArgKindEnum.FLAG:
            assert(arg is None)
            self.flag_name = name
        elif kind == ArgKindEnum.OPTION and arg is not None:
            self.option_name = name
            self.option_arg = arg
        else:
            raise Exception("no proper kind given for Arg")

    def __repr__(self):
        if self.kind == ArgKindEnum.FLAG:
            return self.flag_name
        elif self.kind == ArgKindEnum.OPTION:
            return f'{self.option_name} {self.option_arg}'
        else:
            raise Exception("Arg got unknown kind!")

    # def __eq__(self, other):
    #     if isinstance(other, Arg):
    #         if self.kind == other.kind: and self.flag_name == self.flagname
    #
    #     return False

    def get_name(self) -> str:
        if self.kind == ArgKindEnum.FLAG:
            return self.flag_name
        elif self.kind == ArgKindEnum.OPTION:
            return self.option_name
        else:
            raise Exception("Arg got unknown kind!")


def make_arg_simple(arg: list) -> Arg:
    
    if len(arg) == 1:
        ret = Arg(ArgKindEnum.FLAG, arg[0])
    elif len(arg) == 2:
        ret = Arg(ArgKindEnum.OPTION, arg[0], arg[1])
    else:
        assert False
    
    return ret


class ArgKindEnum(Enum):
    FLAG = 1
    OPTION = 2
