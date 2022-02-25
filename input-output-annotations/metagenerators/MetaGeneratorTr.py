from metagenerators.MetaGenerator_Interface import MetaGeneratorInterface


class MetaGeneratorTr(MetaGeneratorInterface):
    # for details on what the functions do, check comments in its super class MetaGeneratorInterface

    # list_of_all_flags = ["-c", "-d", "-s", "-t", "--help", "--version",
    # list_of_all_options = []

    # Questions:
    # Shall stdin and stdout be part of input/output_lists or rather some flag in meta
    # whether they use (one of) them? For now, we omit but easy to add.
    # TODO: imo add flags about stdin and stdout in meta and then in functions below

    # Which ones do affect input/output?
    # none, takes from stdin and prints to stdout

    def transformer_for_operands(self, operand_list):
        pass

    def transformer_for_args(self, arg):
        pass
