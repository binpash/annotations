from annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorComm(ParallelizabilityInfoGeneratorInterface):
    # for details on what the functions do, check comments in its super class ParallelizablibilityInfoGeneratorInterface

    # list_of_all_flags = ["-1", "-2", "-3", "--check-order", "--nocheck-order", "--total", "-z", "--help", "--version"]
    # list_of_all_options = ["--output-delimiter"]

    # Which ones do affect parallelizability?
    # none, it is very hard to parallelize because of potentially different speed of traversing both files

    def generate_info(self) -> None:
        # No parallelizers
        pass
