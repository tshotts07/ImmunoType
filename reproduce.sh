#!/usr/bin/env bash
# Rebuild every ImmunoType result from a fresh clone:
#   1. download the raw PBMC3K data (checksum-verified)
#   2. execute the pipeline notebooks in order, in place, each in a fresh kernel
#
# Usage (from the repository root, with the venv active):
#   pip install -r requirements-lock.txt
#   ./reproduce.sh
#
# There is no notebook 04: Phase 3 clustering and annotation live in
# notebooks/03_preprocessing.ipynb (see README).

set -euo pipefail

cd "$(dirname "$0")"

NOTEBOOKS=(
    01_dataset_exploration
    02_dataset_validation
    03_preprocessing
    05_machine_learning
    06_gene_interpretation
)

start_total=$(date +%s)

echo "==> Downloading raw data"
python scripts/download_data.py

for nb in "${NOTEBOOKS[@]}"; do
    echo "==> Executing notebooks/${nb}.ipynb"
    start=$(date +%s)
    # notebooks use paths relative to notebooks/, so execute from there
    (
        cd notebooks
        jupyter nbconvert --to notebook --execute --inplace \
            --ExecutePreprocessor.timeout=-1 \
            --ExecutePreprocessor.record_timing=False \
            --ExecutePreprocessor.store_widget_state=False \
            "${nb}.ipynb"
    )
    echo "    done in $(( $(date +%s) - start ))s"
done

echo "==> All notebooks executed in $(( $(date +%s) - start_total ))s"
