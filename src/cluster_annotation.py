def compare_clusters_to_reference(cluster_markers, canonical_markers):
    results = {}

    for cluster, genes in cluster_markers.items():
        cluster_genes = set(genes)
        results[cluster] = {}

        for cell_type, info in canonical_markers.items():
            core = set(info["core_markers"])
            supporting = set(info["supporting_markers"])

            core_matches = cluster_genes & core
            supporting_matches = cluster_genes & supporting

            results[cluster][cell_type] = {
                "core_matches": sorted(core_matches),
                "supporting_matches": sorted(supporting_matches),
                "core_count": len(core_matches),
                "supporting_count": len(supporting_matches),
            }
    return results

def score_cluster_matches(comparison_results, canonical_markers):
    scored_results = {}

    for cluster, cell_types in comparison_results.items():
        scored_results[cluster] = {}

        for cell_type, result in cell_types.items():
            core_count = result["core_count"]
            supporting_count = result["supporting_count"]

            n_core = len(
                canonical_markers[cell_type]["core_markers"]
            )
            n_supporting = len(
                canonical_markers[cell_type]["supporting_markers"]
            )

            weighted_score = (core_count * 2 + supporting_count)

            max_possible_score = (n_core * 2 + n_supporting)

            normalized_score = (
                weighted_score / max_possible_score
                if max_possible_score > 0
                else 0
            )

            scored_results[cluster][cell_type] = {
                **result,
                "weighted_score": weighted_score,
                "normalized_score": normalized_score,
            }

    return scored_results