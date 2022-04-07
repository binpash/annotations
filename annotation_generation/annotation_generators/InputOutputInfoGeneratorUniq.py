from annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorUniq(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-d", "-D", "-i", "-u", "-z", "--help", "--version"]
    # list_of_all_options = ["--all-repeated", "-f", "--group", "-s", "-w"]

    # Which ones do affect input/output?
    # only the number of operands and flags --help and --version

    def generate_info(self) -> None:
        self.apply_standard_filedescriptor_transformer()
        self.apply_operands_transformer()

    def apply_standard_filedescriptor_transformer(self) -> None:
        pass
        # self.meta.append_stderr_to_output_list()
        # we add stdout and stdin in transformer_for_operands

    def apply_operands_transformer(self) -> None:
        # tested this with the command, man-page a bit inconclusive with optional OUTPUT
        if self.is_version_or_help_in_flag_option_list():
            self.set_implicit_use_of_stdout()
        elif self.get_operand_list_length() == 0:
            self.set_implicit_use_of_stdin()
            self.set_implicit_use_of_stdout()
        elif self.get_operand_list_length() == 1:
            self.all_operands_are_inputs()
            self.set_implicit_use_of_stdout()
        elif self.get_operand_list_length() == 2:
            self.all_but_last_operand_is_input()
            self.only_last_operand_is_output()
        else:
            raise Exception('extra operand for uniq, the 3rd one')
