import argparse
from typing import Optional

# create parser
from annotation_generation.AnnotationGeneration import get_input_output_info_from_cmd_invocation, \
    get_parallelizability_info_from_cmd_invocation

from annotation_generation.datatypes.InputOutputInfo import InputOutputInfo
from annotation_generation.datatypes.ParallelizabilityInfo import ParallelizabilityInfo
from datatypes.CommandInvocationInitial import CommandInvocationInitial
from parser.parser import parse

parser = argparse.ArgumentParser()

# add arguments to the parser
parser.add_argument('--command_invocation', metavar='STRING', type=str, required=True,
                    help='specifies the command invocation to check (enclosed by \")')
parser.add_argument('--save_to', metavar='FILE', type=str, default=None,
                    help='store output in file (relative to where the script is called from); '
                         'will not overwrite existing files but then print instead')

# parse the arguments
options = parser.parse_args()

script_path = __file__
split_path = script_path.rpartition('/')
script_prefix = "".join(split_path[:2])

where_to_save = options.save_to
cmd_invocation = options.command_invocation

shall_we_write_to_file = False
if where_to_save is not None:
    shall_we_write_to_file = True
    try:
        text_file = open(script_prefix + where_to_save)
        text_file.close()
    except IOError:
        shall_we_write_to_file = False
    if not shall_we_write_to_file:
        print("There exists a file on the provided path so the result will be output (only). ")


result = ""
result += ">>> READ COMMAND INVOCATION: \n" + cmd_invocation + "\n\n"

result += ">>> PARSED COMMAND INVOCATION: \n"
command_invocation: CommandInvocationInitial = parse(cmd_invocation)
result += str(command_invocation) + "\n"

result += ">>> INPUT-OUTPUT INFORMATION (applied to command invocation if possible): \n"
io_info: Optional[InputOutputInfo] = get_input_output_info_from_cmd_invocation(command_invocation)
if io_info is None:
    result += f"Information not provided so considered side-effectful."
elif io_info.has_other_outputs():
    result += f"Provided command has outputs other than streaming."
else:
    command_invocation_with_io = io_info.apply_input_output_info_to_command_invocation(command_invocation)
    result += str(command_invocation_with_io)
result += "\n"
para_info: Optional[ParallelizabilityInfo] = get_parallelizability_info_from_cmd_invocation(command_invocation)
if para_info is None:
    para_info = ParallelizabilityInfo() # defaults to no parallelizer's and all properties False
result += ">>> PARALLELIZABILITY INFORMATION: \n"
# TODO: change representation when we move commutativity into parallelizers
result += str(para_info)

if shall_we_write_to_file:
    text_file = open(script_prefix + where_to_save, "w+")
    text_file.write(result)
    text_file.close()
else:
    print(result)
