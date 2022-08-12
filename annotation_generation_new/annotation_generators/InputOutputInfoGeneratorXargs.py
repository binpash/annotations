from annotation_generation_new.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorXargs(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        # TODO: this is not quite true, and we actually would need to recursively call the respective annotation generator?
        self.set_all_operands_as_arg_string()
        self.set_implicit_use_of_stdin()
        self.set_implicit_use_of_stdout()
