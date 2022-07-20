from annotation_generation_new.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorTee(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdin()
        # copies to both operands and stdout
        self.set_implicit_use_of_stdout()
        self.all_operands_are_streaming_outputs()