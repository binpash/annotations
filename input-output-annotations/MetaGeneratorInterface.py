from Meta import Meta


class MetaGeneratorInterface:

    def __init__(self):
        self.meta = Meta()

    def get_deduplicated_meta(self):
        self.meta.deduplicate_input_output_lists()
        return self.meta

    def generate_operand_meta_func(self, operand_list, meta):
        pass

    def transformers_for_args(self, arg, meta):
        pass
