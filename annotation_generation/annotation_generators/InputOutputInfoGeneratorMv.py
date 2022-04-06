from typing import List
from datatypes.FlagOption import FlagOption
from annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorMv(InputOutputInfoGeneratorInterface):

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

    def generate_info(self) -> None:
        self.apply_standard_filedescriptor_transformer()
        self.apply_operands_transformer()

    def apply_standard_filedescriptor_transformer(self) -> None:
        self.if_version_or_help_stdout_implicitly_used()
        # # no way to suppress error messages hence added
        # self.meta.append_stderr_to_output_list()

    def apply_operands_transformer(self) -> None:
        # -T shall treat destination as file, not directory, not considered currently
        # -t gives destination directory as an argument to option and determines how operands are interpreted
        list_options_t : List[FlagOption] = self.get_flag_option_list_filtered_with(["-t"])
        if len(list_options_t) == 0:
            self.all_but_last_operand_is_input()
            self.only_last_operand_is_output()
        elif len(list_options_t) == 1:
            self.all_operands_are_inputs()
        else:
            # multiple -t options not allowed (checked using cmd)
            raise Exception("multiple -t options defined for mv")

    # option args shall be handled in parser
    # def apply_indiv_arg_transformer_for_input_output_lists(self, arg: FlagOption) -> None:
    #     if arg.get_name() == "-t":
    #         self.meta.prepend_el_to_output_list(arg.option_arg)
