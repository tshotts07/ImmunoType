# ImmunoType Research Log

## Project Overview

**ImmunoType** is a computational immunology research project investigating whether machine learning can accurately classify peripheral blood mononuclear cell (PBMC) immune cell types from single-cell RNA sequencing (scRNA-seq) data while identifying the genes that contribute most strongly to model predictions.

### Core Research Question

> Can machine learning accurately classify PBMC immune cell types from scRNA-seq data, and which genes contribute most to those predictions?

This document records the scientific progress of the project. Each phase documents the research objectives, experiments, observations, decisions, and conclusions that guide the development of the analysis pipeline.

---

# Phase 0 — Preparation

## Objective

Prepare a reproducible research environment for computational analysis.

## Activities

- Created the ImmunoType repository.
- Established a reproducible directory structure.
- Configured the Python development environment.
- Designed the notebook organization around research objectives.

## Findings

No biological or computational findings were generated during this phase.

## Decisions

- Separate preprocessing, modeling, evaluation, and interpretation into distinct research phases.
- Record scientific decisions alongside code implementation.

## Status

Complete

---

# Phase 1 — Dataset Exploration

## Objective

Evaluate candidate PBMC datasets and determine their suitability for preprocessing development, supervised classification, and biological interpretation.

---

## PBMC3K Dataset

### Activities

Loaded the Scanpy PBMC3K dataset and examined:

- `adata.X`
- `adata.obs`
- `adata.var`
- `adata.uns`

### Dataset Dimensions

- **Cells:** 2,700
- **Genes:** 32,738

### Findings

- Contains full-transcriptome gene expression data.
- Does not include immune-cell annotations suitable for supervised machine learning.
- Appropriate for developing and validating a preprocessing workflow.

---

## PBMC68K Reduced Dataset

### Activities

Loaded `pbmc68k_reduced` and inspected its processed expression matrix, metadata, embeddings, and immune-cell labels.

### Dataset Dimensions

- **Cells:** 700
- **Genes:** 765

### Available Metadata

- Cell-type labels (`bulk_labels`)
- QC metrics
- PCA
- UMAP
- Highly variable genes
- Neighbor graph
- Marker-gene analysis

### Immune Cell Types

- Dendritic cells
- CD14+ monocytes
- CD19+ B cells
- CD4+ T-cell subsets
- CD8+ T-cell subsets
- CD56+ NK cells
- CD34+ progenitor cells

### Findings

- Suitable for supervised pipeline development.
- Already heavily preprocessed.
- Reduced feature space limits biological interpretation.
- Class imbalance should be considered during model evaluation.

## Phase 1 Decisions

- Use PBMC3K as the preprocessing development dataset.
- Use PBMC68K Reduced as the machine-learning development dataset.
- Transition to a larger annotated PBMC dataset for final experiments and biological interpretation.

## Status

Complete

---

# Phase 2 — Preprocessing

## Objective

Develop a transparent and scientifically justified preprocessing workflow for raw PBMC scRNA-seq data.

---

## 2.1 Preprocessing Audit of PBMC68K Reduced

### Objective

Determine the preprocessing state of the development dataset.

### Activities

- Inspected the AnnData object.
- Compared `adata.X` and `adata.raw.X`.
- Examined stored metadata.
- Investigated matrix formats.

### Findings

#### Matrix Structure

- `adata.X` is a dense scaled matrix.
- `adata.raw.X` is a sparse normalized expression matrix.
- No additional expression layers exist.

#### Confirmed Downstream Analyses

Metadata confirms:

- PCA
- Neighbor graph construction
- Louvain clustering
- Marker-gene identification using logistic regression

Marker analysis used:

- `groupby="bulk_labels"`
- `reference="rest"`
- `use_raw=True`

### Conclusion

PBMC68K Reduced is an analysis-ready dataset.

Normalization parameters cannot be directly recovered and therefore should not be assumed.

---

## 2.2 Proposed Preprocessing Workflow

