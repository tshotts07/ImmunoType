"""The saved tuned Logistic Regression reproduces the reported test metrics (05_machine_learning.ipynb cell 30)."""

import joblib
import pytest
from sklearn.metrics import accuracy_score, f1_score

from conftest import MODELS_DIR, require

# Reported in README.md and 05_machine_learning.ipynb cell 30
EXPECTED_ACCURACY = 520 / 527  # 0.9867
EXPECTED_MACRO_F1 = 0.9901660124043191
EXPECTED_WEIGHTED_F1 = 0.9867025373200148


@pytest.fixture(scope="module")
def tuned_logreg():
    return joblib.load(require(MODELS_DIR / "logreg_tuned_pipeline.pkl"))


def test_tuned_logreg_hyperparameters(tuned_logreg):
    classifier = tuned_logreg.named_steps["classifier"]
    assert classifier.C == 0.01
    assert classifier.class_weight == "balanced"


def test_tuned_logreg_reproduces_test_metrics(tuned_logreg, split):
    y_pred = tuned_logreg.predict(split["X_test"])
    assert (y_pred == split["y_test"]).sum() == 520
    assert accuracy_score(split["y_test"], y_pred) == pytest.approx(EXPECTED_ACCURACY, abs=1e-12)
    assert f1_score(split["y_test"], y_pred, average="macro") == pytest.approx(EXPECTED_MACRO_F1, abs=1e-12)
    assert f1_score(split["y_test"], y_pred, average="weighted") == pytest.approx(EXPECTED_WEIGHTED_F1, abs=1e-12)
