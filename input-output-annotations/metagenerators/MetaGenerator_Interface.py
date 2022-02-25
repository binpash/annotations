from datatypes.Meta import Meta


class MetaGeneratorInterface:

    # This is the select_subcommand from the original proposal,
    #   instead of returning functions, it initializes the object
    #   and then we can call its methods.
    def __init__(self, arg_list):
        self.meta = Meta()
        self.arg_list = arg_list

    # Roughly corresponds to this type, but updates meta in place
    #   ([Operand] x Meta) -> Meta
    def generate_operand_meta_func(self, operand_list, meta):
        pass

    # Roughly corresponds to this type, but updates meta in place
    #   Arg -> (Meta -> Meta)
    def transformers_for_args(self, arg, meta):
        pass

    def get_deduplicated_meta(self):
        self.meta.deduplicate_input_output_lists()
        return self.meta

