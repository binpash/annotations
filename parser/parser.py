from typing import Union, Set

import json
import shlex
import os
from util_flag_option import make_arg_simple
from datatypes.BasicDatatypes import FlagOption, Flag, Option, Operand, OptionArgPosConfigType, FileName, ArgStringType
from datatypes.CommandInvocation import CommandInvocation
from config.definitions import ROOT_DIR


def parse_json(command, command_json_fn) -> list[Union[str, FlagOption, Operand]]:

    # split all terms (command, flags, options, arguments, operands)
    parsed_elements_list : list[str] = shlex.split(command)

    # add command name to xbd list
    cmd_name: str = parsed_elements_list[0]

    # get man page data for command as dict
    command_json_fn_absolute : str = os.path.join(ROOT_DIR, 'command_flag_option_info', command_json_fn)
    with open(command_json_fn_absolute) as f:
        json_data = json.load(f)

    set_of_all_flags: Set[str] = get_set_of_all_flags(json_data)
    dict_flag_to_primary_repr: dict[str, str] = get_dict_flag_to_primary_repr(json_data)
    set_of_all_options = set([oplist[0] for oplist in json_data["option"]]) # ASSUMPTION: options cannot have long version
    dict_option_to_class_for_arg: dict[str, OptionArgPosConfigType | FileName] = get_dict_option_to_class_for_arg(json_data)

    # parse list of command invocation terms
    flag_option_list = []
    i = 1
    while i < len(parsed_elements_list):
        potential_flag_or_option = parsed_elements_list[i]
        if potential_flag_or_option in set_of_all_flags:
            flag_name_as_string: str = potential_flag_or_option
            if flag_name_as_string in dict_flag_to_primary_repr.keys():
                flag_name_as_string = dict_flag_to_primary_repr[flag_name_as_string]
            flag: Flag = Flag(flag_name_as_string)
            flag_option_list.append(flag)
        elif (potential_flag_or_option in set_of_all_options) and ((i+1) < len(parsed_elements_list)):
            option_name_as_string: str = potential_flag_or_option
            option_arg_as_string: str = parsed_elements_list[i+1]
            option_arg = dict_option_to_class_for_arg[option_name_as_string](option_arg_as_string)
            option: Option = Option(option_name_as_string, option_arg)
            flag_option_list.append(option)
            i += 1  # since we consumed another term for the argument
        elif are_all_individually_flags(potential_flag_or_option, set_of_all_flags):
            for split_el in list(potential_flag_or_option[1:]):
                flag: Flag = Flag(f'-{split_el}')
                flag_option_list.append(flag)
        else:
            break   # next one is Operand, and we keep these in separate list
        i += 1

    # we would probably want to skip '--' but then the unparsed command could have a different meaning so we'd need to keep it
    # for now, omitted
    # if parsed_elements_list[i] == '--':
    #     i += 1

    operand_list = [Operand(operand_name) for operand_name in parsed_elements_list[i:]]

    return CommandInvocation(cmd_name, flag_option_list, operand_list)


def get_set_of_all_flags(json_data):
    # get tags and map long tags to their short versions
    set_of_all_flags: set[str] = set()
    for flag_list in json_data["flag"]:
        for flag in flag_list:
            set_of_all_flags.add(flag)
    return set_of_all_flags

def get_dict_flag_to_primary_repr(json_data):
    dict_flag_to_primary_repr: dict[str, str] = dict()
    for list_of_equiv_flag_repr in json_data["flag"]:
        for i in range(1, len(list_of_equiv_flag_repr)):
            dict_flag_to_primary_repr[list_of_equiv_flag_repr[i]] = list_of_equiv_flag_repr[0]
    return dict_flag_to_primary_repr

def get_dict_option_to_class_for_arg(json_data):
    dict_option_to_class_for_arg: dict[str, str] = dict()
    for option_name, option_arg_type in json_data["option"]:
        if option_arg_type == 'FILE' or option_arg_type == 'GLOB':
            # for now, we do not allow to have '-' for stdin in option arguments
            dict_option_to_class_for_arg[option_name] = FileName
        else:
            dict_option_to_class_for_arg[option_name] = ArgStringType
    return dict_option_to_class_for_arg

def are_all_individually_flags(potential_flag_or_option, set_of_all_flags):
    if potential_flag_or_option[0] != '-':
        return False
    return all(f'-{split_el}' in set_of_all_flags for split_el in list(potential_flag_or_option[1:]))
