from input_output_info_generator_interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorMkfifo(InputOutputInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.all_operands_are_other_outputs()
