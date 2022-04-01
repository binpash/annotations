from util import make_arg_simple
from datatypes.Operand import Operand
from annotation_generation.datatypes.parallelizability.Parallelizer import Parallelizer
from annotation_generation.datatypes.parallelizability.Mapper import Mapper
from annotation_generation.datatypes.parallelizability.Aggregator import Aggregator

import annotation_generation.AnnotationGeneration as AnnotationGeneration

cmd_name = "cat"


def test_cat_1() -> None:
    args = [make_arg_simple(["-b"]), make_arg_simple(["-e"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 2
    assert len(meta.get_output_list()) == 2     # stdout and stderr

    assert len(meta.get_parallelizer_list()) == 2
    [parallelizer1, parallelizer2] = meta.get_parallelizer_list()
    par1ret = Parallelizer.make_parallelizer_indiv_files()
    par2ret = Parallelizer.make_parallelizer_round_robin()
    assert parallelizer1 == par1ret
    assert parallelizer2 == par2ret


def test_cat_2() -> None:
    args = []
    operands = [Operand("in1.txt"),
                Operand("-"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 3
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 2
    [parallelizer1, parallelizer2] = meta.get_parallelizer_list()
    assert parallelizer1 == Parallelizer.make_parallelizer_indiv_files()
    assert parallelizer2 == Parallelizer.make_parallelizer_round_robin()


def test_cat_3() -> None:
    args = [make_arg_simple(["-n"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 2
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 2
    [parallelizer1, parallelizer2] = meta.get_parallelizer_list()
    assert parallelizer1 == Parallelizer.make_parallelizer_indiv_files(mapper=Mapper.make_mapper_custom("cus"))
    assert parallelizer2 == Parallelizer.make_parallelizer_round_robin(mapper=Mapper.make_mapper_custom("cus"))


def test_cat_4() -> None:
    args = [make_arg_simple(["-n"]), make_arg_simple(["-s"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 2
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 0


def test_cat_5() -> None:
    args = [make_arg_simple(["-s"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 2
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 2
    [parallelizer1, parallelizer2] = meta.get_parallelizer_list()
    assert parallelizer1 == Parallelizer.make_parallelizer_indiv_files(aggregator=Aggregator.make_aggregator_adj_lines_func("squeeze_blanks"))
    assert parallelizer2 == Parallelizer.make_parallelizer_round_robin(aggregator=Aggregator.make_aggregator_adj_lines_func("squeeze_blanks"))

