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

### Scope Note

Early planning considered comparing multiple HVG counts (e.g., 1,000 and 3,000) before settling on a final value. In practice, 2,000 was fixed at this step and used unchanged through every downstream phase: clustering, all four ML models, and gene interpretation. The planned comparison was never run. This is a real scope reduction, not a value that was tested and selected, and should be described that way if the choice is questioned.

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
- Reserve gene-level expression matrices (not principal components) for final supervised machine-learning models to maximize biological interpretability.

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

## Phase 3 — Cell-Type Annotation and Dataset Preparation

### Objective

Establish cell-type labels for the preprocessed PBMC3K dataset via clustering and marker-based annotation, producing a training dataset for supervised classification.

### Activities

- Explored PCA structure from the Phase 2 checkpoint.
- Constructed a neighborhood graph and generated UMAP visualizations.
- Performed Leiden clustering.
- Compared cluster-specific differential expression against canonical PBMC markers from CellMarker 3.0 (`src/canonical_markers.py`), using normalized marker-overlap scoring (`src/cluster_annotation.py`: `compare_clusters_to_reference()` / `score_cluster_matches()`, core markers weighted 2x).
- Validated ambiguous scoring results against marker-expression dot plots.
- Assigned final cell-type labels and prepared the annotated dataset for machine-learning use.

### Findings

The marker-overlap score alone was not treated as sufficient to assign a label; it was used as a candidate ranking, then checked against expression-level evidence per cluster:

