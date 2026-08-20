# ImmunoType

**ImmunoType** is a computational immunology research project
investigating whether machine-learning models can accurately classify
peripheral blood mononuclear cell (PBMC) immune cell types from
single-cell RNA sequencing (scRNA-seq) data and identify the genes that
contribute most strongly to those predictions.

## Core Research Question

> Can machine learning accurately classify PBMC immune cell types from
> scRNA-seq data, and which genes contribute most to model predictions?

## Project Goals

-   Build a transparent and reproducible scRNA-seq preprocessing and
    annotation workflow.
-   Compare Logistic Regression, Random Forest, XGBoost, and a PyTorch
    feedforward neural network for PBMC immune-cell classification.
-   Evaluate performance with held-out testing, stratified
    cross-validation, confusion matrices, macro F1, weighted F1, and
    accuracy.
-   Identify genes that drive predictions using model coefficients,
    feature importance, and SHAP-based interpretation.
-   Validate the final approach on an independently annotated PBMC
    dataset.

## Current Status

**Phases 0-4 are complete. Phase 5 - Gene-Level Interpretation - is up
next.**

### Completed

-   Repository/environment and reproducible research workflow
-   PBMC dataset exploration
-   PBMC3K quality control and preprocessing
-   Highly variable gene selection and dimensionality reduction
-   Leiden clustering and differential-expression analysis
-   CellMarker 3.0-based canonical marker reference
-   Cluster-to-reference marker scoring
-   Biological validation with marker-expression dot plots
-   Final PBMC3K cell-type annotations
-   Logistic Regression, XGBoost, and Random Forest baselines
-   Five-fold stratified cross-validation for all three baseline models
-   Logistic Regression hyperparameter tuning with training-only
    GridSearchCV
-   PyTorch feedforward neural-network baseline (class-weighted loss,
    early stopping on validation macro F1)
-   Four-model comparison (Logistic Regression, XGBoost, Random Forest,
    PyTorch NN) on the held-out test set

### Planned

-   Gene-level interpretation
-   SHAP analysis
-   Independent external PBMC validation
-   Final figures, tables, research synthesis, and manuscript-ready
    documentation

## Phase Roadmap

  ----------------------------------------------------------------------------
  Phase             Name              Status            Description
  ----------------- ----------------- ----------------- ----------------------
  0                 Preparation       Complete          Repository,
                                                        environment, project
                                                        structure,
                                                        reproducibility, and
                                                        research workflow.

  1                 Dataset           Complete          Evaluate PBMC3K and
                    Exploration                         PBMC68K Reduced for
                                                        preprocessing,
                                                        classification, and
                                                        interpretation.

  2                 Preprocessing     Complete          QC, filtering,
                                                        normalization, log
                                                        transformation, HVGs,
                                                        scaling/PCA decisions,
                                                        and processed AnnData
                                                        checkpoints.

  3                 Cell-Type         Complete          Leiden clustering, DE
                    Annotation                          genes, CellMarker 3.0
                                                        reference comparison,
                                                        scoring, validation,
                                                        and final labels.

  4                 Supervised        Complete          Compare Logistic
                    Machine Learning                    Regression, Random
                                                        Forest, XGBoost, and
                                                        PyTorch on a common
                                                        PBMC3K feature space.

  5                 Gene-Level        Planned           Interpret
                    Interpretation                      coefficients/feature
                                                        importance and use
                                                        SHAP to identify
                                                        biologically
                                                        meaningful predictive
                                                        genes.

  6                 External          Planned           Test on independently
                    Validation and                      annotated PBMC data
                    Final Synthesis                     and consolidate final
                                                        conclusions and
                                                        deliverables.
  ----------------------------------------------------------------------------

## Data and Annotation

The current supervised proof-of-concept dataset is the annotated PBMC3K
object:

-   **Cells:** 2,633
-   **ML features:** 2,000 highly variable genes
-   **Cell types:** 6

  Cell type           Cells
  ----------------- -------
  CD4 T cells         1,175
  CD14 Monocytes        639
  NK cells              425
  B cells               342
  Dendritic cells        43
  Platelets               9

Final Phase 3 cluster annotations:

``` python
cluster_annotations = {
    "0": "CD4 T cells",
    "1": "B cells",
    "2": "CD14 Monocytes",
    "3": "Platelets",
    "4": "NK cells",
    "5": "Dendritic cells",
}
```

The annotated AnnData checkpoint is:

``` text
data/processed/pbmc3k_clustered_annotated.h5ad
```

## Machine-Learning Results So Far

### Held-Out Test Set

The stratified split contains **2,106 training cells** and **527
held-out test cells**.

  Model                   Accuracy   Macro F1   Weighted F1
  --------------------- ---------- ---------- -------------
  Logistic Regression       0.9848     0.9888        0.9848
  PyTorch Feedforward NN    0.9791     0.9849        0.9791
  XGBoost                   0.9791     0.9205        0.9788
  Random Forest             0.9753     0.8964        0.9745

### Five-Fold Cross-Validation on Training Data

  Model                   Mean Accuracy   Mean Macro F1   Mean Weighted F1
  --------------------- --------------- --------------- ------------------
  Logistic Regression            0.9796          0.9433             0.9798
  XGBoost                        0.9744          0.9299             0.9739
  Random Forest                  0.9763          0.9278             0.9752

