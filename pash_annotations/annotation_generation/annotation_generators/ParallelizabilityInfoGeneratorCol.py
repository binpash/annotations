from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface

class ParallelizabilityInfoGeneratorCol(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        self.append_to_parallelizer_list_cc_seq_conc()
        self.append_to_parallelizer_list_rr_seq_conc()



