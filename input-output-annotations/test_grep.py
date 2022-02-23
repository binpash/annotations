from Arg import Arg, make_arg_simple
from ArgKindEnum import ArgKindEnum
from Operand import Operand

import Annotation_Generation

def test_grep_1():
    cmd_name = "grep"

    args = [make_arg_simple(["-f", "dict.txt"])]

    operands = [Operand("in1.txt"), 
                Operand("in2.txt")]

    meta = Annotation_Generation.get_meta_from_cmd_invocation(cmd_name, args, operands)

    print(meta)

test_grep_1()