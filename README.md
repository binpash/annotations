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
- Add a json file with the command flags in (https://github.com/binpash/annotations/tree/main/pash_annotations/parser/command_flag_option_info/data). This could be used to generate a first version of it: (https://github.com/binpash/annotations/blob/main/pash_annotations/parser/command_flag_option_info/manpage-to-json.sh).
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

# How to Add a New Command to PaSh's Annotation System

This guide explains how to manually create InputOutputInfo and ParallelizabilityInfo generators for a new command in PaSh.


### **Step 1: Add the Command to the Name Mapping**

PaSh uses a dictionary to map shell command names to Python class names. To register a new command:

1. Open **`AnnotationGeneration.py`** (or the relevant file where `DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES` is defined).
2. Add an entry for the new command:

   ```python
   DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES = {
       ...
       "<command-name>": "<ClassRepresentation>",  # Add your new command here
       ...
   }
### **Step 2: Create the InputOutputInfo and ParallelizabilityInfo Generator files**

Each command requires an InputOutputInfo and ParallelizabilityInfo generator, which determines how it handles input and output files.

Navigate to:

```sh
pash_annotations/annotation_generation/annotation_generators/
```

Create a two files named:

 ```sh
InputOutputInfoGenerator<ClassRepresentation>.py
ParallelizabilityInfo<ClassRepresentation>.py
```

If your command is "cat-wrapper", the file should be:

```sh
InputOutputInfoGeneratorCatWrapper.py
ParallelizabilityInfoCatWrapper.py
```


### **Step 3: Implement the InputOutputInfo and ParallelizabilityInfo Generators**

Inside the newly created files, define a class that **inherits from the appropriate interface**:

- **For Input/Output Behavior**: Inherit from `InputOutputInfoGeneratorInterface`
- **For Parallelization Behavior**: Inherit from `ParallelizabilityInfoGeneratorInterface`

### **InputOutputInfo Generator**
In the **InputOutputInfo generator**, specify how your command processes input and produces output. This includes:
- How the command **reads input**.
- Whether it **writes to stdout** or modifies files in place.
- How **each flag affects input and output behavior**.

For example:
- Commands like `cat` read from **stdin** or files and write to **stdout**.
- Commands like `mv` modify files **in place** without stdout output.
- Commands like `grep` take both **input files and options** that affect behavior.

---

### **ParallelizabilityInfo Generator**
In the **ParallelizabilityInfo generator**, define what parallelization strategies can be applied while maintaining **correct execution**. Consider:
- Whether the command can process input **in independent chunks** (e.g., `sort` can, but `grep` with `-A` or `-B` cannot).
- Whether it can be **executed in parallel** on separate input files.
- Whether it requires **ordering constraints** to maintain correctness.

For example:
- `sort` can process chunks **independently**, then merge results.
- `wc` can process chunks **independently**, and would then sum up the results.
- `cat` with no flags is **stateless**, so the default options work.

By implementing these details, you ensure **efficient parallel execution** while preserving the **functional correctness** of your command.




