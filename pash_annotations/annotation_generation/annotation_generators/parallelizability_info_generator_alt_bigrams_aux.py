from pash_annotations.annotation_generation.annotation_generators.parallelizability_info_generator_interface import (
    ParallelizabilityInfoGeneratorInterface,
)
from pash_annotations.annotation_generation.datatypes.parallelizability.aggregator_spec import (
    make_aggregator_spec_custom_2_ary_from_string_representation,
)
from pash_annotations.annotation_generation.datatypes.parallelizability.mapper_spec import (
    make_mapper_spec_custom_from_string_representation,
)
from pash_annotations.annotation_generation.datatypes.parallelizability.parallelizer import (
    make_parallelizer_consec_chunks,
)


class ParallelizabilityInfoGeneratorAltBigramsAux(
    ParallelizabilityInfoGeneratorInterface
):
    def generate_info(self) -> None:
        mapper_spec = make_mapper_spec_custom_from_string_representation(
            "alt_bigrams_aux", is_implemented=True
        )
        agg_spec = make_aggregator_spec_custom_2_ary_from_string_representation(
            "alt_bigram_aux_reduce", is_implemented=True
        )
        parallelizer_cc = make_parallelizer_consec_chunks(
            mapper_spec=mapper_spec, aggregator_spec=agg_spec
        )
        self.append_to_parallelizer_list(parallelizer_cc)
