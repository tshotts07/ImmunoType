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

# Future Decisions

Document future discussions involving:

- Dataset choices
- Analysis workflow
- Model architecture
- Evaluation methods
- Experiment tracking
- Publication plans