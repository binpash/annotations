import ArgKindEnum


class Arg:

    """
    kind : ArgKindEnum
    data : depending on kind
    """
    def __init__(self, kind, data):
        self.kind = kind,
        match kind:
            case ArgKindEnum.FLAG:
                self.flag_name = data
            case ArgKindEnum.OPTION:
                self.option_name, self.option_arg = data
            case ArgKindEnum.OPERAND:
                self.operand_name = data
            case _:
                raise Exception("Arg got unknown kind!")

    def get_name_suffix_for_transformer(self):
        match self.kind:
            case ArgKindEnum.FLAG:
                str(self.flag_name)
            case ArgKindEnum.OPTION:
                str(self.option_name)
            case ArgKindEnum.OPERAND:
                "operand" # flags and options all start with - so no clash of names
            case _:
                raise Exception("Arg got unknown kind!")
