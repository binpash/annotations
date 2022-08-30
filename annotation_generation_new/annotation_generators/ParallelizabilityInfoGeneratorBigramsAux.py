from annotation_generation_new.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from annotation_generation_new.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_custom_2_ary_from_string_representation
from annotation_generation_new.datatypes.parallelizability.MapperSpec import \
    make_mapper_spec_custom_from_string_representation
from annotation_generation_new.datatypes.parallelizability.Parallelizer import make_parallelizer_consec_chunks

class ParallelizabilityInfoGeneratorBigramsAux(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        map_spec = make_mapper_spec_custom_from_string_representation("bigram_aux_map", is_implemented=True)
        agg_spec = make_aggregator_spec_custom_2_ary_from_string_representation("bigram_aux_reduce", is_implemented=True)
        parallelizer_cc = make_parallelizer_consec_chunks(mapper_spec=map_spec, aggregator_spec=agg_spec)
        parallelizer_cc.info_mapper_aggregator = 2
        self.append_to_parallelizer_list(parallelizer_cc)
