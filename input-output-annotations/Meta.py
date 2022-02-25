class Meta:

    def __init__(self, 
                 input_list=None,
                 output_list=None,
                 custom_info=None):
        if input_list is None:
            self.input_list = []
        else:
            self.input_list = input_list
        if output_list is None:
            self.output_list = []
        else:
            self.output_list = output_list
        self.custom_info = custom_info

    def __str__(self):
        return f'meta: \n' \
            + f'\tinput_list: {self.input_list}\n' \
            + f'\toutput_list: {self.output_list}\n' \
            + f'\tcustom_info: {self.custom_info}'

    def get_input_list(self):
        return self.input_list

    def get_output_list(self):
        return self.output_list

    def add_list_to_input_list(self, input_list_to_be_added: list):
        self.input_list.extend(input_list_to_be_added)

    def prepend_el_to_input_list(self, el_to_be_prepended):
        self.input_list.insert(0, el_to_be_prepended)

    def add_list_to_output_list(self, output_list_to_be_added: list):
        self.output_list.extend(output_list_to_be_added)

    def prepend_el_to_output_list(self, el_to_be_prepended):
        self.output_list.insert(0, el_to_be_prepended)

    def deduplicate_input_output_lists(self):
        deduplicated_input_list = list()
        [deduplicated_input_list.append(item) for item in self.input_list if item not in deduplicated_input_list]
        self.input_list = deduplicated_input_list
        deduplicated_output_list = list()
        [deduplicated_output_list.append(item) for item in self.output_list if item not in deduplicated_output_list]
        self.output_list = deduplicated_output_list
