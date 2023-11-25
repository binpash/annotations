from input_output_info_generator_interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorAltBigramsAux(InputOutputInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.set_implicit_use_of_stdin()
        self.set_implicit_use_of_stdout()
