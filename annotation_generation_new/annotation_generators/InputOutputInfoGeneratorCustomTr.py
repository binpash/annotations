from annotation_generation_new.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface
from datatypes_new.BasicDatatypes import ArgStringType


class InputOutputInfoGeneratorCustomTr(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdin()
        self.set_implicit_use_of_stdout()
        self.set_all_operands_as_config_arg_type_string()
