from util_standard import standard_repr
from typing import List, Optional, Tuple
from annotation_generation_new.datatypes.parallelizability.Parallelizer import Parallelizer, \
    make_parallelizer_round_robin_with_unwrap_from_other

from util_new import return_empty_list_if_none_else_itself

class ParallelizabilityInfo:

    def __init__(self,
                 parallelizer_list: Optional[List[Parallelizer]] = None,    # None translates to empty list
                 # TODO: remove RR_comp_with_cat
                 round_robin_compatible_with_cat: bool  = False,
                 is_commutative: bool = False
                 ) -> None:
        # TODO: remove direct uses of parallelizer list and use getter function which infers additional ones
        self.parallelizer_list = return_empty_list_if_none_else_itself(parallelizer_list)
        self.round_robin_compatible_with_cat = round_robin_compatible_with_cat
        self.is_commutative = is_commutative

    def __repr__(self) -> str:
        return standard_repr(self)

    def append_to_parallelizer_list(self, parallelizer: Parallelizer) -> None:
        self.parallelizer_list.append(parallelizer)

    def set_commutative(self) -> None:
        self.is_commutative = True

    def get_inferred_parallelizer_list(self):
        # add round robin with unwrap parallelizer for commutative command
        parallelizer_list = self.parallelizer_list
        for parallelizer in self.parallelizer_list:
            if self.is_commutative and parallelizer.splitter.is_splitter_consec_chunks():
                parallelizer_list.append(make_parallelizer_round_robin_with_unwrap_from_other(parallelizer))
        return parallelizer_list

    def unpack_info(self) -> Tuple[List[Parallelizer], bool, bool]:
        return self.get_inferred_parallelizer_list(), self.round_robin_compatible_with_cat, self.is_commutative
