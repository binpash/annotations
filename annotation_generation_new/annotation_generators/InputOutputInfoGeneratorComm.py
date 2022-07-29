from annotation_generation_new.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorComm(InputOutputInfoGeneratorInterface):
    # for details on what the functions do, check comments in its super class InputOutputInfoGeneratorInterface

    # list_of_all_flags = ["-1", "-2", "-3", "--check-order", "--nocheck-order", "--total", "-z", "--help", "--version"]
    # list_of_all_options = ["--output-delimiter"]

    # Which ones do affect input/output?
    # none

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()
        assert(self.get_operand_list_length() == 2)  # needs two files to compare;
        self.all_operands_are_streaming_inputs()
