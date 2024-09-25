from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface
from pash_annotations.datatypes.BasicDatatypes import Operand


class InputOutputInfoGeneratorGrep(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        #no flags case
        self.set_implicit_use_of_stdout()
        """
        if self.does_flag_option_list_contain_at_least_one_of(["-e", "-f"]):
            if self.get_operand_list_length() == 0:
                self.set_implicit_use_of_stdin()
            else:
                self.all_operands_are_streaming_inputs() # this is true also if empty
        """
        #else:
        self.set_first_operand_as_config_arg_type_string()
        if self.get_operand_list_length() == 1:
            self.set_implicit_use_of_stdin()
        else:
            self.all_but_first_operand_is_streaming_input()
