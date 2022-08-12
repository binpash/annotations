from annotation_generation_new.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from annotation_generation_new.datatypes.parallelizability.Parallelizer import Parallelizer


class ParallelizabilityInfoGeneratorCut(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-n", "--complement", "-s", "-z", "--help", "--version"]
    # list_of_all_options = ["-b", "-c", "-d", "-f", "--output-delimiter", ]

    def generate_info(self) -> None:
        self.append_to_parallelizer_list_cc_seq_conc()
        self.append_to_parallelizer_list_rr_seq_conc()
