"""QC keeps the expected cell and gene counts (03_preprocessing.ipynb cells 11 to 17)."""

import scanpy as sc

# Expected counts as reported in 03_preprocessing.ipynb and docs/research_log.md
RAW_CELLS, RAW_GENES = 2700, 32738
QC_CELLS = 2633
QC_GENES = 13692
N_HVG = 2000


def run_qc(adata):
    """Same thresholds as 03_preprocessing.ipynb: >=300 genes, <5% mitochondrial, genes in >=3 cells."""
    adata = adata.copy()
    adata.var["mt"] = adata.var_names.str.startswith("MT-")
    sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True)
    adata = adata[
        (adata.obs["n_genes_by_counts"] >= 300)
        & (adata.obs["pct_counts_mt"] < 5)
    ].copy()
    sc.pp.filter_genes(adata, min_cells=3)
    return adata


def test_raw_data_dimensions(raw_adata):
    assert raw_adata.shape == (RAW_CELLS, RAW_GENES)


def test_qc_keeps_expected_cells_and_genes(raw_adata):
    adata_qc = run_qc(raw_adata)
    assert adata_qc.n_obs == QC_CELLS
    assert adata_qc.n_vars == QC_GENES


def test_annotated_checkpoint_matches_qc(raw_adata, annotated_adata):
    adata_qc = run_qc(raw_adata)
    assert annotated_adata.n_obs == QC_CELLS
    assert list(annotated_adata.obs_names) == list(adata_qc.obs_names)
    # adata.raw holds the full post-QC gene set; X holds the HVGs used as ML features
    assert annotated_adata.raw.n_vars == QC_GENES
    assert annotated_adata.n_vars == N_HVG
    assert annotated_adata.var["highly_variable"].sum() == N_HVG


def test_annotated_checkpoint_class_counts(annotated_adata):
    counts = annotated_adata.obs["cell_type"].astype(str).value_counts().to_dict()
    assert counts == {
        "CD4 T cells": 1175,
        "CD14 Monocytes": 639,
        "NK cells": 425,
        "B cells": 342,
        "Dendritic cells": 43,
        "Platelets": 9,
    }
