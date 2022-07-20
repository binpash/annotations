from annotation_generation_new.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorDiff(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        # all operands streaming inputs
        self.set_implicit_use_of_stdout()