from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorWc(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["--files0-from"]):
            raise Exception('wc with --files0-from is considered side-effectful for now')
        
        if self.get_operand_list_length() == 0:
            self.set_implicit_use_of_stdin()
            self.set_implicit_use_of_stdout()
        else:
            self.all_operands_are_streaming_inputs()
            self.set_implicit_use_of_stdout()
