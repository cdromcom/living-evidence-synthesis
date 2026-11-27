#!/bin/zsh
# usage: run_supp.sh ; supplementary files with all four readers (about 10 to 20 minutes)
cd /Users/ppatel/Documents/living-synthesis/pipeline/misc/evd-validation/table-parsers
. /Users/ppatel/.cache/lives-bench/env.sh
PY=/Users/ppatel/.cache/lives-bench/venv-tables/bin/python
for p in reader pymupdf marker mineru; do $PY run_supp.py $p; done
echo ALLDONE
