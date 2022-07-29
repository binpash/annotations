from annotation_generation_new.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface

class ParallelizabilityInfoGeneratorSeq(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        self.set_parallelizability_info_for_pure() # according to original info
