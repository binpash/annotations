#!/bin/bash
man $1 | grep '^       -' | sed -E 's/^\s+//g' | python3 args-to-json.py
