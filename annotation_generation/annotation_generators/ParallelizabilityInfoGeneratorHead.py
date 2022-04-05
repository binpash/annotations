from annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from annotation_generation.datatypes.parallelizability.Parallelizer import Parallelizer


class ParallelizabilityInfoGeneratorHead(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-q", "-v", "-z", "--help", "--version"]
    # list_of_all_options = ["-c", "-n"]

    # Which ones do affect parallelizability?
    # we can parallelize individual files

    def generate_info(self) -> None:
        self.append_to_parallelizer_list_if_seq_conc()
