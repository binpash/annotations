from pash_annotations.annotation_generation.annotation_generators.parallelizability_info_generator_interface import (
    ParallelizabilityInfoGeneratorInterface,
)


class ParallelizabilityInfoGeneratorCut(ParallelizabilityInfoGeneratorInterface):
    # list_of_all_flags = ["-n", "--complement", "-s", "-z", "--help", "--version"]
    # list_of_all_options = ["-b", "-c", "-d", "-f", "--output-delimiter", ]

    def generate_info(self) -> None:
        self.append_to_parallelizer_list_cc_seq_conc()
        self.append_to_parallelizer_list_rr_seq_conc()
