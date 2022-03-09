import json
import shlex
import os
from datatypes.Arg import Arg, ArgKindEnum
from datatypes.Operand import Operand
from config.definitions import ROOT_DIR


# assumes that command_json_fn is the filename in folder command_flag_option_info
def parse_json(command, command_json_fn):
    command_json_fn_absolute = os.path.join(ROOT_DIR, 'command_flag_option_info', command_json_fn)
    """
    Convert terminal command invocation string to 
    [ command_name, FLAG, ..., OPTION, ..., OPERAND, ... ] list.
    """
    # split all terms (command, flags, options, operands)
    command_list = shlex.split(command)
    print(command_list)

    # add command name to xbd list
    xbd_list = [command_list[0]]

    # get man page data for command as dict
    with open(command_json_fn_absolute) as f:
        json_data = json.load(f)

    # get tags and map long tags to their short versions
    unique_tags = set()
    for flaglist in json_data["flag"]:
        for flag in flaglist:
            unique_tags.add(flag)
    tag_map = dict()
    for taglist in json_data["flag"]:
        for i in range(1, len(taglist)):
            tag_map[taglist[i]] = taglist[0]

    # get options
    unique_options = set([oplist[0] for oplist in json_data["option"]])

    # parse list of command invocation terms
    i = 1
    while i < len(command_list):
        term = command_list[i]
        if term in unique_tags:
            if term in tag_map:
                xbd_list.append(Arg(ArgKindEnum.FLAG, tag_map[term]))
            else:
                xbd_list.append(Arg(ArgKindEnum.FLAG, term))
        elif (term in unique_options) and ((i+1) < len(command_list)):
            xbd_list.append(Arg(ArgKindEnum.OPTION, (term, command_list[i+1])))
            i += 1
        else:
            xbd_list.append(Operand(term))
        i += 1

    # TODO: fix structure of result
    # return [ command_name, FLAG, ..., OPTION, ..., OPERAND, ... ] list
    # for xbd_term in xbd_list:
        # print(type(xbd_term))
        # print(xbd_term)
    return xbd_list
