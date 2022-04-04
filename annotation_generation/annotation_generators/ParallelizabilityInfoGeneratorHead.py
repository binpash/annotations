from annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from annotation_generation.datatypes.parallelizability.Parallelizer import Parallelizer


class ParallelizabilityInfoGeneratorHead(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-q", "-v", "-z", "--help", "--version"]
    # list_of_all_options = ["-c", "-n"]

    # Which ones do affect parallelizability?
    # we can parallelize individual files

    def generate_info(self) -> None:
        #     TODO
        pass

    def apply_transformers_for_parallelizers(self) -> None:
        parallelizer_if_seq_conc = Parallelizer.make_parallelizer_indiv_files()
        self.meta.append_to_parallelizer_list(parallelizer_if_seq_conc)
