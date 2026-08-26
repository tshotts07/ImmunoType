# ImmunoType Meeting Notes

## Purpose

This document records important project discussions, design decisions, and workflow choices.

Use:

- `developer_guide.md` → setup and technical instructions
- `research_log.md` → experiments, findings, and research progress


---

# 2026-07-16

## Documentation Structure

### Discussion

Project documentation needed clearer separation between technical setup, research progress, and decisions.

### Decision

Documentation was separated into:

| File | Purpose |
|---|---|
| developer_guide.md | Setup, commands, and workflow |
| research_log.md | Research progress and experiments |
| meeting_notes.md | Decisions and discussions |

### Reason

Keeps information organized and easier to reference.


---

## Session Scripts

### Discussion

Startup and end-of-session scripts were useful for collecting project information but did not belong inside the repository.

### Decision

Moved scripts outside the repo:

```
~/Documents/dev-tools/ImmunoType/
```

Scripts:

```
start_session.sh
end_session.sh
```

### Reason

Keeps the repository clean and avoids storing personal machine-specific tools.


---

## Session Automation

### Discussion

Starting each coding session required repeating the same checks.

### Decision

The startup script should check:

- Environment status
- Git status
- Python version
- Package versions
- Import validation
- Jupyter availability

The end script should record:

- Final project state
- Git status
- Package versions
- Notebook inventory
- Session summary

### Reason

Creates a consistent development workflow and makes debugging easier.


---

## VS Code Workflow

### Discussion

Opening the project manually and running startup checks added unnecessary steps.

### Decision

Use VS Code workspace tasks to automatically run:

```
start_session.sh
```

when opening the project.

### Reason

Reduces repetitive setup steps.


---

## Python Environment

### Discussion

Scientific Python packages can have compatibility issues across versions.

### Decision

Standardize development on:

```
Python 3.12.x
```

using:

```
.venv
```

### Reason

Improves reproducibility and package stability.


---

## Dependency Management

### Discussion

Package updates can introduce unexpected changes.

### Decision

Maintain:

```
requirements.txt
```

for normal dependencies.

Maintain:

```
requirements-lock.txt
```

for exact versions.

### Reason

Allows development flexibility while preserving reproducibility.


---

# 2026-08-19

## PyTorch Thread-Pool Warmup Convention

### Discussion

Setting up tensors for the PyTorch feedforward NN baseline (Phase 4) caused the kernel to hang indefinitely on the first `torch.tensor()` call. Diagnosis traced this to PyTorch's CPU thread pool initializing for the first time *after* joblib's `n_jobs=-1` scikit-learn/XGBoost calls (Logistic Regression, XGBoost, Random Forest CV/grid-search) had already forked worker processes earlier in the session. Full diagnosis, including the ruled-out causes, is in `docs/research_log.md` (Phase 4).

### Decision

Any notebook that mixes PyTorch with `n_jobs=-1` scikit-learn/XGBoost calls must warm up PyTorch's thread pool immediately after `import torch`, before the first parallel fit runs:

```python
torch.set_num_threads(1)
_ = torch.zeros(1) + torch.zeros(1)
```

### Reason

Makes the fix a standing project convention rather than a one-off patch, so it isn't rediscovered from scratch in later notebooks that combine PyTorch with parallel scikit-learn/XGBoost calls. The reusable snippet is documented in `docs/developer_guide.md` (Troubleshooting → "PyTorch Hangs on First Tensor Op (macOS)").


---

# Future Decisions

Document future discussions involving:

- Dataset choices
- Analysis workflow
- Model architecture
- Evaluation methods
- Experiment tracking
- Publication plans