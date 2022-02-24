#!/bin/bash
# Find all 2-grams in a piece of text

# IN=${IN:-$PASH_TOP/evaluation/benchmarks/oneliners/input/1G.txt}
IN = input/bi-gram-input.txt

. bi-gram.aux_mod.sh

cat $IN |
  tee bi-gram-outputs/f1.txt |
  tr -cs A-Za-z '\n' |
  tee bi-gram-outputs/f2.txt |
  tr A-Z a-z |
  tee bi-gram-outputs/f3.txt |
  bigrams_aux |
  tee bi-gram-outputs/f8.txt |
  sort |
  tee bi-gram-outputs/f9.txt |
  uniq

