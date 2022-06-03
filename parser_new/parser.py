from __future__ import annotations
from typing import Set, Literal, List

import json
import shlex
import os
from enum import Enum
from datatypes_new.BasicDatatypes import FlagOption, Flag, Option, Operand, FileName, ArgStringType
from datatypes_new.CommandInvocationInitial import CommandInvocationInitial
from config_new.definitions import ROOT_DIR


def parse(command) -> CommandInvocationInitial:

    # split all terms (command, flags, options, arguments, operands)
    parsed_elements_list : list[str] = shlex.split(command)

    # add command name to xbd list
    cmd_name: str = parsed_elements_list[0]
    command_json_fn = f'{cmd_name}.json'

    # TODO: if there is an element "\n", we lose the quotation marks currently

    # get man page data for command as dict
    command_json_fn_absolute : str = os.path.join(ROOT_DIR, 'command_flag_option_info/data', command_json_fn)
    try:
        with open(command_json_fn_absolute) as f:
            json_data = json.load(f)
    except FileNotFoundError:
        print(f'Error: File {command_json_fn_absolute} not found.')
        raise Exception(f'File {command_json_fn_absolute} not found.')

    set_of_all_flags: Set[str] = get_set_of_all_flags(json_data)
    dict_flag_to_primary_repr: dict[str, str] = get_dict_flag_to_primary_repr(json_data)
    set_of_all_options: Set[str] = get_set_of_all_options(json_data)
    dict_option_to_primary_repr: dict[str, str] = get_dict_option_to_primary_repr(json_data)
    dict_option_to_class_for_arg: dict[str, WhichClassForArg] = get_dict_option_to_class_for_arg(json_data)

    # parse list of command invocation terms
    flag_option_list: List[FlagOption] = []
    i = 1
    while i < len(parsed_elements_list):
        potential_flag_or_option = parsed_elements_list[i]
        if potential_flag_or_option in set_of_all_flags:
            flag_name_as_string: str = dict_flag_to_primary_repr.get(potential_flag_or_option, potential_flag_or_option)
            flag: Flag = Flag(flag_name_as_string)
            flag_option_list.append(flag)
        elif (potential_flag_or_option in set_of_all_options) and ((i+1) < len(parsed_elements_list)):
            option_name_as_string: str = dict_option_to_primary_repr.get(potential_flag_or_option, potential_flag_or_option)
            option_arg_as_string: str = parsed_elements_list[i+1]
            option = get_option_from_name_and_untyped_arg(dict_option_to_class_for_arg, option_arg_as_string, option_name_as_string)
            flag_option_list.append(option)
            i += 1  # since we consumed another term for the argument
        elif are_all_individually_flags(potential_flag_or_option, set_of_all_flags):
            for split_el in list(potential_flag_or_option[1:]):
                flag: Flag = Flag(f'-{split_el}')
                flag_option_list.append(flag)
        else:
            break  # next one is Operand, and we keep these in separate list
        i += 1

    # we would probably want to skip '--' but then the unparsed command could have a different meaning so we'd need to keep it
    # for now, omitted
    # if parsed_elements_list[i] == '--':
    #     i += 1

    operand_list = [Operand(operand_name) for operand_name in parsed_elements_list[i:]]

    return CommandInvocationInitial(cmd_name, flag_option_list, operand_list)


def get_option_from_name_and_untyped_arg(dict_option_to_class_for_arg, option_arg_as_string, option_name_as_string):
    option_arg_kind = dict_option_to_class_for_arg[option_name_as_string]
    if option_arg_kind == WhichClassForArg.FILENAME:
        option_arg = FileName(option_arg_as_string)
    elif option_arg_kind == WhichClassForArg.ARGSTRING:
        option_arg = ArgStringType(option_arg_as_string)
    else:
        raise Exception('unknown kind for option argument')
    return Option(option_name_as_string, option_arg)


def get_set_of_all_flags(json_data) -> Set[str]:
    return get_set_of_all("flag", json_data)


def get_set_of_all_options(json_data) -> Set[str]:
    return get_set_of_all("option", json_data)


def get_set_of_all(flag_or_option_str: Literal["flag", "option"], json_data) -> Set[str]:
    set_of_all: set[str] = set()
    for flag_list in json_data[flag_or_option_str]:
        for flag in flag_list:
            set_of_all.add(flag)
    return set_of_all


def get_dict_flag_to_primary_repr(json_data):
    dict_flag_to_primary_repr: dict[str, str] = dict()
    for list_of_equiv_flag_repr in json_data["flag"]:
        for i in range(1, len(list_of_equiv_flag_repr)):
            dict_flag_to_primary_repr[list_of_equiv_flag_repr[i]] = list_of_equiv_flag_repr[0]
    return dict_flag_to_primary_repr

def get_dict_option_to_primary_repr(json_data):
    dict_option_to_primary_repr: dict[str, str] = dict()
    for list_of_equiv_flag_repr in json_data["option"]:
        for i in range(1, len(list_of_equiv_flag_repr) - 1):    # last one contains type
            dict_option_to_primary_repr[list_of_equiv_flag_repr[i]] = list_of_equiv_flag_repr[0]
    return dict_option_to_primary_repr

def get_dict_option_to_class_for_arg(json_data) -> dict[str, WhichClassForArg]:
    dict_option_to_class_for_arg: dict[str, WhichClassForArg] = dict()
    for option_data in json_data["option"]:
        option_name = option_data[0]
        option_arg_type = option_data[-1]
        if option_arg_type == 'FILE' or option_arg_type == 'GLOB' or option_arg_type == 'DIR':
            # for now, we do not allow to have '-' for stdin in option arguments
            dict_option_to_class_for_arg[option_name] = WhichClassForArg.FILENAME
        else:
            dict_option_to_class_for_arg[option_name] = WhichClassForArg.ARGSTRING
    return dict_option_to_class_for_arg

def are_all_individually_flags(potential_flag_or_option, set_of_all_flags):
    if potential_flag_or_option[0] != '-':
        return False
    return all(f'-{split_el}' in set_of_all_flags for split_el in list(potential_flag_or_option[1:]))

class WhichClassForArg(Enum):
    FILENAME = 'filename'
    ARGSTRING = 'argstring'
