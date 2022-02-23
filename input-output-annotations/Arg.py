from ArgKindEnum import ArgKindEnum


class Arg:

    """
    kind : ArgKindEnum
    data : depending on kind
    """
    def __init__(self, kind, data):
        self.kind = kind,
        if kind == ArgKindEnum.FLAG:
            self.flag_name = data
        elif kind == ArgKindEnum.OPTION:
            self.option_name, self.option_arg = data
        else:
            raise Exception("Arg got unknown kind!")

    def get_name_suffix_for_transformer(self):
        if self.kind == ArgKindEnum.FLAG:
            str(self.flag_name)
        elif self.kind == ArgKindEnum.OPTION:
            str(self.option_name)
        else:
            raise Exception("Arg got unknown kind!")

def make_arg_simple(arg: list):
    
    if len(arg) == 1:
        ret = Arg(ArgKindEnum.FLAG, arg[0])
    elif len(arg) == 2:
        ret = Arg(ArgKindEnum.OPTION, arg)
    else:
        assert(False)
    
    return ret
