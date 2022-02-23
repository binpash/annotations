import Meta
import ArgKindEnum

class MetaGeneratorInterface:

    # determines the initial meta, the function for args transformations, and a function to change meta due to operands
    # [Arg] -> Meta
    #        x Arg -> (Meta -> Meta)
    #        x [Arg] -> ([Operand] x Meta) -> Meta
    def select_subcommand(arg_list):
        pass

    def generate_operand_meta_func(arg_list):
        pass

    def transformers_for_args_grep(arg, meta):
        pass