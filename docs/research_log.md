# ImmunoType Research Log

## Overview

This document tracks the research progress of the ImmunoType project.

Each section represents a project phase and documents the research activities, experiments, observations, and conclusions from that phase.

---

# Phase 0 — Preparation

## Objective

Prepare the project environment so that research and analysis workflows can begin.

---

## Research Activities

No biological or computational research experiments were performed during this phase.

Phase 0 focused on preparing the foundation required for future research activities.

---

## Current Status

The research environment is prepared for initial analysis.

---

## Findings

No research findings were generated during this phase.

---

# Phase 1 — Dataset Exploration

## Objective

Evaluate candidate datasets for the ImmunoType project and determine whether they are suitable for supervised immune cell classification.

---

## Research Activities

### PBMC 3k Dataset

Loaded the PBMC 3k dataset provided by Scanpy and explored the AnnData object.

The following components were inspected:

- `adata.X` – Gene expression matrix
- `adata.obs` – Cell metadata
- `adata.var` – Gene metadata
- `adata.uns` – Unstructured metadata

**Dataset dimensions**

- 2,700 cells
- 32,738 genes

---

### PBMC68k Reduced Dataset

Loaded the Scanpy `pbmc68k_reduced` dataset and examined its metadata and available cell labels.

**Dataset dimensions**

- 700 cells
- 765 genes

**Available metadata**

- Cell type labels (`bulk_labels`)
- Quality control metrics
- PCA and UMAP embeddings
- Highly variable gene annotations

**Observed immune cell populations**

- Dendritic cells
- CD14+ Monocytes
- CD19+ B cells
- CD4+ T-cell subsets
- CD8+ T-cell subsets
- CD56+ NK cells
- CD34+ progenitor cells

---

## Findings

- The PBMC 3k dataset contains gene expression data but does not include cell-type annotations required for supervised machine learning.
- The PBMC68k reduced dataset contains annotated immune cell identities suitable for supervised classification.
- The PBMC68k reduced dataset is already preprocessed and contains a reduced number of cells and genes, making it unsuitable as the final research dataset for feature discovery and biological interpretation.
- The PBMC68k reduced dataset exhibits class imbalance across immune cell populations, which should be considered during model evaluation.

---

## Decisions

- Use PBMC 3k as a learning dataset for understanding Scanpy and the AnnData data structure.
- Use PBMC68k reduced as the development dataset for building and validating the machine learning pipeline.
- Transition to a larger annotated PBMC dataset containing the full transcriptome for the final experimental analysis and biological interpretation.