1. Load raw counts.
2. Calculate QC metrics.
3. Inspect QC distributions.
4. Filter low-quality cells.
5. Filter low-information genes.
6. Normalize sequencing depth.
7. Log-transform expression values.
8. Identify highly variable genes.
9. Scale expression values.
10. Perform dimensionality reduction.
11. Prepare machine-learning feature matrices.

Every preprocessing step should have a biological or statistical justification.

---

## 2.3 Raw PBMC3K Inspection

### Dataset Structure

- 2,700 cells
- 32,738 genes
- Sparse CSR count matrix
- No cell metadata
- No stored preprocessing

### Conclusion

PBMC3K appears to contain genuine raw count data suitable for preprocessing development.

---

## 2.4 Quality Control

### Quality Metrics

Quality control was based on:

- Total counts per cell
- Number of detected genes
- Percentage mitochondrial RNA
- Ribosomal RNA percentage (informational only)

Summary statistics and visual inspection showed:

- Most cells contained approximately 700–1,000 detected genes.
- Most cells contained approximately 1,500–3,000 counts.
- Most cells contained approximately 2% mitochondrial RNA.
- Only a small number of mitochondrial outliers were observed.
- Overall dataset quality appeared high.

Filtering thresholds were selected after examining the empirical distributions rather than applying tutorial defaults.

---

## 2.5 Cell Filtering

### Candidate Thresholds

| Criterion | Cells Removed |
|-----------|--------------:|
| <200 genes | 0 |
| <300 genes | 15 |
| >2500 genes | 5 |
| >3000 genes | 2 |
| >5% mitochondrial RNA | 57 |
| >10% mitochondrial RNA | 6 |

### Final Criteria

Cells were retained when they satisfied:

- ≥300 detected genes
- <5% mitochondrial RNA

### Rationale

Thresholds were selected using both published guidance and the observed distributions within PBMC3K.

High-gene-count cells were not removed because elevated complexity alone cannot distinguish true biological cells from doublets.

### Filtering Outcome

Original cells:

- **2,700**

Remaining cells:

- **2,633**

Removed cells:

- **67**

Percentage removed:

- **2.48%**

### Conclusion

Only a small proportion of cells required removal, indicating that PBMC3K was already a high-quality dataset.

---

## 2.6 Gene Filtering

### Candidate Thresholds

| Minimum Cells | Genes Removed |
|--------------|--------------:|
| 1 | 16,132 |
| 3 | 19,046 |
| 5 | 20,192 |
| 10 | 21,620 |

### Final Criterion

Genes were retained only if detected in **three or more cells**.

### Rationale

Gene filtering was treated strictly as technical quality control.

Genes observed in only one or two cells provide insufficient observations for reliable downstream analysis and substantially increase matrix sparsity.

This filtering step **does not imply biological irrelevance**.

Predictive importance will instead be determined later through:

- Highly variable gene selection
- Machine-learning models
- SHAP interpretation

### Filtering Outcome

Genes before filtering:

- **32,738**

Genes after filtering:

- **13,692**

Genes removed:

- **19,046**

Percentage removed:

- **58.18%**

### Conclusion

Despite removing over half of the original genes, the filtered dataset retains more than 13,000 genes, providing ample information for downstream preprocessing and classification.

---

## Phase 2 Progress

### Completed

- Preprocessing audit
- Raw dataset inspection
- Quality-control metric calculation
- QC visualization
- Cell filtering
- Gene filtering

### Remaining

- Normalize counts
- Log transformation
- Highly variable gene selection
- Scaling
- PCA
- Machine-learning feature preparation

## Current Status

Phase 2 is approximately **45% complete**.

The quality-control stage is complete.

The next session will begin with normalization and log transformation.

---

## Notes for the Final Paper

The Methods section should justify preprocessing decisions using both:

- Published scRNA-seq preprocessing literature.
- Empirical evidence observed within the PBMC3K dataset.

This combination provides stronger methodological support than relying solely on conventional tutorial thresholds.