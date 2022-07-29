from annotation_generation_new.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface

class ParallelizabilityInfoGeneratorXargs(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        # in original, there is a case distinction but same info
        self.append_to_parallelizer_list_cc_seq_conc()
        self.append_to_parallelizer_list_rr_seq_conc()




