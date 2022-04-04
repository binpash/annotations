from annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from annotation_generation.datatypes.parallelizability.Parallelizer import Parallelizer


class ParallelizabilityInfoGeneratorTail(ParallelizabilityInfoGeneratorInterface):
    # for details on what the functions do, check comments in ParallelizabilityInfoGeneratorInterface
    # basically the same as for HEAD but man page for TAIL is a bit longer

    # list_of_all_flags = ["-q", "--retry", "-v", "-z", "--help", "--version"]
    # list_of_all_options = ["-c", "-f", "-n", "-max-unchanged-stats", "--pid", "-s"]

    # Which ones do affect parallelizability?
    # we can parallelize individual files

    def generate_info(self) -> None:
    #     TODO
        pass

    def apply_transformers_for_parallelizers(self):
        parallelizer_if_seq_conc = Parallelizer.make_parallelizer_indiv_files()
        self.meta.append_to_parallelizer_list(parallelizer_if_seq_conc)
