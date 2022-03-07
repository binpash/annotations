from datatypes.Arg import make_arg_simple
from datatypes.Operand import Operand
from parallelizers.ParallelizerIndivFiles import ParallelizerIndivFiles
from parallelizers.ParallelizerRoundRobin import ParallelizerRoundRobin

import AnnotationGeneration

cmd_name = "cat"


def test_cat_1():
    args = [make_arg_simple(["-b"]), make_arg_simple(["-e"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 2
    assert len(meta.get_output_list()) == 2     # stdout and stderr

    assert len(meta.get_parallelizer_list()) == 2
    assert ParallelizerIndivFiles.is_parallelizer_mapper_seq_aggregator_conc(meta.get_parallelizer_list()[0])
    assert ParallelizerRoundRobin.is_parallelizer_mapper_seq_aggregator_conc(meta.get_parallelizer_list()[1])


def test_cat_2():
    args = []
    operands = [Operand("in1.txt"),
                Operand("-"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 3
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 2
    assert ParallelizerIndivFiles.is_parallelizer_mapper_seq_aggregator_conc(meta.get_parallelizer_list()[0])
    assert ParallelizerRoundRobin.is_parallelizer_mapper_seq_aggregator_conc(meta.get_parallelizer_list()[1])


def test_cat_3():
    args = [make_arg_simple(["-n"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 2
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 2
    assert ParallelizerIndivFiles.is_parallelizer_mapper_custom_aggregator_conc(meta.get_parallelizer_list()[0], "cus")
    assert ParallelizerRoundRobin.is_parallelizer_mapper_custom_aggregator_conc(meta.get_parallelizer_list()[1], "cus")


def test_cat_4():
    args = [make_arg_simple(["-n"]), make_arg_simple(["-s"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 2
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 0


def test_cat_5():
    args = [make_arg_simple(["-s"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 2
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 2
    assert ParallelizerIndivFiles.is_parallelizer_mapper_seq_aggregator_adjf(meta.get_parallelizer_list()[0], "squeeze_blanks")
    assert ParallelizerRoundRobin.is_parallelizer_mapper_seq_aggregator_adjf(meta.get_parallelizer_list()[1], "squeeze_blanks")

