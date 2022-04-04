from annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorCat(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-A", "-b", "-e", "-E", "--number", "-s", "t", "-T", "-u", "-v", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # basically only operands and the stdout as standard output (and stderr for errors)

    def generate_info(self) -> None:
        self.apply_standard_filedescriptor_transformer()
        self.apply_operands_transformer()

    def apply_standard_filedescriptor_transformer(self) -> None:
        self.set_ioinfo_implicit_use_of_stdout()
        self.if_no_operands_given_stdin_implicitly_used()

    def apply_operands_transformer(self) -> None:
        self.all_operands_are_inputs()
