from annotation_generation_new.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from annotation_generation_new.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_custom_n_ary_from_string_representation
from annotation_generation_new.datatypes.parallelizability.Parallelizer import make_parallelizer_round_robin, \
    make_parallelizer_consec_chunks


class ParallelizabilityInfoGeneratorTestTwo(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        agg_spec = make_aggregator_spec_custom_n_ary_from_string_representation("runtime/agg/opt/concat.sh")
        parallelizer_cc = make_parallelizer_consec_chunks(aggregator_spec = agg_spec)
        self.append_to_parallelizer_list(parallelizer_cc)
        # RR does not work since we assert that the aggregator is cat or adj_line_*;
        # we could circumvent this with a field that indicates compatibility with RR
        # parallelizer_rr = make_parallelizer_round_robin(aggregator_spec = agg_spec)
        # self.append_to_parallelizer_list(parallelizer_rr)
