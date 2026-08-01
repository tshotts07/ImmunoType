"""
Canonical marker genes for PBMCs.

Markers are compiled from CellMarker 3.0.

These marker sets are intended to assist annotation of Leiden clusters
and should be interpreted alongside differential expression analysis,
dot plots, and UMAP visualization.
"""

canonical_markers = {
    "T_cells": {
        "core_markers": [
            "CD3D",
            "CD3E",
            "CD3G",
            "TRAC"
        ],
        "supporting_markers": [
            "CCR7",
            "IL7R",
            "LEF1",
            "TCF7",
            "LTB",
            "GZMK"
        ],
        "source": "CellMarker 3.0",
        "notes": "Human, Blood, Peripheral blood, Normal",
        "accessed": "2026-08-01",
        "evidence": "Single-cell sequencing with experimental confirmation where available"
    },

    "CD4_T_cells": {
        "core_markers": [
            "CD4",
            "IL7R",
            "CCR7",
            "LEF1",
            "TCF7",
            "CD40LG"
        ],
        "supporting_markers": [
            "CD3D",
            "CD3E",
            "GATA3"
        ],
        "source": "CellMarker 3.0",
        "notes": "Human, Blood, Peripheral blood, Normal",
        "accessed": "2026-08-01",
        "evidence": "Single-cell sequencing with experimental confirmation where available"
    },

    "CD8_T_cells": {
        "core_markers": [
            "CD8A",
            "CD8B"
        ],
        "supporting_markers": [
            "CD3D",
            "CD3E",
            "GZMK",
            "CCL5",
            "GZMH",
            "NKG7"
        ],
        "source": "CellMarker 3.0",
        "notes": "Human, Blood, Peripheral blood, Normal",
        "accessed": "2026-08-01",
        "evidence": "Single-cell sequencing with experimental confirmation where available"
    },

    "Regulatory_T_cells": {
        "core_markers": [
            "FOXP3",
            "IL2RA",
            "CTLA4",
            "TIGIT",
            "IKZF2"
        ],
        "supporting_markers": [
            "CD4",
            "CCR4",
            "RTKN2",
            "CD3D",
            "CD3E"
        ],
        "source": "CellMarker 3.0",
        "notes": "Human, Blood, Peripheral blood, Normal",
        "accessed": "2026-08-01",
        "evidence": "Single-cell sequencing with experimental confirmation where available"
    },

    "B_cells": {
        "core_markers": [
            "CD19",
            "MS4A1",
            "CD79A",
            "CD79B",
            "PAX5",
            "CD22"
        ],
        "supporting_markers": [
            "BANK1",
            "FCRLA",
            "IGHM",
            "LINC00926"
        ],
        "source": "CellMarker 3.0",
        "notes": "Human, Blood, Peripheral blood, Normal",
        "accessed": "2026-08-01",
        "evidence": "Single-cell sequencing with experimental confirmation where available"
    },

    "Plasma_cells": {
        "core_markers": [
            "MZB1",
            "JCHAIN",
            "TNFRSF17",
            "SDC1",
            "CD38",
            "DERL3"
        ],
        "supporting_markers": [
            "TXNDC5",
            "IGHA1",
            "PARM1",
            "IGF1"
        ],
        "source": "CellMarker 3.0",
        "notes": "Human, Blood, Peripheral blood, Normal",
        "accessed": "2026-08-01",
        "evidence": "Single-cell sequencing with experimental confirmation where available"
    },

    "NK_cells": {
        "core_markers": [
            "NKG7",
            "GNLY",
            "KLRD1",
            "PRF1",
            "NCAM1"
        ],
        "supporting_markers": [
            "CCL5",
            "GZMB",
            "GZMH",
            "GZMK",
            "FCGR3A",
            "TYROBP",
            "PTGDS"
        ],
        "source": "CellMarker 3.0",
        "notes": "Human, Blood, Peripheral blood, Normal",
        "accessed": "2026-08-01",
        "evidence": "Single-cell sequencing with experimental confirmation where available"
    },

    "CD14_Monocytes": {
        "core_markers": [
            "CD14",
            "LYZ",
            "S100A8",
            "S100A9",
            "FCN1"
        ],
        "supporting_markers": [
            "VCAN",
            "CLEC4D",
            "TNFAIP2",
            "CCR2"
        ],
        "source": "CellMarker 3.0",
        "notes": "Human, Blood, Peripheral blood, Normal",
        "accessed": "2026-08-01",
        "evidence": "Single-cell sequencing with experimental confirmation where available"
    },

    "FCGR3A_Monocytes": {
        "core_markers": [
            "FCGR3A",
            "LST1",
            "MS4A7",
            "AIF1"
        ],
        "supporting_markers": [
            "LGALS3",
            "IFITM3",
            "SAT1",
            "TYMP",
            "FCER1G"
        ],
        "source": "CellMarker 3.0",
        "notes": "Human, Blood, Peripheral blood, Normal",
        "accessed": "2026-08-01",
        "evidence": "Single-cell sequencing with experimental confirmation where available"
    },

    "Dendritic_cells": {
        "core_markers": [],
        "supporting_markers": [],
        "source": "CellMarker 3.0",
        "notes": "Human, Blood, Peripheral blood, Normal",
        "accessed": "2026-08-01",
        "evidence": "Single-cell sequencing with experimental confirmation where available"
    },

    "Plasmacytoid_Dendritic_cells": {
        "core_markers": [],
        "supporting_markers": [],
        "source": "CellMarker 3.0",
        "notes": "Human, Blood, Peripheral blood, Normal"
    },

    "Platelets": {
        "core_markers": [],
        "supporting_markers": [],
        "source": "CellMarker 3.0",
        "notes": "Human, Blood, Peripheral blood, Normal"
    },

    "Megakaryocytes": {
        "core_markers": [],
        "supporting_markers": [],
        "source": "CellMarker 3.0",
        "notes": "Human, Blood, Peripheral blood, Normal"
    },

    "Hematopoietic_Stem_Progenitor_Cells": {
        "core_markers": [],
        "supporting_markers": [],
        "source": "CellMarker 3.0",
        "notes": "Human, Blood, Peripheral blood, Normal"
    },

    "Erythrocytes": {
        "core_markers": [],
        "supporting_markers": [],
        "source": "CellMarker 3.0",
        "notes": "Human, Blood, Peripheral blood, Normal"
    }
}