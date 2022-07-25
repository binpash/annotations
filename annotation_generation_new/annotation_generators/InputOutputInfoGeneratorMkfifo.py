from annotation_generation_new.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorMkfifo(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        self.all_operands_are_other_outputs()
