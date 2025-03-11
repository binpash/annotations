from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import \
    AdditionalInfoSplitterToMapper, make_parallelizer_round_robin, make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.MapperSpec import make_mapper_spec_custom
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_custom_2_ary_from_string_representation


class ParallelizabilityInfoGeneratorGrep(ParallelizabilityInfoGeneratorInterface):

    #base case with grep parallelizability info
    def generate_info(self) -> None:
            mapper_spec = None
            aggregator_spec = None
            add_info_from_splitter = None
            
            if (mapper_spec is None or mapper_spec.is_implemented) and \
                    (aggregator_spec is None or aggregator_spec.is_implemented):
                parallelizer_cc = make_parallelizer_consec_chunks(mapper_spec=mapper_spec,
                                                                  aggregator_spec=aggregator_spec,
                                                                  info_splitter_mapper=add_info_from_splitter)
                self.append_to_parallelizer_list(parallelizer_cc)
                parallelizer_rr = make_parallelizer_round_robin(mapper_spec=mapper_spec,
                                                                 aggregator_spec=aggregator_spec,
                                                                 info_splitter_mapper=add_info_from_splitter)
                self.append_to_parallelizer_list(parallelizer_rr)



""""
from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_custom_2_ary_from_string_representation
from pash_annotations.annotation_generation.datatypes.parallelizability.MapperSpec import \
    make_mapper_spec_custom_from_string_representation
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import make_parallelizer_round_robin, \
    make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import Parallelizer
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_custom_n_ary_from_string_representation

class ParallelizabilityInfoGeneratorCustom(ParallelizabilityInfoGeneratorInterface):
    # info to provide: parallelizer_list, round_robin_comp_with_cat, is_commutative (for optimisations)
    # parallelizabilityinfo has to-do to remove round_robin_comp_with_cat?

    def generate_info(self, parallelizer_list:Parallelizer, round_robin_comp_with_cat:bool, is_commutative:bool, aggregator_spec:str) -> None:
        if is_commutative:
            self.parallelizability_info.set_commutative()
        #mapper spec?
        #mapper_spec = make_mapper_spec_custom_from_string_representation("alt_bigrams_aux", is_implemented=True)

        if (mapper_spec is None or mapper_spec.is_implemented) and \
            (aggregator_spec is None or aggregator_spec.is_implemented):
               parallelizer_cc = make_parallelizer_consec_chunks(mapper_spec=mapper_spec,
                                                                  aggregator_spec=aggregator_spec,
                                                                  info_splitter_mapper=add_info_from_splitter)
            self.append_to_parallelizer_list(parallelizer_cc)
            parallelizer_rr = make_parallelizer_round_robin(mapper_spec=mapper_spec,
                                                                 aggregator_spec=aggregator_spec,
                                                                 info_splitter_mapper=add_info_from_splitter)
            self.append_to_parallelizer_list(parallelizer_rr)
        if round_robin_comp_with_cat:
            aggregator_spec_custom_rr = make_aggregator_spec_custom_2_ary_from_string_representation(aggregator_spec,
                                                                                       is_implemented=False)
            parallelizer_rr = make_parallelizer_round_robin(mapper_spec=None,
                                                                 aggregator_spec=aggregator_spec_custom_rr,
                                                                 info_splitter_mapper=None)
            self.append_to_parallelizer_list(parallelizer_rr)

        #how should the parallelizability info generator handle aggregators, i.e taking in file 
        agg_spec_custom_cc = make_aggregator_spec_custom_n_ary_from_string_representation(aggregator_spec)
        parallelizer_cc = make_parallelizer_consec_chunks(aggregator_spec = agg_spec_custom_cc)
        self.parallelizability_info.append_to_parallelizer_list(parallelizer_cc)
"""