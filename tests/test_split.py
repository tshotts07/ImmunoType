"""The train/test split is stratified with the expected sizes (05_machine_learning.ipynb cell 5)."""

import numpy as np
import pandas as pd

from conftest import MODELS_DIR, require

N_TRAIN, N_TEST = 2106, 527

# Per-class counts printed by 05_machine_learning.ipynb cell 5
TRAIN_COUNTS = {
    "CD4 T cells": 940,
    "CD14 Monocytes": 511,
    "NK cells": 340,
    "B cells": 274,
    "Dendritic cells": 34,
    "Platelets": 7,
}
TEST_COUNTS = {
    "CD4 T cells": 235,
    "CD14 Monocytes": 128,
    "NK cells": 85,
    "B cells": 68,
    "Dendritic cells": 9,
    "Platelets": 2,
}


def test_split_sizes(split):
    assert split["X_train"].shape == (N_TRAIN, 2000)
    assert split["X_test"].shape == (N_TEST, 2000)


def test_split_is_disjoint_and_complete(split):
    train, test = set(split["idx_train"]), set(split["idx_test"])
    assert not train & test
    assert len(train | test) == N_TRAIN + N_TEST


def test_split_class_counts(split):
    assert pd.Series(split["y_train"]).value_counts().to_dict() == TRAIN_COUNTS
    assert pd.Series(split["y_test"]).value_counts().to_dict() == TEST_COUNTS


def test_split_is_stratified(split):
    # Every class, including the rare ones, lands within one cell of a 20% test share
    totals = pd.Series(split["y"]).value_counts()
    test_counts = pd.Series(split["y_test"]).value_counts()
    for cell_type, total in totals.items():
        assert test_counts.get(cell_type, 0) >= 1, cell_type
        assert abs(test_counts[cell_type] - 0.2 * total) <= 1, cell_type


def test_split_matches_saved_training_array(split):
    # Ties this rebuilt split to the one nb05 actually trained on
    saved = np.load(require(MODELS_DIR / "X_train_unscaled.npy"))
    np.testing.assert_array_equal(split["X_train"], saved)
