from annotation_generation_new.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface
from datatypes_new.BasicDatatypes import Operand


class InputOutputInfoGeneratorGrep(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-V", "--help", "-E", "-F", "-G", "-P", "-i", "--no-ignore-case", "-v", "-w",
    #                      "-x", "-y", "-c", "-L", "-l", "-o", "-q", "-s", "-b", "-H", "-h", "-n", "-T", "-Z",
    #                      "--no-group-separator", "-a", "-I", "-r", "-R", "--line-buffered", "-U", "-z"]
    # list_of_all_options = ["-e", "-f", "--color", "-m", "--label", "-A", "-B", "-C", "--group-separator",
    #                        "--binary-files", "-D", "-d", "--exclude", "--exclude-from", "--exclude-dir", "--include"]

    # Which ones do affect input/output?
    # -f affects input
    # -r actually does not really affect both since files and directories are both identified by their name
    # for now, we ignore --exclude, --exclude-from, --exclude-dir, and --include and, thus, over-approximate
    # for now, we ignore -D/-d with actions

    def generate_info(self) -> None:
        self.apply_standard_filedescriptor_transformer()
        self.apply_operands_transformer()
        # self.set_multiple_inputs_possible()

    def apply_standard_filedescriptor_transformer(self) -> None:
        # though, --help and --version overrules this (and no actual result returned)
        output_suppressed = self.does_flag_option_list_contains_at_least_one_of(["-q"])
        version_or_help_write_to_stdout = self.is_version_or_help_in_flag_option_list()
        if not output_suppressed or version_or_help_write_to_stdout:
            self.set_implicit_use_of_stdout()

    def apply_operands_transformer(self) -> None:
        if self.does_flag_option_list_contains_at_least_one_of(["-e", "-f"]):
            self.all_operands_are_streaming_inputs() # this is true also if empty
        else:
            self.set_first_operand_as_positional_config_arg_type_string()
            self.all_but_first_operand_is_streaming_input()
        # TODO: make correct CA for input list
        # deciding on whether there is an input to check, add to input_list
        # if self.get_length_ioinfo_positional_input_list() == 0:
        #     if self.does_flag_option_list_contains_at_least_one_of(["-r"]):
        #         raise Exception("-r option without dir name not handled")
        #         # self.set_ioinfo_positional_input_list([Operand("$PWD")]) # TODO: this is not exactly equivalent due to path and type wrong
        #     else:
        #         self.set_implicit_use_of_stdin()
