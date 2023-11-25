from input_output_info_generator_interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorAltBigramAuxReduce(InputOutputInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.all_operands_are_streaming_inputs()
        self.set_implicit_use_of_stdout()
