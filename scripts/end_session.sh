#!/bin/bash

echo "====================================="
echo " ImmunoType Research Session - END "
echo "====================================="

echo ""
echo "Date:"
date

echo ""
echo "====================================="
echo "Git Changes"
echo "====================================="

echo ""
echo "Status:"
git status

echo ""
echo "Changed files:"
git diff --stat

echo ""
echo "Detailed changes:"
git diff

echo ""
echo "====================================="
echo "Repository Structure"
echo "====================================="

tree -a -L 3 -I ".git|.venv"

echo ""
echo "====================================="
echo "Environment Check"
echo "====================================="

echo ""
echo "Python:"
python --version

echo ""
echo "Virtual Environment:"
echo $VIRTUAL_ENV

echo ""
echo "Important packages:"
pip list | grep -E "scanpy|anndata|numpy|pandas|scipy|sklearn|xgboost|torch|shap|matplotlib|seaborn|jupyter|umap"

echo ""
echo "Jupyter kernels:"
jupyter kernelspec list

echo ""
echo "====================================="
echo "Suggested Git Commands"
echo "====================================="

echo ""
echo "Review changes above."
echo ""
echo "If ready:"
echo "git add ."
echo 'git commit -m "describe your changes"'
echo "git push"

echo ""
echo "====================================="
echo "Session complete"
echo "====================================="
