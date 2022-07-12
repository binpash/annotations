from annotation_generation_new.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface

class ParallelizabilityInfoGeneratorExport(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        # no parallelization as effectful for environment
        pass



