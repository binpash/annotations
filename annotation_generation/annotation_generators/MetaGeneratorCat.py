
from annotation_generation.annotation_generators.MetaGenerator_Interface import MetaGeneratorInterface
from annotation_generation.datatypes.parallelizability.Parallelizer import Parallelizer
from annotation_generation.datatypes.parallelizability.Mapper import Mapper
from annotation_generation.datatypes.parallelizability.Aggregator import Aggregator


class MetaGeneratorCat(MetaGeneratorInterface):
    # for details on what the functions do, check comments in MetaGeneratorInterface

    # list_of_all_flags = ["-A", "-b", "-e", "-E", "--number", "-s", "t", "-T", "-u", "-v", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # basically only operands and the stdout as standard output and stderr for errors

    def apply_standard_filedescriptor_transformer_for_input_output_lists(self) -> None:
        self.meta.append_stdout_to_output_list()
        self.meta.append_stderr_to_output_list()  # errors are written to stderr and cannot be suppressed
        self.if_no_file_given_add_stdin_to_input_list()

    def apply_operands_transformer_for_input_output_lists(self) -> None:
        # all operands are inputs
        self.meta.add_list_to_input_list(self.operand_names_list)

    # Which ones do affect parallelizability?
    # in general it is easily parallelizable, with the following exception:
    # -n which numbers output lines and -s which squeezes repeated empty output lines
    # for -n without -s, we can parallelize with some a custom mapper (given the offset from which to count)
    # for -n and -s, we could only do with a 2nd pass so we omit this for now
    # for

    def apply_transformers_for_parallelizers(self) -> None:
        if self.does_flag_option_list_contains_at_least_one_of(["-n"]) and not self.does_flag_option_list_contains_at_least_one_of(["-s"]):
            # case (True, False): # we can have mappers that take offset as argument and without -s, this is stable
                # TODO: instantiate special mapper
                mapper = Mapper.make_mapper_custom("cus")
                parallelizer_if_cus_conc = Parallelizer.make_parallelizer_indiv_files(mapper=mapper)
                self.meta.append_to_parallelizer_list(parallelizer_if_cus_conc)
                parallelizer_rr_cus_conc = Parallelizer.make_parallelizer_round_robin(mapper=mapper)
                self.meta.append_to_parallelizer_list(parallelizer_rr_cus_conc)
            # case (True, True):
            #     pass    # do not add any since it is tricky
        elif not self.does_flag_option_list_contains_at_least_one_of(["-n"]) and self.does_flag_option_list_contains_at_least_one_of(["-s"]):
            # case (False, True):
                # not numbered but need to compare adjacent lines and possibly remove one blank line
                aggregator = Aggregator.make_aggregator_adj_lines_func("squeeze_blanks")
                parallelizer_if_seq_adjf = Parallelizer.make_parallelizer_indiv_files(aggregator=aggregator)
                self.meta.append_to_parallelizer_list(parallelizer_if_seq_adjf)
                parallelizer_rr_seq_adjf = Parallelizer.make_parallelizer_round_robin(aggregator=aggregator)
                self.meta.append_to_parallelizer_list(parallelizer_rr_seq_adjf)
        elif not self.does_flag_option_list_contains_at_least_one_of(["-n"]) and not self.does_flag_option_list_contains_at_least_one_of(["-s"]):
            # case (False, False):
                # add two parallelizers: IF and RR with SEQ and CONC each
                parallelizer_if_seq_conc = Parallelizer.make_parallelizer_indiv_files()
                self.meta.append_to_parallelizer_list(parallelizer_if_seq_conc)
                parallelizer_rr_seq_conc = Parallelizer.make_parallelizer_round_robin()
                self.meta.append_to_parallelizer_list(parallelizer_rr_seq_conc)
        # match (self.arg_list_contains_at_least_one_of(["-n"]), self.arg_list_contains_at_least_one_of(["-s"])):
        #     case (True, False): # we can have mappers that take offset as argument and without -s, this is stable
        #         # TODO: instantiate special mapper
        #         mapper = Mapper.make_mapper_custom("cus")
        #         parallelizer_if_cus_conc = Parallelizer.make_parallelizer_indiv_files(mapper=mapper)
        #         self.meta.append_to_parallelizer_list(parallelizer_if_cus_conc)
        #         parallelizer_rr_cus_conc = Parallelizer.make_parallelizer_round_robin(mapper=mapper)
        #         self.meta.append_to_parallelizer_list(parallelizer_rr_cus_conc)
        #     case (True, True):
        #         pass    # do not add any since it is tricky
        #     case (False, True):
        #         # not numbered but need to compare adjacent lines and possibly remove one blank line
        #         aggregator = Aggregator.make_aggregator_adj_lines_func("squeeze_blanks")
        #         parallelizer_if_seq_adjf = Parallelizer.make_parallelizer_indiv_files(aggregator=aggregator)
        #         self.meta.append_to_parallelizer_list(parallelizer_if_seq_adjf)
        #         parallelizer_rr_seq_adjf = Parallelizer.make_parallelizer_round_robin(aggregator=aggregator)
        #         self.meta.append_to_parallelizer_list(parallelizer_rr_seq_adjf)
        #         pass
        #     case (False, False):
        #         # add two parallelizers: IF and RR with SEQ and CONC each
        #         parallelizer_if_seq_conc = Parallelizer.make_parallelizer_indiv_files()
        #         self.meta.append_to_parallelizer_list(parallelizer_if_seq_conc)
        #         parallelizer_rr_seq_conc = Parallelizer.make_parallelizer_round_robin()
        #         self.meta.append_to_parallelizer_list(parallelizer_rr_seq_conc)

