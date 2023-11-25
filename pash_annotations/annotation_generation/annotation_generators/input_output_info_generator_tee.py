from input_output_info_generator_interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorTee(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdin()
        # copies to both operands and stdout
        self.set_implicit_use_of_stdout()
        self.all_operands_are_streaming_outputs()