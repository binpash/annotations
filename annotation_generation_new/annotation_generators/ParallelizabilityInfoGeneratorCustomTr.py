from annotation_generation_new.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from datatypes_new.BasicDatatypes import Operand


class ParallelizabilityInfoGeneratorCustomTr(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        self.append_to_parallelizer_list_cc_seq_conc()
        self.append_to_parallelizer_list_rr_seq_conc()
