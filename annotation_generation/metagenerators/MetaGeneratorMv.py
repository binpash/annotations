
from datatypes.Arg import ArgKindEnum
from metagenerators.MetaGenerator_Interface import MetaGeneratorInterface


class MetaGeneratorMv(MetaGeneratorInterface):
    # for details on what the functions do, check comments in its super class MetaGeneratorInterface

    # list_of_all_flags = ["-b", "-f", "-i", "-n", "--strip-trailing-slashes", "-T",
    #                      "-u", "-v", "-Z", "--help", "--version"]
    # list_of_all_options = ["--backup", "-S", "-t"]

    # Questions:
    # What does --strip-trailing-slashes mean for input/output lists?
    # How to handle this? standard backup suffix: ~ , could be set by VERSION_CONTROL=
    #   none/off, numbered/t, existing/nil, simple/never

    # Which ones do affect input/output?
    # --backup[=Control] -> O
    # -b -> O
    # -f -> O kind of since it would not overwrite otherwise
    # -i -> O kind of since it would ask -> no interactive assumed for now
    # -n -> O do not overwrite existing file
    # --suffix=SUFFIX -> O overwrites the usual backup suffix
    # note that last of -f, -i, -n takes affect
    # -t -> O target directory
    # -u -> O update only if source file is newer than destination file

    # 2 Versions possible for output files, going for A:
    # A) over-approximating:
    #   - put (whole) output directory (file) in output_list
    #   - do only check -t then
    # B) more precise:
    #   - we know state of file system, so we can determine which files will
    #     be written in the destination directory, i.e., moved and backed up,
    #     depending on all the different options but recomputing quite some program logic then

    def apply_standard_filedescriptor_transformer_for_input_output_lists(self):
        version_or_help_write_to_stdout = self.arg_list_contains_at_least_one_of(["--help", "--version"])
        if version_or_help_write_to_stdout:
            self.meta.append_stdout_to_output_list()
        # no way to suppress error messages hence added
        self.meta.append_stderr_to_output_list()

    def apply_operands_transformer_for_input_output_lists(self):
        # -T shall treat destination as file, not directory, not considered currently
        # -t gives destination directory as an argument to option and determines
        #    how operands are interpreted
        list_options_t = self.filter_arg_list_with("-t")
        match len(list_options_t):
            case 0:
                # all but last input, last output
                self.meta.add_list_to_input_list(self.operand_names_list[:-1])
                self.meta.add_list_to_output_list(self.operand_names_list[-1:])
            case 1:
                # all input, output given as argument to "-t"
                self.meta.add_list_to_input_list(self.operand_names_list)
            case _:
                # multiple -t options not allowed (checked using cmd)
                raise Exception("multiple -t options defined for mv")

    def apply_indiv_arg_transformer_for_input_output_lists(self, arg):
        if arg.get_name() == "-t":
            self.meta.prepend_el_to_output_list(arg.option_arg)

    # Which ones do affect parallelizability?
    # It does not really make sense to parallelize mv.
    # We parallelize data streams to exploit multi cores but mv deals with the disk e.g.

