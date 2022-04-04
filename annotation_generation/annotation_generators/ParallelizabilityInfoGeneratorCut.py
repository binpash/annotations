from annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from annotation_generation.datatypes.parallelizability.Parallelizer import Parallelizer


class ParallelizabilityInfoGeneratorCut(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-n", "--complement", "-s", "-z", "--help", "--version"]
    # list_of_all_options = ["-b", "-c", "-d", "-f", "--output-delimiter", ]

    def generate_info(self) -> None:
        # TODO
        pass

    def apply_transformers_for_parallelizers(self) -> None:
        # add two parallelizers: IF and RR with SEQ and CONC each
        parallelizer_if_seq_conc = Parallelizer.make_parallelizer_indiv_files()
        self.meta.append_to_parallelizer_list(parallelizer_if_seq_conc)
        parallelizer_rr_seq_conc = Parallelizer.make_parallelizer_round_robin()
        self.meta.append_to_parallelizer_list(parallelizer_rr_seq_conc)


