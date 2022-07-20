from annotation_generation_new.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorTee(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        self.all_but_first_operand_is_streaming_output()
        self.set_implicit_use_of_stdout()