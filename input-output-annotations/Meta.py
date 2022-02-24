class Meta:

    def __init__(self, input_list=[], output_list=[], custom_info=None):
        self.input_list = input_list,
        self.output_list = output_list,
        self.custom_info = custom_info

    def __str__(self):
        "meta: " \
            + "input_list:" + str(self.input_list) + "\n" \
            + "output_list:" + str(self.output_list) + "\n" \
            + "custom_info:" + str(self.custom_info)

    def add_to_input_list(self, input_list_to_be_added):
        self.input_list = self.input_list.extend(input_list_to_be_added)

    def add_to_output_list(self, output_list_to_be_added):
        self.output_list = self.output_list.extend(output_list_to_be_added)
