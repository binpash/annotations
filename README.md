# Annotations

This repository contains a framework for generating annotations for command invocations.
It comprises a parser which turns a string into a command invocation data structure.
For the time being, there are two sets of annotation generators:
- input-output information which specifies how a command invocation interacts with the files, pipes, stdin, stdout, etc.
- parallelizability information which describes how a command invocation can be parallelized - containing information about how to split inputs, mappers and aggregators, etc.

## Command-line tool
`main.py` contains a command line tool which, provided a command invocation returns:
- the parsed command invocation data structure
- the input-output information generated
- the parallelizability information generated

## Adding an annotation

- Add the command in the dictionary in (https://github.com/binpash/annotations/blob/main/pash_annotations/annotation_generation/AnnotationGeneration.py#L13)
- Add an `InputOutputInfoGeneratorXXX.py` in (https://github.com/binpash/annotations/tree/main/pash_annotations/annotation_generation/annotation_generators)
- (Optionally) add a `ParallelizabilityInfoGeneratorXXX.py` in (https://github.com/binpash/annotations/tree/main/pash_annotations/annotation_generation/annotation_generators)

## Parser
Use command_flag_option_info JSON files to parse xbd-type terminal commands.
Will split on spaces (`" "`) and equal signs (`"="`).

## Flag and Option Information
The folder command_flag_option_info contains [command_name].json files with list of flags and options for each command. 
For arguments that have two options (e.g. `-a` and `--all`), store them as a pair in the format [short version, long version].
In addition, we store here in which way an argument is accessed if applicable, e.g., if it is a file.

We also have a regex-based script that can be used to generate initial JSON files with parsed arguments.
Since there is no standard for man-pages, the quality of results varies but it usually provides a good skeleton and saves quite some time.

## Annotation Generation
Currently, annotation generators for input-output information and parallelizability information has been implemented.
Each annotation generator implements a specific generator interface (e.g., `InputOutputInfoGenerator_Interface.py`) which specializes a more general generator interface (`Generator_Interface.py`).
The general generator interface contains functions that help to check conditions on the command invocation while 
the more specific generator interface provides functionality to change the respective information (object) generated.

## Terms
- flag = takes no arguments, e.g. `--verbose`
- option = takes arguments, e.g. `-n 10`
- operand = argument with no flag, e.g. `input.txt`

## Coding

## typing 
We strive to use types and typecheck with `pyright` (v1.1.232).
This does not only help to catch bugs but shall also help future developers to understand the code more easily.

## tests
Use `pytest` to run tests. 
It will run all tests found (recursively) in the current directory.

## imports
For clean imports, we add empty `__init__.py` modules in all non-root directories.
Thus, `pytest` will add the root directory to sys.path and 
we can import modules by prefixing the path from there.
For instance, to import `Parallelizer.py`, we use 
```
from annotation_generation.parallelizers.Parallelizer import Parallelizer
```