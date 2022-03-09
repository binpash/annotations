# annotations
A repo for exploring the PaSh annotation subsystem

## folder: oneliners
Run the `setup.sh` script in `input` first.
Commands to be run in the folder as no links (with variables) used currently.

## folder: command_flag_option_info
Contains [command_name].json files with list of flags and options for each command. For arguments that have two options (e.g. `-a` and `--all`), store them as a pair in the format [short version, long version].

Also contains a regex-based script that can be used to generate somewhat accurate JSON files with parsed arguments.

## folder: parser
Use command_flag_option_info JSON files to parse xbd-type terminal commands.
Will split on spaces (`" "`) and equal signs (`"="`).

## folder: annotation_generation
TODO

# terms
- flag = takes no arguments, e.g. `--verbose`
- option = takes arguments, e.g. `-n 10`
- operand = argument with no flag, e.g. `input.txt`

# tests
Use `pytest` to run tests. 
It will run all tests found (recursively) in the current directory.

# imports
For clean imports, we add empty `__init__.py` modules in all non-root directories.
Thus, `pytest` will add the root directory to sys.path and 
we can import modules by prefixing the path from there.
For instance, to import `Parallelizer.py`, we use 
```
from annotation_generation.parallelizers.Parallelizer import Parallelizer
```