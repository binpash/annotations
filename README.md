# annotations
A repo for exploring the PaSh annotation subsystem

## oneliners
Run the `setup.sh` script in `input` first.
Commands to be run in the folder as no links (with variables) used currently.

## command-flag-option-info
Contains [command_name].json files with list of flags and options for each command. For arguments that have two options (e.g. `-a` and `--all`), store them as a pair in the format [short version, long version].

Also contains a regex-based script that can be used to generate somewhat accurate JSON files with parsed arguments.

## parser
Use command-flag-option-info JSON files to parse xbd-type terminal commands.
Will split on spaces (`" "`) and equal signs (`"="`).

## input-output-annotations
Class to hold parsed terminal command data.

# terms
- flag = takes no arguments, e.g. `--verbose`
- option = takes arguments, e.g. `-n 10`
- operand = argument with no flag, e.g. `input.txt`
