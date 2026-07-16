# Developer Quick Referencing

## Clone the Repo

```bash
git clone https://github.com/<username>/ImmunoType.git
cd ImmunoType
```

---

## Create the Virtual Environment (first time only)

```bash
python3 -m venv .venv
```

---

## Activate the venv

macOS / Linux

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

---

## Deactivate the Virtual Environment

```bash
deactivate
```

---

## Update requirements.txt

After installing new packages:

```bash
pip list
```

---

## Check python version

```bash
python --version
```

---

## Check which Python is being used

```bash
which python
```

Should return something similar to:

```

.../ImmunoType/.venv/bin/python
```

---

# Useful Git Commands (I always forget too)

## Check Repo status

```bash
git status
```

---

## Stage All Changes

```bash
git add .
```

---

## Stage One File

```bash
git add README.md
```

---

## Commit Changes

```bash
git commit -m "Meaningful commit message"
```

Example:

```bash
git commit -m "Implement Scanpy preprocessing pipeline"
```

--- 

## Push Changes

```bash
git push
```

---

## Pull latest Changes

```bash
git pull
```

---

## View Commit History

```bash
git log --online
```

---

## Switch Branches

```bash
git checkout main
```

---

# Jupyter

## Start Jupyter Lab

```bash
jupyter lab
```

---

# Running Python Files

Run a script:
```bash
python src/train.py
```

---

# Useful Commands

List project files

```bash
ls
```

Current Directory:

```bash
pwd
```

Move into a folder:

```bash
cd data/raw
```

Move up one directory:

```bash
cd ...
```

Clear terminal:

```bash
clear
```

---

# Project Startup Checklist

1. Open terminal
2. Navigate to project

```bash
cd ~/Documents/GitHub/ImmunoType
```

3. Activate virtual environment

```bash
source.venv/bin/activate
```

4. Open VS code

```bash
code .
```

5. Pull latest changes

```bash
git pull
```

6. Work
   