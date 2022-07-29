from annotation_generation_new.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from annotation_generation_new.datatypes.parallelizability.Parallelizer import \
    make_parallelizer_round_robin
from annotation_generation_new.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_adj_lines_func_from_string_representation


class ParallelizabilityInfoGeneratorSed(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        # TODO: logic copied from PaSh, not in the style we'd like to write annotations
        first_operand = self.cmd_inv.operand_list[0]
        first_operand_arg = first_operand.get_name()
        first_operand_name = str(first_operand_arg)
        if (not (first_operand_name.startswith("-") or first_operand_name.startswith("s"))
            and ("d" in first_operand_name or "q" in first_operand_name)):
            self.set_parallelizability_info_for_pure()
        else:
            self.set_parallelizability_info_for_stateless()

