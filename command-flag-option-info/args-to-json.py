import re
import sys
import json

def parse(lines):
    args_list = parse_lines(lines)
    args_dict = parse_args(args_list)
    json_formatted_args = json.dumps(args_dict, indent=4)
    print(json_formatted_args)

def parse_lines(lines):
    """
    Patterns to match (will be separated with ", ") =
       ['--opt ARG', '--opt=ARG', '--opt[=ARG]', '-o ARG', '-O ARG'
        '-o=ARG', '-O=ARG', '-opt[=ARG]', '-f', '-F', '--flag']
    """
    args = []
    for line in lines:
        # remove [] from line
        line = re.sub(r"\[|\]", '', line)
        # find all arguments in line; generally separated by commas
        line_args = re.findall(r"-[a-zA-Z-\[\]=]+[ ]*[A-Z]*(?![a-z])", line)
        # remove empty line args
        line_args = [arg for arg in line_args if arg != ""]
        # split by spaces and equal signs
        for i in range(len(line_args)):
            la = re.split(" |=", line_args[i].strip())
            if len(la)>0:
                line_args[i] = la[0] if len(la)==1 else tuple(la)
        # ignore empty lists
        if line_args != []:
            args.append(line_args)
    return args

def parse_args(args):
    """
    Flags: ['--flag']; ['-F']; ['-F', '--flag']
    Options: [('-opt', 'ARG')]; [('--opt', 'ARG')]; [('-opt', 'ARG'), ('--opt', 'ARG')]
    """
    args_dict = {"flag": [], "option": []}
    for line_args in args:
        if all([type(arg)==str for arg in line_args]):
            args_dict["flag"].append(list(line_args))
        else:
            for arg in line_args:
                if type(arg)==str:
                    args_dict["flag"].append(arg)
                else:
                    args_dict["option"].append(list(arg))
    return args_dict

parse(sys.stdin)