- **Cluster 0** — DE genes and marker-overlap scoring supported CD4-like T cell identity; no ambiguity.
- **Cluster 2** — the automated marker-overlap score favored FCGR3A monocytes, but the marker-expression dot plot showed the CD14 monocyte core markers more clearly expressed across the cluster. This was the one genuinely ambiguous case in the phase (CD14 vs. FCGR3A monocytes are transcriptionally similar and CellMarker 3.0's marker sets for the two overlap), and the dot-plot evidence was weighted over the scalar score.
- **Cluster 3** — a strong PPBP/PF4 signature unambiguously supported platelet identity.
- Clusters 1, 4, and 5 (B cells, NK cells, Dendritic cells) were supported consistently by both the marker-overlap score and DE genes, with no ambiguity requiring dot-plot resolution.

### Final Cell-Type Annotations

| Cluster | Cell type |
|---|---|
| 0 | CD4 T cells |
| 1 | B cells |
| 2 | CD14 Monocytes |
| 3 | Platelets |
| 4 | NK cells |
| 5 | Dendritic cells |

### Phase 3 Decisions

- Treat the marker-overlap scoring system as a candidate-ranking method, not an automatic ground-truth classifier; final assignment is a judgment call informed by the score plus DE genes plus dot-plot validation.
- For Cluster 2, assign CD14 Monocytes (not FCGR3A Monocytes, despite the higher automated score) based on marker-expression dot-plot validation.

### Rationale

A single scalar overlap score cannot distinguish two transcriptionally similar cell types whose canonical marker sets partially overlap, which is exactly what happened between CD14 and FCGR3A monocytes in Cluster 2; the score alone would have produced the wrong label. Requiring dot-plot validation whenever the score-based ranking is close catches this kind of case that a fully automated argmax over scores would miss, at the cost of the annotation step not being fully reproducible from the score alone. This caveat carries forward into Phase 4/5: the resulting six-class labels are derived (Leiden + DE + marker scoring + manual validation), not independent ground truth, and "accuracy" against them should be read as reproduction of these derived labels.

### Status

**Complete**

---

## Phase 4 - Model Training

### Split Design

Early planning called for a three-way 70/15/15 train/validation/test split. What was implemented instead was a single stratified 80/20 train/test split (2,106/527 cells), reused identically across all four models so the final comparison is apples-to-apples. Cross-validation on the training partition covers the validation role for Logistic Regression, Random Forest, and XGBoost. Only the PyTorch NN needed a separate, static validation set, and that was carved out of the training partition itself via a further 80/20 split (1,684/422 cells, see PyTorch Feedforward Neural Network below), not from a project-wide three-way split. The 527-cell held-out test set was touched exactly once per model, at the very end, matching this project's reproducibility convention that the held-out split is reserved for final evaluation only.

Model: Logistic Regression
Features: 2,000 HVGs
Training cells: 2,106
Held-out cells: 527
Classes: 6
Accuracy: 98.48%
Macro F1: 98.9%
Weighted F1: 98.5%

Logistic regression and XGBoost both achieved high classification performance on the PBMC3K held-out test set. Logistic regression performed slightly better overall, achieving 98.5% accuracy compared with 97.9% for XGBoost. Most errors from both models involved confusion between CD4 T cells and NK cells. Performance estimates for dendritic cells and especially platelets should be interpreted cautiously because these classes contained very few test samples.

The cross-validation results show that logistic regression performs consistently well across different subsets of the training data. The model averaged about 98% accuracy, suggesting that its strong performance was not caused by one lucky train/test split. Performance varied more for the rare cell types, which is expected because there are very few examples of those cells.

Original logistic regression had 98.48% accuracy and 0.989 macro F1. After tuning regularization to C=0.01, reached 98.67% accuracy and 0.990 macro F1. Small test-set improvement; the tuning was selected using cross-validation rather than the test set.

## PyTorch Environment Issue (Neural Network Setup)

While preparing tensors and DataLoaders for the PyTorch feedforward neural-network baseline, the kernel hung indefinitely on the first `torch.tensor()` call. No error or traceback was produced; the kernel process showed near-zero CPU activity.

The hang occurred specifically when this was the first PyTorch operation executed after the Logistic Regression, XGBoost, and Random Forest fits and their `n_jobs=-1` cross-validation/grid-search steps had already run earlier in the same session.

### Diagnosis

Checkpoint print statements isolated the hang to the tensor-conversion line itself rather than to the surrounding data (array shapes and dtypes were confirmed correct beforehand). `KMP_DUPLICATE_LIB_OK=TRUE`, the standard fix for duplicate-OpenMP-runtime conflicts, was tried first and did not resolve it, ruling that out as the cause.

The remaining explanation: PyTorch's CPU thread pool initializes lazily on first use. scikit-learn/XGBoost's `n_jobs=-1` calls use joblib's process-based backend, which forks worker processes. Initializing PyTorch's thread pool for the first time *after* that forking had already happened deadlocked instead of erroring.

### Fix

Added, immediately after `import torch` and before any `n_jobs=-1` fit or CV call:

```python
torch.set_num_threads(1)
_ = torch.zeros(1) + torch.zeros(1)  # forces thread-pool init while the process is still single-threaded
```

This forces PyTorch's thread pool to initialize while the process is still single-threaded, before joblib forks any workers.

### Verification

After the fix and a full kernel restart, tensor/dataset/DataLoader construction (1,684 training cells, 422 validation cells, batch size 64) completed immediately: 27 training batches, 7 validation batches, matching the expected split sizes exactly.

See `docs/developer_guide.md` (Troubleshooting → "PyTorch Hangs on First Tensor Op (macOS)") for the reusable fix.

## PyTorch Feedforward Neural Network

### Architecture

A feedforward network was trained on the same 2,000-HVG feature space (standardized) used by the other three models:

- Input: 2,000 features
- Hidden layers: 2,000 → 256 → 64, each with BatchNorm, ReLU, and dropout (p=0.4)
- Output: 6 classes (softmax via `CrossEntropyLoss`)
- Optimizer: Adam, lr=1e-3, weight_decay=1e-4
- Loss: `CrossEntropyLoss` weighted by inverse class frequency (`compute_class_weight("balanced")`), matching the `class_weight="balanced"` setting used for Logistic Regression and Random Forest, needed given the extreme class imbalance (Platelets: 7 training cells; Dendritic cells: 34)
- Batch size: 64
- Random seed: 42 (`torch.manual_seed(42)`)

### Deviation from the Originally Discussed Design

Early discussion had sketched a simpler, single-hidden-layer network (2,000 → 128 → 6). The two-hidden-layer 2,000 → 256 → 64 → 6 architecture actually implemented was a mid-implementation change, made before a review step rather than after one. It is defensible on the evidence rather than on assumption alone: BatchNorm, dropout (p=0.4), and early stopping together provided enough regularization that the added capacity did not overfit on only 1,684 training rows. Validation macro F1 (0.995) and test macro F1 (0.985) stayed close (see Results below), and that gap, not the architecture choice by itself, is the actual evidence against overfitting.

Output is raw logits, not `Linear → Softmax`. `CrossEntropyLoss` applies softmax internally, so stacking an explicit `Softmax` layer on top would double-apply it and distort the loss landscape. Early hand-written project notes had specified `Linear → Softmax` paired with `CrossEntropyLoss`; this was caught and corrected before implementation.

### Training/Validation Split

Following the reproducibility requirement that NN architecture and training decisions use only the train/validation split, not the held-out test set:

- NN training cells: 1,684
- Validation cells: 422
- Both splits were stratified on the encoded label and retained all six classes (minimum 5 Platelets in training, 2 in validation).

### Training

Early stopping on validation macro F1 (patience=15 epochs, max 100 epochs) stopped training at **epoch 29**, restoring the weights from the best epoch.

- Best validation macro F1: 0.995
- Validation accuracy at best epoch: 0.993

Validation-set classification report (used only to confirm the architecture, not as a final result):

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| B cells | 1.000 | 1.000 | 1.000 | 55 |
| CD14 Monocytes | 1.000 | 1.000 | 1.000 | 102 |
| CD4 T cells | 0.995 | 0.989 | 0.992 | 188 |
| Dendritic cells | 1.000 | 1.000 | 1.000 | 7 |
| NK cells | 0.971 | 0.985 | 0.978 | 68 |
| Platelets | 1.000 | 1.000 | 1.000 | 2 |

### Held-Out Test Set Result (Final, One-Time Evaluation)

| Metric | Value |
|---|---:|
| Accuracy | 97.91% |
| Macro F1 | 0.985 |
| Weighted F1 | 0.979 |

Per-class performance on the 527-cell held-out test set:

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| B cells | 0.971 | 1.000 | 0.986 | 68 |
| CD14 Monocytes | 1.000 | 1.000 | 1.000 | 128 |
| CD4 T cells | 0.983 | 0.970 | 0.976 | 235 |
| Dendritic cells | 1.000 | 1.000 | 1.000 | 9 |
| NK cells | 0.942 | 0.953 | 0.947 | 85 |
| Platelets | 1.000 | 1.000 | 1.000 | 2 |

### Four-Model Comparison (Held-Out Test Set)

| Model | Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|
| Logistic Regression | 98.48% | 0.989 | 0.985 |
| PyTorch Feedforward NN | 97.91% | 0.985 | 0.979 |
| XGBoost | 97.91% | 0.921 | 0.979 |
| Random Forest | 97.53% | 0.896 | 0.975 |

Logistic Regression remains the strongest model overall, but the class-weighted PyTorch NN was the closest competitor and clearly outperformed XGBoost and Random Forest on macro F1, the metric most sensitive to the rare classes (Dendritic cells, Platelets). This suggests the NN's weighted loss handled class imbalance more effectively than XGBoost/Random Forest's tree-based class weighting on this small, high-dimensional (2,000-feature), imbalanced dataset. As with the other models, Dendritic cells and Platelets have very few test-set examples (9 and 2, respectively), so their per-class metrics should be interpreted cautiously.

### Conclusion

Phase 4 is complete: all four models (Logistic Regression, XGBoost, Random Forest, PyTorch feedforward NN) have been trained, cross-validated where applicable, and evaluated once on the same held-out test set. Logistic Regression is the leading model on this feature space and dataset size, with the NN as a strong second. Next steps move to Phase 5 (gene-level interpretation via coefficients/feature importance and SHAP).

## Phase 5 — Gene-Level Interpretation

### Logistic Regression Coefficients

#### Method

The tuned Logistic Regression model (`C=0.01`, from GridSearchCV) was used to extract per-class coefficients via `coef_` (shape: 6 classes x 2,000 HVGs). Because features were standardized (StandardScaler) before fitting, coefficient magnitudes are directly comparable across genes without needing to account for differing expression scales. For each cell type, the 15 genes with the largest positive coefficient (i.e., most strongly pushing predictions toward that class) were extracted.

Models, encoders, and gene names were loaded from `models/` (saved at the end of `05_machine_learning.ipynb`) rather than rerun, in `06_gene_interpretation.ipynb`.

#### Top Genes by Cell Type

| Cell type | Top genes (by coefficient) |
|---|---|
| B cells | CD79A, MS4A1, CD79B, HLA-DQA1, HLA-DRA, LINC00926, HLA-DQB1, CD74 |
| CD14 Monocytes | FTL, LST1, S100A9, FCN1, FTH1, S100A8, AIF1, TYROBP |
| CD4 T cells | FYB, MAL, LTB, TPT1, IL32, JUNB, TNFRSF4, AQP3 |
| Dendritic cells | FCER1A, CLEC10A, SERPINF1, ENHO, BIRC5, CD1C, CLEC4C, ZWINT |
| NK cells | NKG7, GZMK, CCL5, CST7, GZMA, CTSW, KLRG1, LYAR |
| Platelets | LY6G6F, TREML1, ITGA2B, AP001189.4, GP9, GNG11, SDPR, RP11-879F14.2 |

Full top-15 lists are in `06_gene_interpretation.ipynb`.

#### Comparison Against CellMarker 3.0 Reference

Four of six classes are dominated by canonical markers already used in Phase 3 annotation: B cells (CD79A/CD79B/MS4A1), CD14 Monocytes (S100A8/S100A9/LST1, FCER1G/TYROBP), NK cells (NKG7, granzymes, PRF1, GNLY), and Platelets (ITGA2B, PF4, GP9, GNG11) all recover their expected canonical signatures near the top of the list.

**Dendritic cells:** FCER1A, CLEC10A, and CD1C are genuine conventional-DC markers, but CLEC4C is a plasmacytoid-DC-specific marker, and several other top genes (BIRC5, TOP2A, ZWINT, KIAA0101) are cell-cycle/proliferation markers rather than DC-identity genes. This may indicate the 43-cell Dendritic cells cluster from Phase 3 is a mixed cDC/pDC population that Leiden clustering did not separate, or may be an artifact of the very small training sample (~34 cells) for this class. Flagged as a limitation rather than resolved here. `src/canonical_markers.py` defines conventional and plasmacytoid dendritic cells as two separate reference panels (`Dendritic_cells`: FCER1A, CD1C, CLEC10A, CST3; `Plasmacytoid_Dendritic_cells`: CLEC4C, GZMB, JCHAIN, IL3RA, TCF4), so CLEC4C appearing alongside the conventional-DC markers here is consistent with the merged-cluster explanation specifically, not just plausible in general.

**CD4 T cells:** the weakest signature of the six. Coefficient magnitudes are noticeably smaller than other classes, and canonical CD3D/CD3E do not appear in the top 15 (IL7R and CD2 do). This is consistent with CD4 T cells being the largest and most heterogeneous class (1,175 cells) and with the four-model comparison's confusion matrices, where CD4 T cells were the dominant source of misclassification (confused primarily with NK cells) across all four models.

#### Conclusion

Logistic Regression coefficients largely recover the canonical PBMC marker panel used for Phase 3 annotation, providing independent evidence that the model is learning biologically meaningful signal rather than dataset artifacts. The Dendritic cell and CD4 T cell signatures are less clean, plausibly reflecting real subpopulation heterogeneity within those Phase 3 clusters rather than a model or annotation error. Next: Random Forest/XGBoost feature importance, for comparison against these coefficient-based results.

### Random Forest / XGBoost Feature Importance

#### Method

Global feature importance (`feature_importances_`) was extracted from the saved Random Forest and XGBoost models (`06_gene_interpretation.ipynb`, loaded from `models/`). Unlike the Logistic Regression coefficients, tree-based importance is a single score per gene reflecting overall usefulness for splitting decisions across the whole ensemble. It is not broken down by cell type. Top 20 genes by importance were extracted for each model.

#### Top Genes by Importance

| Random Forest | XGBoost |
|---|---|
| NKG7 | CD79A |
| HLA-DRB1 | FTL |
| FTL | HLA-DRA |
| CD79A | SERPINF1 |
| CD74 | NKG7 |
| HLA-DRA | HLA-DRB1 |
| HLA-DPB1 | CST3 |
| FTH1 | CLEC10A |
| GPX1 | CST7 |
| HLA-DPA1 | KIAA0101 |

Full top-20 lists for both models are in `06_gene_interpretation.ipynb`.

#### Cross-Model Consistency

CD79A and NKG7 rank at or near the top in all three interpretation methods tried so far (Logistic Regression coefficients, Random Forest importance, XGBoost importance): three structurally different algorithms (linear, bagged trees, boosted trees) independently converging on the same two genes as maximally decisive. Treated as strong evidence these two genes are genuinely central to distinguishing B cells and NK cells respectively, not an artifact of any one model.

#### Dendritic Cell Proliferation Signature — Reinforced

The proliferation-gene signature flagged in the Logistic Regression DC coefficients (BIRC5, TOP2A, ZWINT, KIAA0101) reappears independently in XGBoost's global importance list (KIAA0101, ZWINT, STMN1, SMC2, CKS1B), alongside genuine DC markers (SERPINF1, CLEC10A, FCER1A, ENHO). Two structurally unrelated models surfacing the same proliferation signature tied to the same 43-cell cluster raises this from a single-model coincidence to a candidate real finding. Not resolved here; flagged as follow-up work (e.g., checking MKI67/proliferation-marker expression specifically within the Dendritic cell cluster) rather than investigated further in this pass.

#### MHC-II Genes in Global Importance

Both models rank several MHC-II genes highly (HLA-DRA, HLA-DRB1, HLA-DPA1, HLA-DPB1, HLA-DQA1, HLA-DQB1, CD74). This reflects the global nature of tree importance: these genes are useful for distinguishing antigen-presenting cells (B cells, monocytes, dendritic cells) from non-APCs (T cells, NK cells, platelets) across many decision splits, rather than being specific to any single cell type the way NKG7 is specific to NK cells. Not a modeling error, expected behavior for a global (non-per-class) importance measure, and worth noting explicitly so it doesn't read as the model being confused.

#### Minor Note

Random Forest's list includes some broadly/ubiquitously expressed genes (MALAT1, OAZ1, GPX1) without clear cell-type-identity meaning, a known tendency of tree importance to reward genes with high, reliable expression variance generally, not just biologically specific markers.

#### Conclusion

Global feature importance from both tree-based models is broadly consistent with the Logistic Regression coefficient results and with each other, particularly for CD79A and NKG7. The Dendritic cell proliferation signal is now a two-model finding rather than a single-model curiosity. Next: SHAP analysis, to get per-class attribution from the tree models (and the NN) comparable to what Logistic Regression coefficients already provide directly.

### Random Forest SHAP Attribution

#### Method

`shap.TreeExplainer` (shap 0.52.0) was used to compute per-class SHAP values for the Random Forest model, in `06_gene_interpretation.ipynb`. A 300-cell background/foreground sample was drawn from the training set via a stratified `train_test_split` (`stratify=y_train_encoded, random_state=42`), so that the rare classes remained represented in proportion to their true training frequency (Dendritic cells: 5/300, Platelets: 1/300, directly reflecting how rare these classes are in the full training set: 34 and 7 cells respectively).

This step surfaced three distinct, non-obvious bugs, each documented here so they aren't repeated in the XGBoost/NN SHAP work that follows.

**Bug 1 — flat expected values from a missing background dataset.** The first `TreeExplainer` construction (`shap.TreeExplainer(rf_model)`, no `data=` argument) produced `expected_value` flat at ~0.1667 for all six classes, regardless of true class frequency. Root cause, confirmed by reading the shap source directly: with no background data, `feature_perturbation` defaults to `"tree_path_dependent"`, and `expected_value` is computed from the ensemble's internal root-node values — which are themselves computed under `class_weight="balanced"` (used to fit `rf_model`, matching Logistic Regression and Random Forest elsewhere in Phase 4). Balanced weighting is defined so every class's total weight is equal, so the weighted root-node proportion is exactly 1/6 for a 6-class problem, independent of real class counts. This is unrelated to `model_output`: for `RandomForestClassifier` specifically, `model_output="raw"` and `model_output="probability"` are numerically identical, since sklearn RF's native tree output is already probability-space (confirmed empirically and in source). Fixed by supplying a real background dataset (`data=X_sample`), which switches to `feature_perturbation="interventional"` and computes `expected_value` from actual predictions on that data.

**Bug 2 — silent, non-stratified re-subsampling of the background.** Passing `X_sample` (the stratified 300-cell set) directly as `data=` wraps it in `shap.maskers.Independent` with its *default* `max_samples=100`, which silently re-subsamples down to 100 cells via a plain non-stratified shuffle (`shap.utils.sample`, internally fixed `random_state=0`, independent of the notebook's own seed). Checked directly: this subsampling dropped Platelets from 1/300 to 0/100 and Dendritic cells from 5/300 to 2/100 in the actual background used, silently defeating the entire purpose of stratifying. Fixed by constructing the masker explicitly: `shap.maskers.Independent(X_sample, max_samples=300)`.

**Bug 3 — mean signed SHAP collapses to ~0 when foreground equals background.** After fixing 1 and 2, `expected_value` was correctly calibrated (see Results below), but averaging *signed* SHAP values across all 300 samples (mixed classes) produced per-gene means on the order of 1e-19 — floating-point noise, not signal. Per-sample SHAP additivity was verified to hold correctly (`expected_value + shap_values[i].sum() ≈ predict_proba(X_sample[i])` to ~1e-8), so the underlying computation was not broken, the issue is specific to averaging across the same population used as the background: since interventional SHAP values are deviations from the background's own expected value, and here foreground = background = the same mixed-class 300 cells, the mean deviation from the mean is zero by construction, independent of biology. Fixed by restricting the average to the subset of samples truly labeled as class *K* before averaging signed SHAP values for class *K*. That subset is not representative of the full background, so it does not cancel, and it preserves the same signed "genes pushing toward *K*" interpretation as the Logistic Regression coefficients (rather than switching to mean-|SHAP|, which would conflate genes that push toward a class with genes that push away from it).

#### Verification

Expected value by class vs. true frequency in the 300-cell sample, after fixing bugs 1 and 2:

| Class | Expected value | True frequency |
|---|---:|---:|
| B cells | 0.1411 | 0.1300 |
| CD14 Monocytes | 0.2382 | 0.2433 |
| CD4 T cells | 0.4072 | 0.4467 |
| Dendritic cells | 0.0242 | 0.0167 |
| NK cells | 0.1856 | 0.1600 |
| Platelets | 0.0037 | 0.0033 |

Tracks true frequencies closely, confirming the fix (previously flat at 0.1667 for every class).

#### Results — Top Genes by True-Label-Restricted Mean SHAP

| Cell type (n) | Top genes |
|---|---|
| B cells (n=39) | CD74, HLA-DRA, CD79A, HLA-DRB1, CD79B, HLA-DPB1, HLA-DPA1, HLA-DQA1, MS4A1 |
| CD14 Monocytes (n=73) | FTL, FTH1, TYROBP, CST3, LYZ, S100A9, LST1, AIF1, S100A8 |
| CD4 T cells (n=134) | NKG7, HLA-DRB1, HLA-DRA, CD74, HLA-DPB1, FTL, TYROBP, HLA-DPA1, CST3 |
| Dendritic cells (n=5) | HLA-DPA1, HLA-DQA1, FCER1A, HLA-DRA, CD74, HLA-DRB1, HLA-DPB1, CST3 |
| NK cells (n=48) | NKG7, CCL5, CST7, GZMA, CTSW, B2M, PRF1, GNLY, GZMK |
| Platelets (n=1) | TUBB1, GPX1, MPP1, PPBP, SDPR, GNG11, PF4, SPARC, NAP1L1 |

Full top-15 lists are in `06_gene_interpretation.ipynb`. **n is reported explicitly because it varies by two orders of magnitude across classes** (134 down to 1). Dendritic cells (n=5) and especially Platelets (n=1) should be read as illustrative, not as reliable per-gene rankings; a single cell's SHAP attribution is not an average of anything.

#### Comparison Against Prior Methods

B cells, CD14 Monocytes, and NK cells are consistent with both the Logistic Regression coefficients and the Random Forest/XGBoost global feature importance reported above (CD74/HLA-DRA/CD79A for B cells; FTL/FTH1/TYROBP for CD14 Monocytes; NKG7/CCL5/CST7/GZMA for NK cells).

**CD4 T cells** again shows the weakest, least cell-type-specific signature. As with the coefficients, no canonical CD4 marker appears at the top; instead NKG7 (an NK cell gene) and MHC-II genes dominate. This is now the third independent method (coefficients, RF/XGBoost global importance, and now RF SHAP) converging on the same finding: CD4 T cells lack a clean gene-level signature in this feature space, consistent with this being the largest, most heterogeneous class (1,175 cells) and the dominant source of cross-model misclassification (primarily with NK cells) noted in the Phase 4 four-model comparison.

This overlap is not just a modeling artifact. `src/canonical_markers.py`'s `CD8_T_cells` reference entry lists NKG7, CCL5, GZMH, and GZMK as supporting markers, the same genes that define the NK cell signature elsewhere in the same file. Because the current six-class scheme has no separate CD8 category (see Phase 3), a cytotoxic or NKT-like subpopulation within the coarse "CD4 T cells" Leiden cluster would be expected to carry these NK-shared markers by the reference's own definition. That reframes the finding: the model is very plausibly picking up a real, reference-documented marker overlap between two lymphocyte subtypes that this project's current cell-type taxonomy does not separate, rather than being confused.

**Platelets and Dendritic cells** are not treated as new findings here given n=1 and n=5. The genes surfaced (TUBB1/GPX1/PPBP/GNG11/PF4/SPARC for Platelets; HLA-DPA1/FCER1A/CD74 for Dendritic cells) are plausible and partially overlap with the coefficient-based results, but the sample sizes are too small to draw conclusions from independently.

#### Conclusion

Once correctly configured (real background data, explicit `max_samples` matching the intended stratified sample, and true-label-restricted averaging to avoid foreground/background cancellation), Random Forest SHAP attribution is consistent with the Logistic Regression coefficients and tree-based feature importance for the four well-supported classes (B cells, CD14 Monocytes, CD4 T cells, NK cells), and reinforces the CD4 T cell heterogeneity finding as a three-method signal rather than a single-model artifact. Next: XGBoost and PyTorch NN SHAP attribution, applying the same background/masker/true-label-restriction approach from the start.

## Notes for the Final Paper

The preprocessing methodology should be justified using both:

- Established scRNA-seq preprocessing literature.
- Empirical observations from the PBMC3K dataset.

This combination provides stronger methodological support than relying solely on conventional preprocessing defaults.