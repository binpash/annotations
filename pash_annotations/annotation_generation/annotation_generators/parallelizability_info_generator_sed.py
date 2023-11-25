from pash_annotations.annotation_generation.datatypes.parallelizability_info_generator_interface import (
    ParallelizabilityInfoGeneratorInterface,
)


class ParallelizabilityInfoGeneratorSed(ParallelizabilityInfoGeneratorInterface):
    def generate_info(self) -> None:
        # TODO: Logic copied from PaSh, but does this not depend how the script is given?
        if (
            self.does_first_operand_start_with("-")
            or self.does_first_operand_start_with("s")
            or not (
                self.does_first_operand_contain("d")
                or self.does_first_operand_contain("q")
            )
        ):
            self.append_to_parallelizer_list_cc_seq_conc()
            self.append_to_parallelizer_list_rr_seq_conc()
