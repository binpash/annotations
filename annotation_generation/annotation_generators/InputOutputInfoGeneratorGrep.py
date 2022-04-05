from annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface
from datatypes.Operand import Operand


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
        # self.apply_flagoptionlist_transformer(arg: FlagOption)

    def apply_standard_filedescriptor_transformer(self) -> None:
        # in general, output is written to stdout but can be suppressed
        # though, --help and --version overrules this (and no actual result returned)
        output_suppressed = self.does_flag_option_list_contains_at_least_one_of(["-q"])
        version_or_help_write_to_stdout = self.if_version_or_help_stdout_implicitly_used()
        if not output_suppressed or version_or_help_write_to_stdout:
            self.set_ioinfo_implicit_use_of_stdout()
        # deprecated since we assume stderr as log for errors and do add to annotation
        # errors are written to stderr but can be suppressed
        # errors_suppressed = self.does_flag_option_list_contains_at_least_one_of(["-s"])
        # if not errors_suppressed:
        #     stderr is used

    def apply_operands_transformer(self) -> None:
        if self.does_flag_option_list_contains_at_least_one_of(["-e", "-f"]):
            self.all_operands_are_inputs() # this is true also if empty
        else:
            self.set_first_operand_as_positional_config()
            self.all_but_first_operand_is_input()
        # deciding on whether there is an input to check, add to input_list
        if self.get_length_ioinfo_positional_input_list() == 0:
            if self.does_flag_option_list_contains_at_least_one_of(["-r"]):
                self.set_ioinfo_positional_input_list([Operand("$PWD")]) # TODO: this is not exactly equivalent due to path and type wrong
            else:
                self.set_ioinfo_implicit_use_of_stdin()

    # TODO: options shall be handled in parser
    # def apply_flagoptionlist_transformer(self, flagoption: FlagOption):
    #     if flagoption.get_name() == "-f":
    #         self.meta.prepend_el_to_input_list(arg.option_arg)