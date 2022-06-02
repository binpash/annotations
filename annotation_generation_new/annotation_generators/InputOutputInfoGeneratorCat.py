from annotation_generation_new.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorCat(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-A", "-b", "-e", "-E", "--number", "-s", "t", "-T", "-u", "-v", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # basically only operands and the stdout as standard output (and stderr for errors)

    def generate_info(self) -> None:
        # self.set_multiple_inputs_possible()
        self.set_implicit_use_of_stdout()
        self.if_no_operands_given_stdin_implicitly_used()
        self.all_operands_are_streaming_inputs()
