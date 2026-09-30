# Results draft — Beyond RSSI

## 3. Results

### 3.1 Configuration-dependent performance

The descriptive results show measurable differences among the six radio configurations across RSSI DL, SNR DL, and MCS DL. RSSI DL means ranged from -76.668 dBm in E1 to -74.396 dBm in E2, while SNR DL means ranged from 19.936 dB in E3 to 21.678 dB in E2. Mean MCS ranged from 103.300 in E2 to 104.995 in E0. Observed throughput was available for E1-E5 and ranged from 0.588 Mb/s in E2 to 0.791 Mb/s in E4.

The global Kruskal-Wallis analysis identified statistically significant differences among scenarios for all four analyzed metrics. RSSI DL: H = 5846.432, df = 5, p < 0.001, epsilon-squared = 0.225. SNR DL: H = 5385.396, df = 5, p < 0.001, epsilon-squared = 0.207. MCS DL: H = 4429.280, df = 5, p < 0.001, epsilon-squared = 0.171. Observed throughput DL, evaluated across E1-E5: H = 1659.254, df = 4, p < 0.001, epsilon-squared = 0.144.

The post-hoc Dunn analysis with Holm adjustment showed multiple statistically significant pairwise differences: 14/15 comparisons for RSSI DL, 13/15 for SNR DL, 13/15 for MCS DL, and 7/10 for observed throughput DL.

These results indicate that the measured performance distributions differed across the tested configurations. Because the scenarios were evaluated sequentially during different calendar periods, the results are reported as configuration-associated differences rather than as a universal causal effect attributable exclusively to frequency or bandwidth.

### 3.2 Temporal stability

The configuration differences were not limited to mean performance. RSSI DL standard deviation ranged from 0.673 dB in E4 to 1.092 dB in E1 among E1-E5. SNR DL standard deviation ranged from 0.424 dB in E3 to 1.047 dB in E4. MCS standard deviation ranged from 0.645 in E5 to 1.805 in E2. Observed-throughput standard deviation ranged from 0.375 Mb/s in E2 to 0.428 Mb/s in E4.

SNR CV ranged from 2.128% in E3 to 5.081% in E4. MCS CV ranged from 0.614% in E5 to 1.747% in E2. Observed-throughput CV ranged from 49.716% in E3 to 63.839% in E2.

A four-component composite stability index was calculated from normalized RSSI standard deviation, SNR CV, MCS CV, and observed-throughput CV. The index is a relative measure within the evaluated dataset. Across E1-E5, the values were E3 = 0.9120, E4 = 0.5566, E5 = 0.5446, E1 = 0.2572, and E2 = 0.2302. E0 is not directly comparable in this four-component publication index because observed throughput is unavailable.

The stability analysis provides information not captured by mean performance alone. The scenario with the largest mean throughput is not necessarily the scenario with the smallest relative variability, supporting the analysis of central tendency and stability as separate dimensions.

### 3.3 Multiscale temporal robustness

MTRA evaluated whether configuration-associated differences persisted after aggregation at 15-, 30-, and 60-minute scales.

At 15 minutes, epsilon-squared values were 0.424775 for RSSI, 0.348985 for SNR, 0.378132 for MCS, and 0.131903 for observed throughput. Sample sizes were 4,848, 4,848, 4,849, and 3,876, respectively; all global tests had p < 0.001.

At 30 minutes, epsilon-squared values were 0.451989 for RSSI, 0.361207 for SNR, 0.456772 for MCS, and 0.133342 for observed throughput. Sample sizes were 2,434, 2,434, 2,435, and 1,952.

At 60 minutes, epsilon-squared values were 0.479519 for RSSI, 0.370641 for SNR, 0.535934 for MCS, and 0.138797 for observed throughput. Sample sizes were 1,223, 1,223, 1,223, and 983.

Significant Dunn-Holm comparisons remained substantial across scales: RSSI 14/15 at 15 minutes and 13/15 at 30 and 60 minutes; SNR 13/15 at all three scales; MCS 13/15 at all three scales; observed throughput 7/10 at 15 minutes and 6/10 at 30 and 60 minutes.

The MTRA results show that configuration-associated differences detected in the raw telemetry remain detectable after aggregation at all three evaluated temporal scales. MTRA is interpreted as a temporal sensitivity assessment, not as evidence that one temporal resolution is intrinsically superior.

### 3.4 Evidence traceability

Descriptive statistics are stored in outputs/tables/tabla_4_1_descriptivos_principales.csv; Kruskal-Wallis results in outputs/tables/tabla_4_2_kruskal_wallis.csv; significant Dunn-Holm comparisons in outputs/tables/tabla_4_3_dunn_significativas.csv; stability descriptors in outputs/tables/tabla_4_6_estabilidad_por_escenario.csv; the composite stability calculation in outputs/tables/rc1_indice_estabilidad.csv; and MTRA evidence in outputs/article_tables/Table_MTRA_validated.csv.

Publication figures are Fig. 2 configuration-dependent performance profiles, Fig. 3 mean performance versus temporal variability, Fig. 4 MTRA effect sizes, and Fig. 5 metric-specific stability across temporal scales.
