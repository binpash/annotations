from datatypes.FlagOption import FlagOption, Option, Flag

def make_arg_simple(arg: list) -> FlagOption:
    if len(arg) == 1:
        return Flag(arg[0])
    elif len(arg) == 2:
        return Option(arg[0], arg[1])
    else:
        raise Exception("no proper kind given for Arg")

def standard_repr(obj) -> str:
    repr_str = f'{obj.__class__}: \n'
    for attribute, value in obj.__dict__.items():
        repr_str += f'\t {attribute}: {value}\n'
    return repr_str

def standard_eq(obj1, obj2) -> bool:
    if not obj1.__class__ == obj2.__class__:
        return False
    for attribute in obj1.__dict__.keys():
        if not obj1[attribute] == obj2[attribute]:
            return False
    return True
