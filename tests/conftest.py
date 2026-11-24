"""Shared fixtures: load the pipeline's data files and rebuild the nb05 split.

The data, checkpoints, and models are gitignored, so these tests need
./reproduce.sh (or the notebooks) to have been run first; otherwise they skip.
"""

from pathlib import Path

import numpy as np
import pytest
import scanpy as sc
from scipy import sparse
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "pbmc3k" / "pbmc3k_raw.h5ad"
ANNOTATED_PATH = PROJECT_ROOT / "data" / "processed" / "pbmc3k_clustered_annotated.h5ad"
MODELS_DIR = PROJECT_ROOT / "models"


def require(path):
    if not path.exists():
        pytest.skip(f"{path.relative_to(PROJECT_ROOT)} not found; run ./reproduce.sh first")
    return path


@pytest.fixture(scope="session")
def raw_adata():
    return sc.read_h5ad(require(RAW_PATH))


@pytest.fixture(scope="session")
def annotated_adata():
    return sc.read_h5ad(require(ANNOTATED_PATH))


@pytest.fixture(scope="session")
def split(annotated_adata):
    """The train/test split exactly as built in 05_machine_learning.ipynb."""
    adata = annotated_adata
    hvg_mask = adata.raw.var_names.isin(
        adata.var_names[adata.var["highly_variable"]]
    )
    X_hvg = adata.raw.X[:, hvg_mask]
    if sparse.issparse(X_hvg):
        X_hvg = X_hvg.toarray()
    y = adata.obs["cell_type"].astype(str).to_numpy()

    indices = np.arange(adata.n_obs)
    X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
        X_hvg, y, indices,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )
    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "idx_train": idx_train,
        "idx_test": idx_test,
        "y": y,
    }
