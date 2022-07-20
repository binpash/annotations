from annotation_generation_new.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorCustomSort(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        # copied from sort
        if not self.does_flag_option_list_contain_at_least_one_of(["-o"]):
            self.set_implicit_use_of_stdout()
        if self.get_operand_list_length() == 0 and not self.does_flag_option_list_contain_at_least_one_of(["--files0-from"]):
            self.set_implicit_use_of_stdin()
        else:
            self.all_operands_are_streaming_inputs()
