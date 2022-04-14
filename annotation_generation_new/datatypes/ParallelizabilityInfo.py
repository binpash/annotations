from __future__ import annotations
from util_standard import standard_repr
from typing import List, Optional, Tuple
from annotation_generation_new.datatypes.parallelizability.Parallelizer import Parallelizer

from util_new import return_empty_list_if_none_else_itself

class ParallelizabilityInfo:

    def __init__(self,
                 parallelizer_list: Optional[List[Parallelizer]] = None,    # None translates to empty list
                 round_robin_compatible_with_cat: bool  = False,
                 is_commutative: bool = False
                 ) -> None:
        self.parallelizer_list = return_empty_list_if_none_else_itself(parallelizer_list)
        self.round_robin_compatible_with_cat = round_robin_compatible_with_cat
        self.is_commutative = is_commutative

    def __repr__(self) -> str:
        return standard_repr(self)

    def append_to_parallelizer_list(self, parallelizer: Parallelizer) -> None:
        self.parallelizer_list.append(parallelizer)

    def unpack_info(self) -> Tuple[List[Parallelizer], bool, bool]:
        return self.parallelizer_list, self.round_robin_compatible_with_cat, self.is_commutative
