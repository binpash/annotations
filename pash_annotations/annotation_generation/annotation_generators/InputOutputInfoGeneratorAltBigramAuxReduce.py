from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorAltBigramAuxReduce(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        self.all_operands_are_streaming_inputs()
        self.set_implicit_use_of_stdout()
