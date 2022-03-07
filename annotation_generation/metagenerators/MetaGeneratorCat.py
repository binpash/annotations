
from metagenerators.MetaGenerator_Interface import MetaGeneratorInterface
from parallelizers.ParallelizerIndivFiles import ParallelizerIndivFiles
from parallelizers.ParallelizerRoundRobin import ParallelizerRoundRobin


class MetaGeneratorCat(MetaGeneratorInterface):
    # for details on what the functions do, check comments in MetaGeneratorInterface

    # list_of_all_flags = ["-A", "-b", "-e", "-E", "--number", "-s", "t", "-T", "-u", "-v", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # basically only operands and the stdout as standard output and stderr for errors

    def apply_standard_filedescriptor_transformer_for_input_output_lists(self):
        self.meta.append_stdout_to_output_list()
        self.meta.append_stderr_to_output_list()  # errors are written to stderr and cannot be suppressed
        self.if_no_file_given_add_stdin_to_input_list()

    def apply_operands_transformer_for_input_output_lists(self):
        # all operands are inputs
        self.meta.add_list_to_input_list(self.operand_names_list)

    # Which ones do affect parallelizability?
    # in general it is easily parallelizable, with the following exception:
    # -n which numbers output lines and -s which squeezes repeated empty output lines
    # for -n without -s, we can parallelize with some a custom mapper (given the offset from which to count)
    # for -n and -s, we could only do with a 2nd pass so we omit this for now
    # for

    def apply_transformers_for_parallelizers(self):
        match (self.arg_list_contains_at_least_one_of(["-n"]), self.arg_list_contains_at_least_one_of(["-s"])):
            case (True, False): # we can have mappers that take offset as argument and without -s, this is stable
                # TODO: instantiate special mapper
                parallelizer_if_cus_conc = ParallelizerIndivFiles.make_parallelizer_mapper_custom_aggregator_conc("cus")
                self.meta.append_to_parallelizer_list(parallelizer_if_cus_conc)
                parallelizer_rr_cus_conc = ParallelizerRoundRobin.make_parallelizer_mapper_custom_aggregator_conc("cus")
                self.meta.append_to_parallelizer_list(parallelizer_rr_cus_conc)
            case (True, True):
                pass    # do not add any since it is tricky
            case (False, True):
                # not numbered but need to compare adjacent lines and possibly remove one blank line
                parallelizer_if_seq_adjf = ParallelizerIndivFiles.make_parallelizer_mapper_seq_aggregator_adjf("seq", "squeeze_blanks")
                self.meta.append_to_parallelizer_list(parallelizer_if_seq_adjf)
                parallelizer_rr_seq_adjf = ParallelizerRoundRobin.make_parallelizer_mapper_seq_aggregator_adjf("seq", "squeeze_blanks")
                self.meta.append_to_parallelizer_list(parallelizer_rr_seq_adjf)
                pass
            case (False, False):
                # add two parallelizers: IF and RR with SEQ and CONC each
                parallelizer_if_seq_conc = ParallelizerIndivFiles.make_parallelizer_mapper_seq_aggregator_conc("seq")
                self.meta.append_to_parallelizer_list(parallelizer_if_seq_conc)
                parallelizer_rr_seq_conc = ParallelizerRoundRobin.make_parallelizer_mapper_seq_aggregator_conc("seq")
                self.meta.append_to_parallelizer_list(parallelizer_rr_seq_conc)

