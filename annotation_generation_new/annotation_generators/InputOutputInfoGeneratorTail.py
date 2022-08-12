from annotation_generation_new.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorTail(InputOutputInfoGeneratorInterface):
    # basically the same as for HEAD but man page for TAIL is a bit longer

    # list_of_all_flags = ["-q", "--retry", "-v", "-z", "--help", "--version"]
    # list_of_all_options = ["-c", "-f", "-n", "-max-unchanged-stats", "--pid", "-s"]

    # Which ones do affect input/output?
    # none

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()
        self.if_no_operands_given_stdin_implicitly_used()
        self.all_operands_are_streaming_inputs()
