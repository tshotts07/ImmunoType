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

## Phase 4 - Model Training
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

Original logistic regression had 98.48% accuracy and 0.989 macro F1. After tuning regularization to C=0.01, reached 98.67% accuracy and 0.990 macro F1. Small test-set improvement,g the tuning was selected using cross-validation rather than the test set.

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
- Loss: `CrossEntropyLoss` weighted by inverse class frequency (`compute_class_weight("balanced")`), matching the `class_weight="balanced"` setting used for Logistic Regression and Random Forest — needed given the extreme class imbalance (Platelets: 7 training cells; Dendritic cells: 34)
- Batch size: 64
- Random seed: 42 (`torch.manual_seed(42)`)

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

Logistic Regression remains the strongest model overall, but the class-weighted PyTorch NN was the closest competitor and clearly outperformed XGBoost and Random Forest on macro F1 — the metric most sensitive to the rare classes (Dendritic cells, Platelets). This suggests the NN's weighted loss handled class imbalance more effectively than XGBoost/Random Forest's tree-based class weighting on this small, high-dimensional (2,000-feature), imbalanced dataset. As with the other models, Dendritic cells and Platelets have very few test-set examples (9 and 2, respectively), so their per-class metrics should be interpreted cautiously.

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

**Dendritic cells:** FCER1A, CLEC10A, and CD1C are genuine conventional-DC markers, but CLEC4C is a plasmacytoid-DC-specific marker, and several other top genes (BIRC5, TOP2A, ZWINT, KIAA0101) are cell-cycle/proliferation markers rather than DC-identity genes. This may indicate the 43-cell Dendritic cells cluster from Phase 3 is a mixed cDC/pDC population that Leiden clustering did not separate, or may be an artifact of the very small training sample (~34 cells) for this class. Flagged as a limitation rather than resolved here.

**CD4 T cells:** the weakest signature of the six — coefficient magnitudes are noticeably smaller than other classes, and canonical CD3D/CD3E do not appear in the top 15 (IL7R and CD2 do). This is consistent with CD4 T cells being the largest and most heterogeneous class (1,175 cells) and with the four-model comparison's confusion matrices, where CD4 T cells were the dominant source of misclassification (confused primarily with NK cells) across all four models.

#### Conclusion

Logistic Regression coefficients largely recover the canonical PBMC marker panel used for Phase 3 annotation, providing independent evidence that the model is learning biologically meaningful signal rather than dataset artifacts. The Dendritic cell and CD4 T cell signatures are less clean, plausibly reflecting real subpopulation heterogeneity within those Phase 3 clusters rather than a model or annotation error. Next: Random Forest/XGBoost feature importance, for comparison against these coefficient-based results.

### Random Forest / XGBoost Feature Importance

#### Method

Global feature importance (`feature_importances_`) was extracted from the saved Random Forest and XGBoost models (`06_gene_interpretation.ipynb`, loaded from `models/`). Unlike the Logistic Regression coefficients, tree-based importance is a single score per gene reflecting overall usefulness for splitting decisions across the whole ensemble — it is not broken down by cell type. Top 20 genes by importance were extracted for each model.

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

CD79A and NKG7 rank at or near the top in all three interpretation methods tried so far (Logistic Regression coefficients, Random Forest importance, XGBoost importance) — three structurally different algorithms (linear, bagged trees, boosted trees) independently converging on the same two genes as maximally decisive. Treated as strong evidence these two genes are genuinely central to distinguishing B cells and NK cells respectively, not an artifact of any one model.

#### Dendritic Cell Proliferation Signature — Reinforced

The proliferation-gene signature flagged in the Logistic Regression DC coefficients (BIRC5, TOP2A, ZWINT, KIAA0101) reappears independently in XGBoost's global importance list (KIAA0101, ZWINT, STMN1, SMC2, CKS1B), alongside genuine DC markers (SERPINF1, CLEC10A, FCER1A, ENHO). Two structurally unrelated models surfacing the same proliferation signature tied to the same 43-cell cluster raises this from a single-model coincidence to a candidate real finding. Not resolved here — flagged as follow-up work (e.g., checking MKI67/proliferation-marker expression specifically within the Dendritic cell cluster) rather than investigated further in this pass.

#### MHC-II Genes in Global Importance

Both models rank several MHC-II genes highly (HLA-DRA, HLA-DRB1, HLA-DPA1, HLA-DPB1, HLA-DQA1, HLA-DQB1, CD74). This reflects the global nature of tree importance: these genes are useful for distinguishing antigen-presenting cells (B cells, monocytes, dendritic cells) from non-APCs (T cells, NK cells, platelets) across many decision splits, rather than being specific to any single cell type the way NKG7 is specific to NK cells. Not a modeling error — expected behavior for a global (non-per-class) importance measure, and worth noting explicitly so it doesn't read as the model being confused.

#### Minor Note

Random Forest's list includes some broadly/ubiquitously expressed genes (MALAT1, OAZ1, GPX1) without clear cell-type-identity meaning — a known tendency of tree importance to reward genes with high, reliable expression variance generally, not just biologically specific markers.

#### Conclusion

Global feature importance from both tree-based models is broadly consistent with the Logistic Regression coefficient results and with each other, particularly for CD79A and NKG7. The Dendritic cell proliferation signal is now a two-model finding rather than a single-model curiosity. Next: SHAP analysis, to get per-class attribution from the tree models (and the NN) comparable to what Logistic Regression coefficients already provide directly.

## Notes for the Final Paper

The preprocessing methodology should be justified using both:

- Established scRNA-seq preprocessing literature.
- Empirical observations from the PBMC3K dataset.

This combination provides stronger methodological support than relying solely on conventional preprocessing defaults.