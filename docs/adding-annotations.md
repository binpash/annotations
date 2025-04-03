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




