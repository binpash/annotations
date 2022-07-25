from annotation_generation_new.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorBigramAuxReduce(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        # since this is a mapper function with aux information,
        # we internally assume that all inputs are given in operands: input, output, aux_output_1, aux_output_2, ...
        pass
