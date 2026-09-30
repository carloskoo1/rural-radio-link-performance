# Article evidence matrix — Beyond RSSI

## Purpose

This matrix is the control document for drafting the manuscript. Every quantitative claim in the article should be traceable to a versioned table, figure, or documented analysis.

## Core experimental configurations

| Scenario | Frequency | Channel |
|---|---:|---:|
| E0 | 5800 MHz | 20 MHz |
| E1 | 5660 MHz | 40 MHz |
| E2 | 5660 MHz | 80 MHz |
| E3 | 5730 MHz | 40 MHz |
| E4 | 5730 MHz | 80 MHz |
| E5 | 5805 MHz | 40 MHz |

## Descriptive evidence

| Metric | E0 | E1 | E2 | E3 | E4 | E5 |
|---|---:|---:|---:|---:|---:|---:|
| RSSI mean (dBm) | -76.231 | -76.668 | -74.396 | -76.356 | -75.694 | -75.626 |
| RSSI SD (dB) | 1.111 | 1.092 | 0.910 | 0.811 | 0.673 | 1.043 |
| SNR mean (dB) | 20.596 | 21.115 | 21.678 | 19.936 | 20.616 | 21.136 |
| SNR SD (dB) | 0.895 | 0.980 | 0.853 | 0.424 | 1.047 | 0.841 |
| MCS mean | 104.995 | 104.746 | 103.300 | 104.644 | 103.672 | 104.976 |
| MCS SD | 1.930 | 0.948 | 1.805 | 0.690 | 1.223 | 0.645 |
| Throughput mean (Mb/s) | — | 0.601 | 0.588 | 0.770 | 0.791 | 0.743 |
| Throughput SD (Mb/s) | — | 0.377 | 0.375 | 0.383 | 0.428 | 0.406 |

Source: outputs/tables/tabla_4_6_estabilidad_por_escenario.csv and outputs/tables/tabla_4_1_descriptivos_principales.csv.

## Inferential evidence

| Metric | Scenarios | N | H | df | p | epsilon-squared |
|---|---|---:|---:|---:|---:|---:|
| RSSI DL | E0–E5 | 25944 | 5846.432 | 5 | <0.001 | 0.225 |
| SNR DL | E0–E5 | 25944 | 5385.396 | 5 | <0.001 | 0.207 |
| MCS DL | E0–E5 | 25947 | 4429.280 | 5 | <0.001 | 0.171 |
| Throughput DL | E1–E5 | 11492 | 1659.254 | 4 | <0.001 | 0.144 |

Source: outputs/tables/tabla_4_2_kruskal_wallis.csv.

Post-hoc Dunn comparisons are Holm-adjusted. The complete comparison table is outputs/tables/tabla_4_3_dunn_completa.csv; significant comparisons are retained in outputs/tables/tabla_4_3_dunn_significativas.csv.

## Stability evidence

The composite stability index currently stored in outputs/tables/rc1_indice_estabilidad.csv is:

| Scenario | Variability index | Stability index |
|---|---:|---:|
| E3 | 0.0880 | 0.9120 |
| E4 | 0.4434 | 0.5566 |
| E5 | 0.4554 | 0.5446 |
| E1 | 0.7428 | 0.2572 |
| E2 | 0.7698 | 0.2302 |
| E0 | 0.9172 | 0.0828 |

Important scope note: throughput is unavailable for E0. The publication branch therefore treats the four-dimensional composite stability comparison as directly comparable across E1–E5, while E0 remains available for the signal-only descriptive and inferential analyses.

## Multiscale robustness evidence

MTRA is a sensitivity framework using fixed 15, 30 and 60 minute aggregation windows. It does not claim to introduce a new statistical test.

| Scale | Metric | N | H | df | p | epsilon-squared | Significant Dunn-Holm pairs |
|---|---|---:|---:|---:|---:|---:|---:|
| 15 min | RSSI | 4848 | 2061.760 | 5 | <0.001 | 0.424775 | 14/15 |
| 15 min | SNR | 4848 | 1694.785 | 5 | <0.001 | 0.348985 | 13/15 |
| 15 min | MCS | 4849 | 1836.295 | 5 | <0.001 | 0.378132 | 13/15 |
| 15 min | Observed throughput | 3876 | 514.595 | 4 | <0.001 | 0.131903 | 7/10 |
| 30 min | RSSI | 2434 | 1102.430 | 5 | <0.001 | 0.451989 | 13/15 |
| 30 min | SNR | 2434 | 882.011 | 5 | <0.001 | 0.361207 | 13/15 |
| 30 min | MCS | 2435 | 1114.498 | 5 | <0.001 | 0.456772 | 13/15 |
| 30 min | Observed throughput | 1952 | 263.617 | 4 | <0.001 | 0.133342 | 6/10 |
| 60 min | RSSI | 1223 | 588.574 | 5 | <0.001 | 0.479519 | 13/15 |
| 60 min | SNR | 1223 | 456.070 | 5 | <0.001 | 0.370641 | 13/15 |
| 60 min | MCS | 1223 | 657.232 | 5 | <0.001 | 0.535934 | 13/15 |
| 60 min | Observed throughput | 983 | 139.744 | 4 | <0.001 | 0.138797 | 6/10 |

Source: outputs/article_tables/Table_MTRA_validated.csv.

## Manuscript claim discipline

The manuscript should distinguish three levels:

1. Observed result: directly reported descriptive or inferential statistic.
2. Interpretation: technical explanation supported by the experimental design and cited literature.
3. Generalization: any statement extending beyond this link, these configurations, or this observation period. Such statements require explicit qualification.

Avoid causal wording such as “frequency caused” or “bandwidth caused” unless the manuscript explicitly justifies the causal design. The safer formulation for the current evidence is “configuration was associated with differences in…”, while the controlled configuration changes can be described as experimental factors.

## Current publication figures

- Fig. 2 — configuration-dependent performance profiles.
- Fig. 3 — mean performance versus temporal variability.
- Fig. 4 — MTRA effect sizes across temporal scales.
- Fig. 5 — metric-specific stability across temporal scales.

## Drafting order

1. Methods and experimental design.
2. Results: configuration-dependent differences.
3. Results: temporal stability.
4. Results: multiscale robustness.
5. Discussion and limitations.
6. Introduction and related work.
7. Abstract and conclusions.

This order is intentional: the manuscript is drafted from frozen evidence rather than from a narrative chosen before the results are audited.

