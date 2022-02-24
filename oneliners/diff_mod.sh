#!/bin/bash
# Compares two streams element by element
# Taken from https://crashingdaily.wordpress.com/2008/03/06/diff-two-stdout-streams/
# shuf() { awk 'BEGIN {srand(); OFMT="%.17f"} {print rand(), $0}' "$@" | sort -k1,1n | cut -d ' ' -f2-; }

# IN=${IN:-$PASH_TOP/evaluation/benchmarks/oneliners/input/1G.txt}

IN1=input/diff-input-1.txt
IN2=input/diff-input-2.txt

rm -f diff-output/*

mkfifo s1 s2

cat $IN1 |
  # shuf |
  tee diff-output/f1-1.txt |
  tr [:lower:] [:upper:] |
  tee diff-output/f1-2.txt |
  sort > s1 &

cat $IN2 |
  # shuf |
  tr [:lower:] [:upper:] |
  sort > s2 &

diff -B s1 s2
rm s1 s2
