from datatypes.FileName import FileName
from datatypes.FileDescriptor import FileDescriptor, FileDescriptorEnum


def foldl(func, acc0, list):
    acc = acc0
    for el in list:
        acc = func(el, acc)    
    return acc


def list_deduplication(list_to_dedup):
    deduplicated_input_list = list()
    # side-effectful comprehension
    [deduplicated_input_list.append(item) for item in list_to_dedup if item not in deduplicated_input_list]
    return deduplicated_input_list


def compute_actual_el_for_input(input_el):
    if input_el == "-":
        return FileDescriptor(FileDescriptorEnum.STDIN)
    else:
        return FileName(input_el)


def compute_actual_el_for_output(output_el):
    if output_el == "-":
        return FileDescriptor(FileDescriptorEnum.STDOUT)
    else:
        return FileName(output_el)

