def standard_repr(obj) -> str:
    repr_str = f'{obj.__class__}'
    if len(obj.__dict__) != 0:
        repr_str += f': \n'
    else:
        repr_str += f'\n'
    for attribute, value in obj.__dict__.items():
        repr_str += f'\t {attribute}: {value}\n'
    return repr_str

def standard_eq(obj1, obj2) -> bool:
    if not obj1.__class__ == obj2.__class__:
        return False
    return vars(obj1) == vars(obj2)
    # for attribute in obj1.__dict__.keys():
    #     if not obj1[attribute] == obj2[attribute]:
    #         return False
    # return True
