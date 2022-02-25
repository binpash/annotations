
from datatypes.ArgKindEnum import ArgKindEnum
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

    def transformer_for_operands(self, operand_list_strings):
        # -T shall treat destination as file, not directory, not considered currently
        # -t gives destination directory as an argument to option and determines
        #    how operands are interpreted
        list_options_t = [arg for arg in self.arg_list if arg.get_name() == "-t"]
        match len(list_options_t):
            case 0:
                # all but last input, last output
                self.meta.add_list_to_input_list(operand_list_strings[:-1])
                self.meta.add_list_to_output_list(operand_list_strings[-1:])
            case 1:
                # all input, output given as argument to "-t"
                self.meta.add_list_to_input_list(operand_list_strings)
            case _:
                # multiple -t options not allowed (checked using cmd)
                raise Exception("multiple -t options defined for mv")

    def transformer_for_args(self, arg):
        if arg.kind == ArgKindEnum.OPTION and arg.option_name == "-t":
            self.meta.prepend_el_to_output_list(arg.option_arg)
