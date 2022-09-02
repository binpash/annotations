from copy import deepcopy
from typing import List, Union, Optional, Dict

from datatypes_new.BasicDatatypes import Flag, ArgStringType, FileNameOrStdDescriptor
from datatypes_new.BasicDatatypesWithIO import OptionWithIO, FileNameOrStdDescriptorWithIOInfo, FileNameWithIOInfo, \
    StdDescriptorWithIOInfo
from datatypes_new.AccessKind import make_stream_input, make_stream_output, AccessKind
from annotation_generation_new.datatypes.Inputs import Inputs, InputsEnum
from datatypes_new.BasicDatatypesWithIOVar import OptionWithIOVar, IOVar
from util_standard import standard_repr, standard_eq


class CommandInvocationWithIOVars:

    # TODO: get_access() will not work here anymore, use access_map

    def __init__(self,
                 cmd_name: str,
                 flag_option_list: List[Union[Flag, OptionWithIOVar]],
                 operand_list: List[Union[ArgStringType, IOVar]],
                 implicit_use_of_streaming_input: Optional[IOVar],
                 implicit_use_of_streaming_output: Optional[IOVar],
                 access_map: Dict[IOVar, AccessKind]
                 ) -> None:
        self.cmd_name: str = cmd_name
        self.flag_option_list: List[Union[Flag, OptionWithIOVar]] = deepcopy(flag_option_list)
        self.operand_list: List[Union[ArgStringType, IOVar]] = deepcopy(operand_list)
        self.implicit_use_of_streaming_input: Optional[IOVar] = deepcopy(implicit_use_of_streaming_input)
        self.implicit_use_of_streaming_output: Optional[IOVar] = deepcopy(implicit_use_of_streaming_output)
        self.access_map = deepcopy(access_map)

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other):
        return standard_eq(self, other)

    def is_aggregator_concatenate(self): # needed since isinstance(_, Aggregator) does not work
        return False

    # problematic regarding typing so removed
    # @staticmethod
    # def get_from_without_vars(cmd_inv_with_io: CommandInvocationWithIO, access_map):
    #     return CommandInvocationWithIOVars(cmd_name=cmd_inv_with_io.cmd_name,
    #                                 flag_option_list=cmd_inv_with_io.flag_option_list,
    #                                 operand_list=cmd_inv_with_io.operand_list,
    #                                 implicit_use_of_streaming_input=cmd_inv_with_io.implicit_use_of_streaming_input,
    #                                 implicit_use_of_streaming_output=cmd_inv_with_io.implicit_use_of_streaming_output,
    #                                 access_map=access_map)


    def substitute_inputs_and_outputs_in_cmd_invocation(self,
                                                        inputs_from: List[IOVar],
                                                        outputs_to: List[IOVar]) -> None:
        self.substitute_inputs_in_cmd_invocation(inputs_from)
        self.substitute_outputs_in_cmd_invocation(outputs_to)

    def substitute_inputs_in_cmd_invocation(self, inputs_from):
        def function_to_apply_to_vars(var):
            if self.access_map[var].is_stream_input():
                new_var = inputs_from.pop(0)
                return self.replace_var_consistently(var, new_var)
            else:
                return var
        self.map_var(function_to_apply_to_vars)
        assert len(inputs_from) == 0

    def substitute_outputs_in_cmd_invocation(self, outputs_to):
        def function_to_apply_to_vars(var):
            if self.access_map[var].is_stream_output():
                new_var = outputs_to.pop(0)
                return self.replace_var_consistently(var, new_var)
            else:
                return var
        self.map_var(function_to_apply_to_vars)
        assert len(outputs_to) == 0

    def generate_inputs(self):
        streaming_inputs = []
        def function_to_apply(el):
            if self.access_map[el].is_stream_input():
                streaming_inputs.append(el)
            return el
        self.map_var(function_to_apply)
        # ASSUMPTION: no configuration inputs, no fallback (no streaming inputs)
        return Inputs(InputsEnum.STREAMING, ([], streaming_inputs))

    def generate_outputs(self):
        outputs = []
        def function_to_apply(el):
            if self.access_map[el].is_any_output():
                outputs.append(el)
            return el
        self.map_var(function_to_apply)
        return outputs

    def has_other_outputs(self):
        outputs = []
        def function_to_apply(el):
            if self.access_map[el].is_other_output():
                outputs.append(el)
            return el
        self.map_var(function_to_apply)
        return len(outputs) > 0

    def replace_var_consistently(self, from_var, to_var):
        assert(from_var in self.access_map) # if this is not true, something went wrong before
        self.access_map[to_var] = self.access_map.pop(from_var)
        return to_var

    def replace_var(self, from_var, to_var):
        function_to_apply_to_var = lambda el: self.replace_var_consistently(from_var, to_var) if el == from_var else el
        self.map_var(function_to_apply_to_var)

    def flat_map_non_names_aux_flag_option_list(self, function_to_apply):
        new_flag_option_list = []
        for i in range(len(self.flag_option_list)):
            flagoption = self.flag_option_list[i]
            if isinstance(flagoption, OptionWithIO):
                [new_option_arg] = function_to_apply(flagoption.option_arg)
                new_flag_option_list.append(OptionWithIO(flagoption.option_name, new_option_arg))
            else:
                new_flag_option_list.append(flagoption)
        self.flag_option_list = new_flag_option_list

    def flat_map_non_names_aux_operand_list(self, function_to_apply):
        new_operand_list = []
        for i in range(len(self.operand_list)):
            new_operand_list += function_to_apply(self.operand_list[i])
        self.operand_list = new_operand_list

    def flat_map_non_names_aux_implicit_streaming_input(self, function_to_apply):
        result = function_to_apply(self.implicit_use_of_streaming_input)
        if result == []:
            self.implicit_use_of_streaming_input = None
        else:
            assert len(result) == 1
            self.implicit_use_of_streaming_input = result[0]

    def flat_map_non_names_aux_implicit_streaming_output(self, function_to_apply):
        result = function_to_apply(self.implicit_use_of_streaming_output)
        if result == []:
            self.implicit_use_of_streaming_output = None
        else:
            assert len(result) == 1
            self.implicit_use_of_streaming_output = result[0]

    # this determines the order in which CMDInvocations are traversed
    # _non_names as we descend into option arguments and leave option and flag names unchanged/unchecked
    def flat_map_anything_non_names(self, function_to_apply):
        self.flat_map_non_names_aux_flag_option_list(function_to_apply)
        self.flat_map_non_names_aux_operand_list(function_to_apply)
        self.flat_map_non_names_aux_implicit_streaming_input(function_to_apply)
        self.flat_map_non_names_aux_implicit_streaming_output(function_to_apply)

    def map_var(self, function_to_apply_to_vars):
        function_to_apply_to_anything = lambda el: [function_to_apply_to_vars(el)] if isinstance(el, int) else [el]
        self.flat_map_anything_non_names(function_to_apply_to_anything)

    # TODO: move to util-file command-invocation helpers
    @staticmethod
    def make_cat_command_invocation_with_io_vars(input_ids, output_id):
        access_map = {input_id: make_stream_input() for input_id in input_ids}
        access_map[output_id] = make_stream_output()
        cmd_inv_with_io_vars = CommandInvocationWithIOVars(
            cmd_name="cat",
            flag_option_list=[],
            operand_list=input_ids,
            implicit_use_of_streaming_input=None,
            implicit_use_of_streaming_output=output_id,
            access_map=access_map)
        return cmd_inv_with_io_vars

    def remove_streaming_inputs(self):
        # TODO: check whether this removes options with streaming input
        def function_to_apply(el):
           if isinstance(el, int) and self.access_map[el].is_stream_input():
               self.access_map.pop(el)
               return []
           else:
               return [el]
        self.flat_map_anything_non_names(function_to_apply)

    def remove_streaming_outputs(self):
        # TODO: check whether this removes options with streaming output
        def function_to_apply(el):
            if isinstance(el, int) and self.access_map[el].is_stream_output():
                self.access_map.pop(el)
                return []
            else:
                return [el]
        self.flat_map_anything_non_names(function_to_apply)


    # for test cases:
    def get_operands_with_config_input(self) -> List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]]:
        return [x for x in self.operand_list if
                isinstance(x, ArgStringType) or
                ((isinstance(x, FileNameWithIOInfo) or isinstance(x, StdDescriptorWithIOInfo))
                and x.access.is_config_input())]

    def get_operands_with_stream_input(self) -> List[FileNameOrStdDescriptorWithIOInfo]:
        return [x for x in self.operand_list if (isinstance(x, FileNameWithIOInfo) or isinstance(x, StdDescriptorWithIOInfo))
                and x.access.is_stream_input()]

    def get_operands_with_other_input(self) -> List[FileNameOrStdDescriptorWithIOInfo]:
        return [x for x in self.operand_list if (isinstance(x, FileNameWithIOInfo) or isinstance(x, StdDescriptorWithIOInfo))
                and x.access.is_other_input()]

    def get_operands_with_stream_output(self) -> List[FileNameOrStdDescriptorWithIOInfo]:
        return [x for x in self.operand_list if (isinstance(x, FileNameWithIOInfo) or isinstance(x, StdDescriptorWithIOInfo))
                and x.access.is_stream_output()]

    def get_operands_with_other_output(self) -> List[FileNameOrStdDescriptorWithIOInfo]:
        return [x for x in self.operand_list if (isinstance(x, FileNameWithIOInfo) or isinstance(x, StdDescriptorWithIOInfo))
                and x.access.is_other_output()]

    def get_options_with_other_output(self) -> List[OptionWithIO]:
        only_options: List[OptionWithIO] = [x for x in self.flag_option_list if isinstance(x, OptionWithIO)]
        return [x for x in only_options if
                ((isinstance(x.option_arg, FileNameWithIOInfo) or isinstance(x.option_arg, StdDescriptorWithIOInfo)))
                and x.option_arg.access.is_other_output()]
