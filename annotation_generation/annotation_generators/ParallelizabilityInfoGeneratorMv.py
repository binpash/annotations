from annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorMv(ParallelizabilityInfoGeneratorInterface):
    # for details on what the functions do, check comments in its super class ParallelizabilityInfoGeneratorInterface

    # list_of_all_flags = ["-b", "-f", "-i", "-n", "--strip-trailing-slashes", "-T",
    #                      "-u", "-v", "-Z", "--help", "--version"]
    # list_of_all_options = ["--backup", "-S", "-t"]

    # Which ones do affect parallelizability?
    # It does not really make sense to parallelize mv.
    # We parallelize data streams to exploit multi cores but mv deals with the disk e.g.

    def generate_info(self) -> None:
        #     TODO
        pass
