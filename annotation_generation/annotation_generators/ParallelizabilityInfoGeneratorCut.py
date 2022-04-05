from annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from annotation_generation.datatypes.parallelizability.Parallelizer import Parallelizer


class ParallelizabilityInfoGeneratorCut(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-n", "--complement", "-s", "-z", "--help", "--version"]
    # list_of_all_options = ["-b", "-c", "-d", "-f", "--output-delimiter", ]

    def generate_info(self) -> None:
        # add two parallelizers: IF and RR each with SEQ and CONC
        self.append_to_parallelizer_list_if_seq_conc()
        self.append_to_parallelizer_list_rr_seq_conc()
