import Meta
import ArgKindEnum
from meta_transformer import MetaGeneratorInterface


class GrepMetaTransformer(MetaGeneratorInterface):
    # determines the initial meta, the function for args transformations, and a function to change meta due to operands
    # [Arg] -> Meta
    #        x Arg -> (Meta -> Meta)
    #        x [Arg] -> ([Operand] x Meta) -> Meta
    def select_subcommand(arg_list):
        initial_meta = Meta(),
        transformer_for_operands = GrepMetaTransformer.generate_operand_meta_func(arg_list),
        {initial_meta, GrepMetaTransformer.transformers_for_args_grep, transformer_for_operands}


    def generate_operand_meta_func(arg_list):
        operand_slicing_parameter = 0 \
            if any(arg.kind == ArgKindEnum.OPTION and arg.option_name == "-f" for arg in arg_list) else 1,
        return lambda operand_list, meta: meta.add_to_input_list(operand_list[:operand_slicing_parameter])


    # TODO: implement this for all flags and options

    def transformers_for_args_grep(arg, meta):
        match arg:
            case _: pass
