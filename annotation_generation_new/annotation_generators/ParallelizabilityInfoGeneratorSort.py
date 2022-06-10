from annotation_generation_new.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from annotation_generation_new.datatypes.parallelizability.AggregatorSpec import AggregatorSpec
from annotation_generation_new.datatypes.parallelizability.Parallelizer import Parallelizer
from annotation_generation_new.datatypes.parallelizability.TransformerFlagOptionList import TransformerFlagOptionListFilter, \
    TransformerFlagOptionListAdd, ChainTransformerFlagOptionList
from datatypes_new.BasicDatatypes import Flag, Option, ArgStringType


class ParallelizabilityInfoGeneratorSort(ParallelizabilityInfoGeneratorInterface):

    # Which ones do affect parallelizability?

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["-c", "-C", "-u", "-z", "-R", "-s", "-m", "--files0-from", "--random-source"]):
            pass    # no parallelization
        else:
            # Build aggregator spec: keep certain flags with filtering and add -m
            # TODO: find a better way to represent flag options lists to filter, maybe FlagOptionNameType
            flag_option_list_to_keep = [Flag("-b"), Flag("-d"), Flag("-f"), Flag("-g"), Flag("-i"), Flag("-M"), \
                                        Flag("-h"), Flag("-n"), Flag("-r"), Option("--sort", ""), Flag("-V"), Flag("-k"), Flag("-t")]
            transformer_flag_option_list_filter: TransformerFlagOptionListFilter = \
                TransformerFlagOptionListFilter(flag_option_list_to_keep)
            transformer_flag_option_list_add: TransformerFlagOptionListAdd = TransformerFlagOptionListAdd([Flag("-m")])
            chain_transformer_flag_option_list: ChainTransformerFlagOptionList = \
                ChainTransformerFlagOptionList([transformer_flag_option_list_filter, transformer_flag_option_list_add])
            aggregator_spec = AggregatorSpec.make_aggregator_spec_custom_2_ary_from_cmd_inv_with_transformers(
                                                                               flag_option_list_transformer=chain_transformer_flag_option_list,
                                                                               is_implemented=True)
            # Build parallelizers and append
            parallelizer_if_seq_cus = Parallelizer.make_parallelizer_indiv_files(aggregator_spec=aggregator_spec)
            parallelizer_rr_seq_cus = Parallelizer.make_parallelizer_round_robin(aggregator_spec=aggregator_spec)
            self.append_to_parallelizer_list(parallelizer_if_seq_cus)
            self.append_to_parallelizer_list(parallelizer_rr_seq_cus)
