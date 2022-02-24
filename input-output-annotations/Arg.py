import ArgKindEnum


class Arg:

    """
    kind : ArgKindEnum
    data : depending on kind
    """
    def __init__(self, kind, data):
        match kind:
            case ArgKindEnum.FLAG:
                self.flag_name = data
            case ArgKindEnum.OPTION:
                self.option_name, self.option_arg = data
            case ArgKindEnum.OPERAND:
                self.operand_name = data
            case _:
                raise Exception("Arg got unknown kind!")
