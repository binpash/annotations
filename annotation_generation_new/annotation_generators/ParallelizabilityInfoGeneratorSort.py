from annotation_generation_new.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from annotation_generation_new.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_custom_2_ary_from_cmd_inv_with_transformers
from annotation_generation_new.datatypes.parallelizability.Parallelizer import \
    make_parallelizer_indiv_files, make_parallelizer_consec_chunks
from annotation_generation_new.datatypes.parallelizability.TransformerFlagOptionList import TransformerFlagOptionListFilter, \
    TransformerFlagOptionListAdd, ChainTransformerFlagOptionList
from datatypes_new.BasicDatatypes import Flag, Option, ArgStringType


class ParallelizabilityInfoGeneratorSort(ParallelizabilityInfoGeneratorInterface):

    # Which ones do affect parallelizability?

    def generate_info(self) -> None:
        self.set_commutative()
        if self.does_flag_option_list_contain_at_least_one_of(["-c", "-C", "-u", "-z", "-R", "-s", "-m", "--files0-from", "--random-source"]):
            pass    # no parallelization
        else:
            # Build aggregator spec: keep certain flags with filtering and add -m
            transformer_filter = TransformerFlagOptionListFilter(["-b", "-d", "-f", "-g", "-i", "-M", "-h", "-n", "-r", "--sort", "-V", "-k", "-t"])
            transformer_add = TransformerFlagOptionListAdd([Flag("-m")])
            chained_transformers = ChainTransformerFlagOptionList([transformer_filter, transformer_add])
            # TODO: change this to n instead of 2 but we keep this for testing aggregator trees for now
            aggregator_spec = make_aggregator_spec_custom_2_ary_from_cmd_inv_with_transformers(
                flag_option_list_transformer=chained_transformers, is_implemented=True)
            # Build parallelizers and append
            parallelizer_cc_seq_cus = make_parallelizer_consec_chunks(aggregator_spec=aggregator_spec)
            self.append_to_parallelizer_list(parallelizer_cc_seq_cus)
