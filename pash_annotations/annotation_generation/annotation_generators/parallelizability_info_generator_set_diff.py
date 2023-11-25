from pash_annotations.annotation_generation.datatypes.parallelizability_info_generator_interface import (
    ParallelizabilityInfoGeneratorInterface,
)


class ParallelizabilityInfoGeneratorSetDiff(ParallelizabilityInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.append_to_parallelizer_list_cc_seq_conc()
        # issues with RR (also in branch future - due to tee I think)
        # self.set_parallelizability_info_for_stateless()
