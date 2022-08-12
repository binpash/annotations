from annotation_generation_new.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorUniq(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-d", "-D", "-i", "-u", "-z", "--help", "--version"]
    # list_of_all_options = ["--all-repeated", "-f", "--group", "-s", "-w"]

    # Which ones do affect input/output?
    # only the number of operands and flags --help and --version

    def generate_info(self) -> None:
        # tested this with the command, man-page a bit inconclusive with optional OUTPUT
        # assumption that version/help not provided
        if self.get_operand_list_length() == 0:
            self.set_implicit_use_of_stdin()
            self.set_implicit_use_of_stdout()
        elif self.get_operand_list_length() == 1:
            self.all_operands_are_streaming_inputs()
            self.set_implicit_use_of_stdout()
        elif self.get_operand_list_length() == 2:
            self.all_but_last_operand_is_streaming_input()
            self.only_last_operand_is_stream_output()
        else:
            raise Exception('extra operand for uniq, the 3rd one')
