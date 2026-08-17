# ImmunoType Research Log

## Project Overview

**ImmunoType** is a computational immunology research project investigating whether machine learning can accurately classify peripheral blood mononuclear cell (PBMC) immune cell types from single-cell RNA sequencing (scRNA-seq) data while identifying the genes that contribute most strongly to model predictions.

## Core Research Question

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

**Complete**

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

**Complete**

---

# Phase 2 — Preprocessing

## Objective

Develop a transparent, reproducible, and scientifically justified preprocessing workflow for raw PBMC scRNA-seq data.

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
2. Calculate quality-control metrics.
3. Inspect QC distributions.
4. Filter low-quality cells.
5. Filter low-information genes.
6. Normalize sequencing depth.
7. Log-transform expression values.
8. Identify highly variable genes.
9. Scale expression values.
10. Perform principal component analysis.
11. Prepare machine-learning feature matrices.

Each preprocessing step should have a biological or statistical justification.

---

## 2.3 Raw PBMC3K Inspection

### Dataset Structure

- 2,700 cells
- 32,738 genes
- Sparse CSR count matrix
- No cell metadata
- No stored preprocessing

### Conclusion

PBMC3K contains raw count data suitable for developing and validating a complete preprocessing pipeline.

---

## 2.4 Quality Control

### Quality Metrics

Quality control was based on:

- Total UMI counts per cell
- Number of detected genes per cell
- Percentage mitochondrial RNA
- Percentage ribosomal RNA (informational only)

Visual inspection and summary statistics showed:

- Most cells contained approximately 700–1,000 detected genes.
- Most cells contained approximately 1,500–3,000 total counts.
- Most cells contained approximately 2% mitochondrial RNA.
- Only a small number of mitochondrial outliers were observed.

Overall dataset quality appeared high.

Filtering thresholds were selected after examining the empirical distributions rather than relying solely on tutorial defaults.

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

Cells were retained only if they satisfied:

- ≥300 detected genes
- <5% mitochondrial RNA

### Rationale

Thresholds were selected using both published recommendations and the observed PBMC3K distributions.

High-gene-count cells were intentionally retained because elevated transcript complexity alone is insufficient evidence of doublets. Dedicated doublet-detection methods should be used instead.

### Filtering Outcome

| Metric | Value |
|--------|------:|
| Original cells | 2,700 |
| Remaining cells | 2,633 |
| Removed cells | 67 |
| Percentage removed | 2.48% |

### Conclusion

Only a small proportion of cells required removal, indicating that PBMC3K is a high-quality dataset.

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

Genes observed in only one or two cells provide insufficient observations for reliable downstream statistical analysis while substantially increasing matrix sparsity.

This filtering step **does not imply biological irrelevance**.

Biological importance will instead be determined later using:

- Highly variable gene selection
- Machine-learning models
- SHAP feature attribution

### Filtering Outcome

| Metric | Value |
|--------|------:|
| Original genes | 32,738 |
| Remaining genes | 13,692 |
| Removed genes | 19,046 |
| Percentage removed | 58.18% |

### Conclusion

Although more than half of the genes were removed, over 13,000 genes remained, preserving substantial biological information while reducing technical noise.

---

## 2.7 Library-Size Normalization

### Objective

Correct for differences in sequencing depth between individual cells.

### Method

Counts were normalized using Scanpy's total-count normalization with a target library size of **10,000 counts per cell**.

### Rationale

Observed differences in total counts largely reflect sequencing depth rather than biological variation.

Normalization places all cells on a common scale, allowing biologically meaningful comparisons of gene expression.

Raw filtered counts were preserved in:

```python
adata.layers["counts"]
```

before normalization.

### Verification

Median total counts after normalization:

- **10,000 counts per cell**

### Conclusion

Sequencing-depth differences were successfully removed while preserving filtered raw counts for future analyses.

---

## 2.8 Log Transformation

### Objective

Reduce the extreme right-skew of count data and stabilize variance.

### Method

Applied the natural logarithm transformation:

```
log(1 + x)
```

using:

```python
sc.pp.log1p()
```

### Rationale

scRNA-seq count data are highly skewed because a small number of genes are expressed at very high levels.

Log transformation compresses extreme expression values while preserving relative biological differences.

### Verification

Observed expression values ranged approximately from:

- Minimum: **0**
- Maximum: **7.47**

which is consistent with expected log-transformed expression values.

### Conclusion

Expression values were successfully transformed into a scale appropriate for downstream statistical analyses.

---

## 2.9 Highly Variable Gene Selection

### Objective

Reduce feature dimensionality while retaining genes that capture the greatest biological variation.

### Method

Highly variable genes were identified using the **Seurat** method implemented in Scanpy.

Parameters:

- Top genes: **2,000**
- `subset=False`

### Results

Selected highly variable genes:

- **2,000**

Representative highly variable genes included:

- ISG15
- TNFRSF4
- CPSF3L
- ATAD3C
- RER1

