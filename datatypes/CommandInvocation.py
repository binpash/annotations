from __future__ import annotations
from typing import List

from datatypes.Arg import Arg
from datatypes.Operand import Operand

class CommandInvocation:

    def __init__(self, cmd: str, arg_list: List[Arg], operand_list: List[Operand]) -> None:
        self.cmd = cmd
        self.arg_list = arg_list
        self.operand_list = operand_list

    def __repr__(self):
#         TODO: add rest
        return self.cmd

    def __eq__(self, other: CommandInvocation):
        return self.cmd == other.cmd \
            and self.arg_list == other.arg_list \
            and self.operand_list == other.operand_list
