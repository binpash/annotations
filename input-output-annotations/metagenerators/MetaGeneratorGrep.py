
from datatypes.Arg import ArgKindEnum
from metagenerators.MetaGenerator_Interface import MetaGeneratorInterface


class MetaGeneratorGrep(MetaGeneratorInterface):
    # for details on what the functions do, check comments in MetaGeneratorInterface

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

    def transformer_for_standard_filedescriptors(self):
        # in general, output is written to stdout but can be suppressed
        # though, --help and --version overrules this (and no actual result returned)
        output_suppressed = self.arg_list_contains_at_least_one_of(["-q"])
        version_or_help_write_to_stdout = self.arg_list_contains_at_least_one_of(["--help"]) \
                                          or self.arg_list_contains_at_least_one_of(["--version"])
        if not output_suppressed or version_or_help_write_to_stdout:
            self.meta.append_stdout_to_output_list()
        # errors are written to stderr but can be suppressed
        errors_suppressed = self.arg_list_contains_at_least_one_of(["-s"])
        if not errors_suppressed:
            self.meta.append_stderr_to_output_list()

    def transformer_for_operands(self):
        if any([arg.get_name() in ["-e", "-f"] for arg in self.arg_list]):
            operand_slicing_parameter = 0
        else:
            operand_slicing_parameter = 1
        print("arg_list" + str(self.arg_list))
        print("operand_slicing_par" + str(operand_slicing_parameter))
        operand_list_filenames = self.operand_names_list[operand_slicing_parameter:]

        # append pattern file if existent
        # pattern_filename_list = self.operand_names_list[:operand_slicing_parameter]
        # self.meta.add_list_to_input_list(pattern_filename_list)

        # deciding on whether there is an input to check, add to input_list
        if len(operand_list_filenames) == 0:
            if self.arg_list_contains_at_least_one_of(["-r"]):
                self.meta.add_list_to_input_list("$CWD")
            else:
                self.meta.prepend_stdin_to_input_list()
        else:
            self.meta.add_list_to_input_list(operand_list_filenames)

    def transformer_for_args(self, arg):
        if arg.kind == ArgKindEnum.OPTION and arg.option_name == "-f":
            self.meta.prepend_el_to_input_list(arg.option_arg)
