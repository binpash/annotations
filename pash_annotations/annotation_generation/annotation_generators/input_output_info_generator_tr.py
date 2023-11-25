from pash_annotations.annotation_generation.annotation_generators.input_output_info_generator_interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorTr(InputOutputInfoGeneratorInterface):
    # list_of_all_flags = ["-c", "-d", "-s", "-t", "--help", "--version",
    # list_of_all_options = []

    # Which ones do affect input/output?
    # none, takes from stdin and prints to stdout and no way to suppress output

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdin()
        self.set_implicit_use_of_stdout()
        self.set_all_operands_as_config_arg_type_string()
