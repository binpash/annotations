from pash_annotations.annotation_generation.annotation_generators.input_output_info_generator_interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorSetDiff(InputOutputInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.set_implicit_use_of_stdin()
        self.set_implicit_use_of_stdout()
        assert self.get_operand_list_length() == 1
        self.set_first_operand_as_config_arg_type_filename_or_std_descriptor()
