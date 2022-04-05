from __future__ import annotations
from util import standard_repr
from typing import List, Optional
from annotation_generation.datatypes.parallelizability.Parallelizer import Parallelizer

from annotation_generation.util import return_empty_list_if_none_else_itself

class ParallelizabilityInfo:

    def __init__(self,
                 parallelizer_list: Optional[List[Parallelizer]] = None,    # None translates to empty list
                 round_robin_compatible_with_cat: bool  = False,
                 is_commutative: bool = False
                 ) -> ParallelizabilityInfo:
        self.parallelizer_list = return_empty_list_if_none_else_itself(parallelizer_list)
        self.round_robin_compatible_with_cat = round_robin_compatible_with_cat
        self.is_commutative = is_commutative

    def __repr__(self) -> str:
        return standard_repr(self)

    def append_to_parallelizer_list(self, parallelizer: Parallelizer) -> None:
        self.parallelizer_list.append(parallelizer)