### Rationale

Highly variable genes capture biological heterogeneity more effectively than uniformly expressed genes.

Feature selection at this stage reduces computational complexity while preserving information relevant for downstream clustering and supervised learning.

Importantly, this step represents statistical feature selection rather than biological interpretation.

### Conclusion

The feature space was reduced from **13,692 genes** to **2,000 highly informative genes** for downstream analyses.

---

## 2.10 Feature Scaling

### Objective

Standardize gene expression values prior to principal component analysis.

### Method

Expression values were centered and scaled to unit variance using:

```python
sc.pp.scale(max_value=10)
```

Values exceeding ±10 standard deviations were clipped.

### Verification

- Matrix converted from sparse to dense.
- Mean ≈ 0
- Standard deviation ≈ 0.91
- Minimum = -10
- Maximum = 10

The slight reduction in standard deviation reflects clipping of extreme values.

### Rationale

Scaling ensures that highly expressed genes do not dominate PCA solely because of their magnitude.

### Conclusion

The dataset was successfully standardized for dimensionality reduction.

---

## 2.11 Principal Component Analysis

### Objective

Summarize the major sources of variation within the highly variable genes.

### Method

Principal component analysis was performed using the ARPACK SVD solver.

### Results

Generated:

- 50 principal components
- PCA embedding for all 2,633 cells
- Principal-component loading vectors for all 2,000 highly variable genes

The variance-ratio plot showed:

- PC1 explains the largest proportion of variance.
- Variance decreases rapidly across the first several principal components.
- An elbow appears approximately between PCs 8 and 10.
- Later components contribute progressively smaller amounts of variation.

### Rationale

PCA provides a compact representation of the dominant variation within the dataset and serves as the foundation for downstream visualization and neighborhood graph construction.

For this project, PCA is treated primarily as an exploratory analysis rather than the feature representation used for supervised classification.

### Conclusion

Principal component analysis successfully captured the major structure of the PBMC dataset while preserving gene-level features for future machine-learning models.

---

## 2.12 Processed Dataset

### Saved Outputs

The fully processed dataset was saved as:

```
data/processed/pbmc3k_preprocessed.h5ad
```

The saved object contains:

- 2,633 cells
- 2,000 highly variable genes
- Raw normalized expression matrix (`.raw`)
- Preserved filtered counts layer (`layers["counts"]`)
- PCA embeddings
- PCA loading vectors

The dataset was successfully reloaded to verify reproducibility.

---

## Phase 2 Decisions

- Preserve filtered raw counts before normalization.
- Preserve normalized full-gene expression in `.raw`.
- Select 2,000 highly variable genes using the Seurat method.
- Scale only the highly variable genes.
- Perform PCA for exploratory analysis and downstream visualization.
- Reserve gene-level expression matrices—not principal components—for final supervised machine-learning models to maximize biological interpretability.

---

## Phase 2 Summary

A complete preprocessing workflow was successfully developed for raw PBMC3K scRNA-seq data.

The workflow:

- Filters low-quality cells.
- Removes extremely sparse genes.
- Corrects sequencing-depth effects.
- Stabilizes expression variance.
- Identifies biologically informative genes.
- Standardizes expression values.
- Computes principal components.
- Produces a reproducible analysis-ready dataset suitable for downstream exploratory analysis and machine-learning experiments.

## Status

**Complete**

---

# Next Phase

## Phase 3 — Cell-Type Annotation and Dataset Preparation

### Planned Objectives

- Explore PCA structure.
- Construct neighborhood graphs.
- Generate UMAP visualizations.
- Perform clustering.
- Establish cell-type labels.
- Prepare machine-learning training datasets.

cluster 0 was supported as CD4-like T cells; cluster 2 was particularly important because the automated score favored FCGR3A monocytes, but the expression-validation plot supported CD14 monocytes; cluster 3 was labeled platelets based on the strong PPBP/PF4 signature.

## Final Cell-Type Annotations

Leiden clusters were annotated using a combination of:

- cluster-specific differential expression,
- comparison against canonical PBMC markers from CellMarker 3.0,
- normalized marker-overlap scoring,
- and validation using marker-expression dot plots.

Final annotations:

- Cluster 0 — CD4 T cells
- Cluster 1 — B cells
- Cluster 2 — CD14 Monocytes
- Cluster 3 — Platelets
- Cluster 4 — NK cells
- Cluster 5 — Dendritic cells

The marker-overlap scoring system was used as a candidate annotation method rather than as an automatic ground-truth classifier. Expression-level validation was used to resolve ambiguous cases, particularly the distinction between CD14 and FCGR3A monocytes.

---

## Notes for the Final Paper

The preprocessing methodology should be justified using both:

- Established scRNA-seq preprocessing literature.
- Empirical observations from the PBMC3K dataset.

This combination provides stronger methodological support than relying solely on conventional preprocessing defaults.