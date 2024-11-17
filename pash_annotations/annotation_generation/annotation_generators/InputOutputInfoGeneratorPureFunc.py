from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import (
    InputOutputInfoGeneratorInterface,
)


class InputOutputInfoGeneratorPureFunc(InputOutputInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.set_implicit_use_of_stdin()
        self.set_implicit_use_of_stdout()
