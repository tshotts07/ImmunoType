"""Download the raw PBMC3K dataset used by notebooks/03_preprocessing.ipynb.

Source: 10x Genomics "3k PBMCs from a Healthy Donor" (Chromium v1.1.0, hg19),
distributed as a single h5ad by scanpy via sc.datasets.pbmc3k().
Writes data/raw/pbmc3k/pbmc3k_raw.h5ad (2,700 cells x 32,738 genes).
"""

import hashlib
from pathlib import Path

import scanpy as sc

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "pbmc3k" / "pbmc3k_raw.h5ad"

# SHA-256 of the file the reported results were produced from
EXPECTED_SHA256 = "89a96f1beaa2dd83a687666d3f19a4513ac27a2a2d12581fcd77afed7ea653a1"


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not OUTPUT_PATH.exists():
        # scanpy downloads into settings.datasetdir under the name pbmc3k_raw.h5ad
        sc.settings.datasetdir = OUTPUT_PATH.parent
        adata = sc.datasets.pbmc3k()
        print(f"Downloaded: {adata.n_obs} cells x {adata.n_vars} genes")

    checksum = sha256(OUTPUT_PATH)
    if checksum != EXPECTED_SHA256:
        raise SystemExit(
            f"Checksum mismatch for {OUTPUT_PATH}\n"
            f"  expected {EXPECTED_SHA256}\n  got      {checksum}"
        )
    print(f"OK: {OUTPUT_PATH} (sha256 verified)")


if __name__ == "__main__":
    main()
