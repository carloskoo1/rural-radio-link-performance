# Beyond RSSI article extension

This branch preserves the frozen thesis release v1.0.0 and adds publication-oriented analyses for the manuscript **Beyond RSSI: Configuration-Dependent Performance and Temporal Stability in a Long-Distance Point-to-Point Wireless Link**.

## Scope

The article focuses on spectral configurations, RSSI DL, SNR DL, MCS DL, observed throughput DL, temporal stability, and multiscale robustness. ERA5-Land and NASA POWER are outside the article scope.

## Multiscale Temporal Robustness Analysis (MTRA)

MTRA is used as a sensitivity-analysis framework, not as a new statistical test. Telemetry is evaluated at fixed 15, 30, and 60 min aggregation scales using arithmetic means, followed by Kruskal-Wallis, epsilon-squared effect size, Dunn pairwise comparisons, and Holm adjustment.

The validated evidence table is stored in `outputs/article_tables/Table_MTRA_validated.csv`. Publication figures are generated in `outputs/article_figures/` by `scripts/article/generate_article_figures.js`.

E0 is excluded from observed-throughput comparisons because throughput is unavailable for that scenario. The four-dimensional composite stability index is therefore directly comparable only across E1-E5.
