#!/bin/zsh
# usage: run_rotation.sh   (about 10 minutes); results in scratch/rot/results/<variant>/<parser>/
cd /Users/ppatel/Documents/living-synthesis/pipeline/misc/evd-validation/table-parsers
. /Users/ppatel/.cache/lives-bench/env.sh
PY=/Users/ppatel/.cache/lives-bench/venv-tables/bin/python
for v in rot0 rot90 rot270 img0 img90; do
  $PY run_pymupdf.py scratch/rot/pages_$v.json scratch/rot/results/$v/pymupdf
  $PY run_marker.py scratch/rot/pages_$v.json scratch/rot/results/$v/marker
  $PY run_mineru.py scratch/rot/pages_$v.json scratch/rot/results/$v/mineru
done
echo ALLDONE
