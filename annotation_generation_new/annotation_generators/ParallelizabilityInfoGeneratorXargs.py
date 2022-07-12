from annotation_generation_new.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface

class ParallelizabilityInfoGeneratorXargs(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        # in original, there is a CA but same info
        self.set_parallelizability_info_for_stateless()




