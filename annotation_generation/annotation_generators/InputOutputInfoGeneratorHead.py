from annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorHead(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-q", "-v", "-z", "--help", "--version"]
    # list_of_all_options = ["-c", "-n"]

    # Which ones do affect input/output?
    # none

    def generate_info(self) -> None:
        self.apply_standard_filedescriptor_transformer()
        self.apply_operands_transformer()

    def apply_standard_filedescriptor_transformer_for_input_output_lists(self) -> None:
        self.set_ioinfo_implicit_use_of_stdout()
        self.if_no_operands_given_stdin_implicitly_used()

    def apply_operands_transformer_for_input_output_lists(self) -> None:
        self.all_operands_are_inputs()
