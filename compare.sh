#!/bin/bash
# Get the test diff between the previous commit and the current workspace.
# Assumes old.txt already exists.
py.test test/*.py --tb=line > new.txt
diff old.txt new.txt > diff.txt
