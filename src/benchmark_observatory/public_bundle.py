"""Shape of the lazily loaded public benchmark detail records."""

# Fields kept in the canonical validation snapshot (site/data/benchmarks.json)
# but omitted from the public per-benchmark detail files. `frontier` and
# `frontier_events` are copies of `capability_frontier`, `historical_frontier`
# is a copy of `reported_frontier`, and `retrospective_observations` is a
# subset of `observations` flagged by `retrospective`. The frontend never reads
# them, so publishing them only inflates every detail download.
PUBLIC_DETAIL_OMITTED_FIELDS = (
    "frontier",
    "frontier_events",
    "historical_frontier",
    "retrospective_observations",
)


def public_detail_benchmark(benchmark):
    """Return the benchmark record exactly as published in its detail file."""
    return {key: value for key, value in benchmark.items() if key not in PUBLIC_DETAIL_OMITTED_FIELDS}
