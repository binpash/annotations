from datatypes.FileDescriptor import FileDescriptor, FileName, StdDescriptor, StdDescriptorEnum
from datatypes.Operand import Operand
from annotation_generation.datatypes.parallelizability.Aggregator import Aggregator
from annotation_generation.datatypes.parallelizability.Mapper import Mapper
from typing import Any, List, Optional, Union, TypeVar

TType = TypeVar("TType")

def foldl(func, acc0, list):
    acc = acc0
    for el in list:
        acc = func(el, acc)    
    return acc


def list_deduplication(list_to_dedup: List[TType]) -> List[TType]:
    deduplicated_input_list = list()
    # side-effectful comprehension
    [deduplicated_input_list.append(item) for item in list_to_dedup if item not in deduplicated_input_list]
    return deduplicated_input_list


def compute_actual_el_for_input(input_el: Operand) -> FileDescriptor:
    if input_el == "-":
        return StdDescriptor(StdDescriptorEnum.STDIN)
    else:
        return FileName(input_el.name)


def compute_actual_el_for_output(output_el: Operand) -> FileDescriptor:
    if output_el == "-":
        return StdDescriptor(StdDescriptorEnum.STDOUT)
    else:
        return FileName(output_el.name)


def return_empty_list_if_none_else_itself(arg: Optional[TType]) -> Union[TType, List[Any]]: #list always empty
    if arg is None:
        return []
    else:
        return arg

def return_default_if_none_else_itself(arg: Optional[TType], default: TType) -> TType:
    if arg is None:
        return default
    else:
        return arg

