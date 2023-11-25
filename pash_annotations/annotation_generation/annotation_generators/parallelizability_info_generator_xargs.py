from parallelizability_info_generator_interface import ParallelizabilityInfoGeneratorInterface

class ParallelizabilityInfoGeneratorXargs(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        # in original, there is a case distinction but same info
        self.append_to_parallelizer_list_cc_seq_conc()
        self.append_to_parallelizer_list_rr_seq_conc()




