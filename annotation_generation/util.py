from annotation_generation.datatypes.FileName import FileName
from annotation_generation.datatypes.FileDescriptor import FileDescriptor, FileDescriptorEnum
from annotation_generation.parallelizers.Aggregator import Aggregator
from annotation_generation.parallelizers.Mapper import Mapper
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


def compute_actual_el_for_input(input_el: str) -> Union[FileName, FileDescriptor]:
    if input_el == "-":
        return FileDescriptor(FileDescriptorEnum.STDIN)
    else:
        return FileName(input_el)


def compute_actual_el_for_output(output_el: str) -> Union[FileName, FileDescriptor]:
    if output_el == "-":
        return FileDescriptor(FileDescriptorEnum.STDOUT)
    else:
        return FileName(output_el)


def return_empty_list_if_none_else_itself(arg: Optional[TType]) -> Union[TType, List[Any]]: #list always empty
    if arg is None:
        return []
    else:
        return arg


def return_mapper_seq_if_none_else_itself(arg: Optional[Mapper]) -> Mapper:
    if arg is None:
        return Mapper.make_mapper_seq()
    else:
        return arg


def return_aggregator_conc_if_none_else_itself(arg: Optional[Aggregator]) -> Aggregator:
    if arg is None:
        return Aggregator.make_aggregator_concatenate()
    else:
        return arg
