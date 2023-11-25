from pash_annotations.annotation_generation.datatypes.parallelizability_info_generator_interface import (
    ParallelizabilityInfoGeneratorInterface,
)
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import (
    make_aggregator_spec_custom_2_ary_from_string_representation,
)
from pash_annotations.annotation_generation.datatypes.parallelizability.MapperSpec import (
    make_mapper_spec_custom_from_string_representation,
)
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import (
    make_parallelizer_consec_chunks,
)


class ParallelizabilityInfoGeneratorBigramsAux(ParallelizabilityInfoGeneratorInterface):
    def generate_info(self) -> None:
        map_spec = make_mapper_spec_custom_from_string_representation(
            "bigram_aux_map", is_implemented=True
        )
        agg_spec = make_aggregator_spec_custom_2_ary_from_string_representation(
            "bigram_aux_reduce", is_implemented=True
        )
        parallelizer_cc = make_parallelizer_consec_chunks(
            mapper_spec=map_spec, aggregator_spec=agg_spec
        )
        parallelizer_cc.info_mapper_aggregator = 2
        self.append_to_parallelizer_list(parallelizer_cc)
