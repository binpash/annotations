from annotation_generation_new.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from annotation_generation_new.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_custom_n_ary_from_string_representation
from annotation_generation_new.datatypes.parallelizability.MapperSpec import \
    make_mapper_spec_custom_from_string_representation
from annotation_generation_new.datatypes.parallelizability.Parallelizer import make_parallelizer_round_robin, \
    make_parallelizer_consec_chunks

class ParallelizabilityInfoGeneratorAltBigramAuxReduce(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        pass
