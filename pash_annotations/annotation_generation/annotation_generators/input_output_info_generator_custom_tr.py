from input_output_info_generator_interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorCustomTr(InputOutputInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.set_implicit_use_of_stdin()
        self.set_implicit_use_of_stdout()
        self.set_all_operands_as_config_arg_type_string()
