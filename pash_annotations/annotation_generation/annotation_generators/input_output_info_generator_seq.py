from pash_annotations.annotation_generation.annotation_generators.input_output_info_generator_interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorSeq(InputOutputInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()
        self.set_all_operands_as_config_arg_type_string()
