from annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorComm(InputOutputInfoGeneratorInterface):
    # for details on what the functions do, check comments in its super class InputOutputInfoGeneratorInterface

    # list_of_all_flags = ["-1", "-2", "-3", "--check-order", "--nocheck-order", "--total", "-z", "--help", "--version"]
    # list_of_all_options = ["--output-delimiter"]

    # Which ones do affect input/output?
    # none

    def generate_info(self) -> None:
        self.apply_standard_filedescriptor_transformer()
        self.apply_operands_transformer()

    def apply_standard_filedescriptor_transformer(self) -> None:
        self.set_ioinfo_implicit_use_of_stdout()

    def apply_operands_transformer(self) -> None:
        # if not self.does_flag_option_list_contains_at_least_one_of(["--help", "--version"]): assume minimized command
        # assert(len(self.operand_names_list) == 2)  # needs two files to compare;
        self.all_operands_are_inputs()
