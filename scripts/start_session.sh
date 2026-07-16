#!/bin/bash

echo "======================================"
echo " ImmunoType Research Session - START "
echo "======================================"

echo ""
echo "Date:"
date

echo ""
echo "Current directory:"
pwd

echo ""
echo "Python environment:"
if [ -z "$VIRTUAl_ENV" ]; then
	echo "WARNING: Virtual Environment is NOT active"
else
	echo "Active venv: $VIRTUAL_ENV"
	python --version
fi

echo ""
echo "Virtual environment:"
echo $VIRTUAL_ENV

echo ""
echo "======================================"
echo "Git Information"
echo "======================================"

echo ""
echo "Branch:"
git branch

echo ""
echo "Remote:"
git remote -v

echo ""
echo "Status:"
git status

echo ""
echo "Latest commits:"
git log --oneline -n 10

echo ""
echo "Latest commit statistics:"
git show --stat HEAD

echo ""
echo "Pulling latest changes:"
git pull

echo ""
echo "======================================"
echo "Repository Structure"
echo "======================================"

tree -a -L 3 -I ".git|.venv"

echo ""
echo "======================================"
echo "Scientific Environment"
echo "======================================"

echo ""
echo "Important packages:"

if [ -n "$VIRTUAL_ENV" ]; then
	echo "Important packages:"
	pip list | grep -E "numpy|pandas|scanpy|anndata|sklearn|torch|xgboost|shap|jupyter"
else
	echo "Skipping package check (venv inactive)"
fi
echo ""
echo "Jupyter kernels:"

if [ -n "$VIRTUAL_ENV" ]; then
	echo "Jupyter kernels:"
	jupyter kernelspec list
else
	echo "Skipping Jupyter check (venv inactive)
fi

echo ""
echo "======================================"
echo "Ready to begin research"
echo "======================================"