### Tuned Logistic Regression

GridSearchCV optimized **macro F1** over regularization strength using
training-only cross-validation.

-   **Best `C`:** `0.01`
-   **Best CV macro F1:** approximately `0.9748`
-   **Final held-out accuracy:** `0.9867`
-   **Final held-out macro F1:** `0.9902`
-   **Final held-out weighted F1:** `0.9867`

Logistic Regression is the strongest model overall, with the PyTorch
neural network as the closest competitor — see below for the completed
four-model comparison.

## Neural-Network Work

The original training portion was split into:

-   **NN training:** 1,684 cells x 2,000 genes
-   **Validation:** 422 cells x 2,000 genes
-   **Held-out test:** 527 cells x 2,000 genes

### Architecture

A feedforward network was trained on the same 2,000-HVG standardized
feature space used by the other three models:

-   **Input:** 2,000 features
-   **Hidden layers:** 2,000 → 256 → 64, each with BatchNorm, ReLU, and
    dropout (p=0.4)
-   **Output:** 6 classes (`CrossEntropyLoss`, i.e. softmax)
-   **Optimizer:** Adam, lr=1e-3, weight_decay=1e-4
-   **Loss weighting:** inverse class frequency
    (`compute_class_weight("balanced")`), matching the
    `class_weight="balanced"` setting used for Logistic Regression and
    Random Forest — required given the severe class imbalance (7
    Platelets and 34 Dendritic cells in the training set)
-   **Batch size:** 64
-   **Random seed:** 42

Architecture and training decisions used only the training/validation
split; the 527-cell held-out test set was evaluated once, at the end.

### Results

Early stopping on validation macro F1 (patience=15, max 100 epochs)
stopped training at **epoch 29**, restoring the best-epoch weights.

-   **Best validation macro F1:** 0.995
-   **Held-out test accuracy:** 97.91%
-   **Held-out test macro F1:** 0.985
-   **Held-out test weighted F1:** 0.979

The class-weighted PyTorch NN outperformed XGBoost and Random Forest on
macro F1 — the metric most sensitive to the rare classes — suggesting its
weighted loss handled class imbalance more effectively than the
tree-based models' class weighting on this small, high-dimensional,
imbalanced dataset. Full per-class metrics and the training/validation
curves are in `docs/research_log.md`.

## Canonical Marker Annotation

Canonical PBMC marker panels were compiled from **CellMarker 3.0** and
organized into core and supporting markers. Cluster-specific
differential-expression genes were compared against these marker sets to
generate candidate annotations.

Candidate scores were treated as evidence rather than automatic ground
truth. Marker-expression dot plots were used to resolve ambiguous cases,
including the CD14 vs. FCGR3A monocyte distinction.

## Important Limitations

-   PBMC3K does not provide authoritative cell-level labels for the
    final six classes used here. The Phase 3 labels were derived from
    Leiden clusters, differential expression, canonical markers, and
    biological validation.
-   Internal PBMC3K classification performance therefore measures the
    ability to reproduce these derived labels from the same broad
    expression domain.
-   Platelets and dendritic cells are rare, so per-class performance
    estimates are unstable.
-   Strong claims of generalization require an independently annotated
    external PBMC dataset.
-   Feature harmonization and equivalent preprocessing will be required
    before external testing.

## Planned Interpretation

After completing the four-model comparison:

1.  Inspect Logistic Regression coefficients by cell type.
2.  Inspect Random Forest/XGBoost feature importance.
3.  Apply SHAP where appropriate.
4.  Compare high-importance genes with the CellMarker 3.0 canonical
    marker reference.
5.  Investigate predictive genes that are not obvious canonical markers.
6.  Test whether the learned signatures transfer to an independent
    dataset.

## Initial Literature

The following articles were supplied at the beginning of the project:

1.  **Robust and interpretable prediction of gene markers and cell types
    from spatial transcriptomics data** - Nature Communications (2026)\
    https://www.nature.com/articles/s41467-026-68487-0

2.  **Cell Reports Methods article, PII S2667-2375(23)00314-4**\
    https://www.cell.com/cell-reports-methods/fulltext/S2667-2375(23)00314-4#fig1

3.  **xCell 2.0: robust algorithm for cell type proportion estimation
    predicts response to immune checkpoint blockade** - Genome Biology
    (2025)\
    https://pmc.ncbi.nlm.nih.gov/articles/PMC12492622/

## Technology

-   Python
-   Scanpy / AnnData
-   NumPy / Pandas / SciPy
-   scikit-learn
-   XGBoost
-   PyTorch
-   SHAP
-   Matplotlib
-   Git / GitHub
-   JupyterLab

## Reproducibility Principles

The project aims to record:

-   dataset/version used
-   cells and genes before/after major processing steps
-   exact preprocessing/model parameters
-   random seeds
-   software versions
-   output artifact paths
-   scientific rationale for major decisions
-   Git commits associated with milestones

## Current Next Step

Begin **Phase 5 — Gene-Level Interpretation**: identify which genes drive
model predictions using Logistic Regression coefficients, tree-based
feature importance (XGBoost/Random Forest), and SHAP attribution, then
compare those signals against the canonical PBMC marker panels used for
cluster annotation.
