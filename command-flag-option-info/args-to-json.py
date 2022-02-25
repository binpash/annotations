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
        # find all arguments in line
        line_args = re.findall(r"-[a-zA-Z-\[\]=]+[ ]*[A-Z]*(?![a-z])", line)
        # split by spaces and commas
        for i in range(len(line_args)):
            la = re.split(" |=", line_args[i].strip())
            if len(la)>0:
                line_args[i] = la[0] if len(la)==1 else tuple(la)
        args.append(line_args)
    return args

def parse_args(args):
    """
    Flags: ['--flag']; ['-F']; ['-F', '--flag']
    Options: [('-opt', 'ARG')]; [('--opt', 'ARG')]; [('-opt', 'ARG'), ('--opt', 'ARG')]
    """
    args_dict = {"flag": [], "option": []}
    for line_args in args:
        if len(line_args)>0:
            if type(line_args[0])==str:
                args_dict["flag"].append(list(line_args))
            else:
                for arg in line_args:
                    args_dict["option"].append(list(arg))
    return args_dict

parse(sys.stdin)
