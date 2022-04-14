from datatypes_new.BasicDatatypes import FlagOption, Option, Flag

def make_arg_simple(arg: list) -> FlagOption:
    if len(arg) == 1:
        return Flag(arg[0])
    elif len(arg) == 2:
        return Option(arg[0], arg[1])
    else:
        raise Exception("no proper kind given for Arg")
