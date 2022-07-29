from annotation_generation_new.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorSed(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdin()
        self.set_implicit_use_of_stdout()
        if not self.does_flag_option_list_contain_at_least_one_of(["-e", "-f"]):
            self.set_first_operand_as_config_arg_type_string()
            self.all_but_first_operand_is_streaming_input()
        else:
            self.all_operands_are_streaming_inputs()

