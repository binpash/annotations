from pash_annotations.annotation_generation.annotation_generators.input_output_info_generator_interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorCut(InputOutputInfoGeneratorInterface):
    # list_of_all_flags = ["-n", "--complement", "-s", "-z", "--help", "--version"]
    # list_of_all_options = ["-b", "-c", "-d", "-f", "--output-delimiter", ]

    # Which ones do affect input/output?
    # none, takes from stdin and prints to stdout and no way to suppress output

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()
        self.if_no_operands_given_stdin_implicitly_used()
        self.all_operands_are_streaming_inputs()
