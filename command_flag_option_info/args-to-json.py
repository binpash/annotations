import re
import sys
import json

def find_matches(line, past_flags):
    # TODO: for mv, it recognizes 2 options as flags: -S and -t (manually fixed for now)
    """
    Patterns to match (will be separated with ", "):
       ['--opt ARG', '--opt=ARG', '--opt[=ARG]', '-o ARG', '-O ARG'
        '-o=ARG', '-O=ARG', '-opt[=ARG]', '-f', '-F', '--flag']

    Patterns NOT to match: 
        ['-ARG', '--ARG', 'command descriptions']
    """
    # remove "[" and "]" from line
    line = re.sub(r"\[|\]", '', line)

    # store all flags & options in line
    xbd_args = []

    # arguments are comma-separated
    phrases = re.split(", ", line)

    # parse line and get xbd flags & options
    for i in range(len(phrases)):
        # remove starting and ending spaces
        phrases[i] = phrases[i].strip()

        # option flag and argument separated by space or equal sign
        if "=" in phrases[i]:
            phrase_parts = re.split(r"=", phrases[i])
        else:
            phrase_parts = re.split(r"\s+", phrases[i])

        if len(phrase_parts) >= 1 and (re.match(r"^-[-]*[a-z][a-z-]*$", phrase_parts[0]) or re.match(r"^-[-]*[A-Z]$", phrase_parts[0])):
            flag = re.sub("-", '', phrase_parts[0])
            # ignore duplicate flags
            if flag not in past_flags:
                past_flags.add(flag)
                if (len(phrase_parts) > 1) and (re.match(r"^[A-Z]+$", phrase_parts[1])):
                    xbd_args.append([phrase_parts[0], phrase_parts[1]])
                else:
                    xbd_args.append(phrase_parts[0])

    # return xbd flags & options in line
    return (xbd_args, past_flags)

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

def parse_lines(lines):
    """
    Return list of args in man page as JSON object.
    """
    # keep track of past flags & ignore duplicates 
    past_flags = set()

    # list of xbd args
    args = []
    for line in lines:
        line_args, past_flags = find_matches(line, past_flags)
        if line_args != []:
            args.append(line_args)

    # parse and return args
    return parse_args(args)

def parse(lines):
    args_dict = parse_lines(lines)
    json_formatted_args = json.dumps(args_dict, indent=4)
    print(json_formatted_args)

parse(sys.stdin)
