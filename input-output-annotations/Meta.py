class Meta:

    def __init__(self, input_list=[], output_list=[], custom_info=None):
        self.input_list = input_list
        self.output_list = output_list
        self.custom_info = custom_info

    def __str__(self):
        return f'meta: ' \
            + f'input_list: {self.input_list}\n' \
            + f'output_list: {self.output_list}\n' \
            + f'custom_info: {self.custom_info}'

    def get_input_list(self):
        return self.input_list

    def add_to_input_list(self, input_list_to_be_added: list):
        self.input_list.extend(input_list_to_be_added)

    def prepend_to_input_list(self, input_el_to_be_added):
        self.input_list.insert(0, input_el_to_be_added)

    def add_to_output_list(self, output_list_to_be_added: list):
        self.output_list.extend(output_list_to_be_added)
