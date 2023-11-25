from pash_annotations.annotation_generation.annotation_generators.input_output_info_generator_interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorCol(InputOutputInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.set_implicit_use_of_stdin()
        self.set_implicit_use_of_stdout()
