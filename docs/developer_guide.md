# ImmunoType Developer Guide

## Overview

This document contains the setup instructions and development workflow for the ImmunoType project.

ImmunoType is a research project focused on single-cell analysis and machine learning workflows.

Current development environment:

- Operating System: macOS
- Python: 3.12.x
- Virtual Environment: `.venv`
- Package Manager: pip
- Notebook Environment: JupyterLab
- Version Control: Git + GitHub

Main research libraries:

- Scanpy
- AnnData
- NumPy
- Pandas
- scikit-learn
- PyTorch
- SHAP
- XGBoost
- matplotlib
- seaborn
- umap-learn


---

# Repository Location

Current repository:

```bash
~/Documents/GitHub/ImmunoType
```

Move into the repository:

```bash
cd ~/Documents/GitHub/ImmunoType
```


---

# Virtual Environment

## Create the Virtual Environment

Only needed the first time:

```bash
python3 -m venv .venv
```


## Activate the Virtual Environment

macOS / Linux:

```bash
source .venv/bin/activate
```


After activation the terminal should show:

```bash
(.venv)
```


## Deactivate the Virtual Environment

```bash
deactivate
```


## Verify Python Version

```bash
python --version
```

Expected:

```text
Python 3.12.x
```


## Verify Python Location

```bash
which python
```

Expected:

```text
.../ImmunoType/.venv/bin/python
```


---

# Installing Dependencies

Install from requirements:

```bash
pip install -r requirements.txt
```


Install exact locked versions:

```bash
pip install -r requirements-lock.txt
```


After installing new packages:

```bash
pip freeze > requirements-lock.txt
```


---

# VS Code Workflow

Open the project:

```bash
code .
```


VS Code should automatically detect:

```
ImmunoType/.venv
```

as the Python interpreter.


To manually select:

1. Open Command Palette
2. Select:

```
Python: Select Interpreter
```

3. Choose:

```
.venv/bin/python
```


---

# Starting a Research Session

The project uses external helper scripts stored outside the repository.

Location:

```bash
~/Documents/dev-tools/ImmunoType/
```


## Start Session

Run:

```bash
~/Documents/dev-tools/ImmunoType/start_session.sh
```


The script checks:

- Current date/time
- Repository location
- Virtual environment
- Python version
- Git status
- Latest commits
- Installed packages
- Import availability
- Jupyter installation


The script can optionally launch JupyterLab.


---

# Ending a Research Session

Run:

```bash
~/Documents/dev-tools/ImmunoType/end_session.sh
```


The script records:

- Session date
- Current repository state
- Git status
- Latest commit
- Project structure
- Installed packages
- Import tests
- Notebook files
- Modified files


Reports are saved outside the repository:

```bash
~/Documents/dev-tools/ImmunoType/logs/
```


---

# JupyterLab

## Start JupyterLab Manually

Activate the environment:

```bash
source .venv/bin/activate
```

Launch:

```bash
jupyter lab
```


Jupyter should open in:

```text
http://localhost:8888
```


---

# Notebook Workflow

Notebooks are stored in:

```text
notebooks/
```


Current notebooks:

```text
notebooks/01_dataset_exploration.ipynb
```


Recommended workflow:

1. Activate `.venv`
2. Open JupyterLab
3. Select the ImmunoType kernel
4. Run notebook cells
5. Save results


---

# Git Workflow

## Check Status

```bash
git status
```


## Pull Latest Changes

```bash
git pull
```


## Stage Changes

```bash
git add .
```


## Commit Changes

Example:

```bash
git commit -m "Add preprocessing pipeline"
```


## Push Changes

```bash
git push
```


## View Commit History

```bash
git log --oneline
```


---

# Project Structure

```
ImmunoType/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   ├── developer_guide.md
│   ├── meeting_notes.md
│   └── research_log.md
│
├── figures/
│
├── models/
│
├── notebooks/
│
├── paper/
│
├── results/
│
├── src/
│
├── tests/
│
├── requirements.txt
└── requirements-lock.txt
```


---

# Common Commands

Current directory:

```bash
pwd
```


List files:

```bash
ls
```


Clear terminal:

```bash
clear
```


Move directories:

```bash
cd folder_name
```


Move up:

```bash
cd ..
```


---

# Troubleshooting

## Python Not Found

Check environment:

```bash
which python
```

If incorrect:

```bash
source .venv/bin/activate
```


---

## Package Import Errors

Update environment:

```bash
pip install -r requirements-lock.txt
```


---

## XGBoost macOS Error

If XGBoost cannot find OpenMP:

```bash
brew install libomp
```


Test:

```bash
python -c "import xgboost; print(xgboost.__version__)"
```


---

# Development Notes

Keep this file limited to:

- Environment setup
- Commands
- Development workflow
- Tool usage

Research decisions, experiment results, and project planning belong in:

```
docs/research_log.md
docs/meeting_notes.md
```