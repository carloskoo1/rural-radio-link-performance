# Methods draft — Beyond RSSI

## 2. Methods

### 2.1 Experimental design and testbed

The study used a sequential field-experiment design for a long-distance point-to-point wireless link deployed in a rural high-Andean environment in Cajamarca, Peru. The experimental factor was the radio configuration, represented by the operating frequency and channel bandwidth. The route, radio equipment, antennas, alignment, and infrastructure were maintained constant to the extent operationally possible while the configuration was changed sequentially.

Six operating scenarios were evaluated. E0 was the baseline configuration, while E1-E5 represented alternative frequency-bandwidth combinations. The repository identifies the scenarios as E0 (5800 MHz/20 MHz), E1 (5660 MHz/40 MHz), E2 (5660 MHz/80 MHz), E3 (5730 MHz/40 MHz), E4 (5730 MHz/80 MHz), and E5 (5805 MHz/40 MHz).

The experimental records cover the following observation windows in the versioned raw dataset: E0, 19-28 February 2026; E1, 2-11 April 2026; E2, 12-21 April 2026; E3, 3-12 May 2026; E4, 13-22 May 2026; and E5, 23 May-2 June 2026. The number of usable records is not identical across scenarios because the analysis retained the observations available after the documented data-cleaning and validity procedures. The descriptive dataset contains 14,400 records for E0, 2,760 for E1, 2,245 for E2, 2,381 for E3, 2,184 for E4, and 2,137 for E5.

### 2.2 Experimental configurations

| Scenario | Frequency | Channel bandwidth | Data source |
|---|---:|---:|---|
| E0 | 5800 MHz | 20 MHz | Local ePMP telemetry |
| E1 | 5660 MHz | 40 MHz | cnMaestro |
| E2 | 5660 MHz | 80 MHz | cnMaestro |
| E3 | 5730 MHz | 40 MHz | cnMaestro |
| E4 | 5730 MHz | 80 MHz | cnMaestro |
| E5 | 5805 MHz | 40 MHz | cnMaestro |

The configuration assignment and scenario metadata are defined in the repository configuration file and are used by the consolidation pipeline to normalize the raw observations.

### 2.3 Measurement variables and data sources

The primary radio-performance variables were downlink received signal strength indicator (RSSI DL), downlink signal-to-noise ratio (SNR DL), downlink modulation and coding scheme (MCS DL), and observed downlink throughput. RSSI and SNR characterize the received radio conditions, MCS represents the link's modulation/coding state, and observed throughput represents the measured data-transfer performance available in the telemetry.

The raw observations were obtained from local ePMP telemetry for E0 and from cnMaestro-derived performance records for E1-E5. The repository's data model also contains fields for uplink metrics and auxiliary counters; however, the publication extension restricts its primary analysis to the downlink variables listed above.

ERA5-Land and NASA POWER are deliberately excluded from the publication analysis. They remain in the research repository as part of the original experimental project but are not used as evidence in the Beyond RSSI manuscript.

### 2.4 Data preparation and quality control

The data-processing workflow consisted of integrity checking, cleaning, field normalization, temporal synchronization, consolidation, statistical analysis, and generation of versioned outputs.

Raw scenario files were first mapped to the corresponding experimental configuration. The consolidation procedure normalized timestamps and metric names and converted numeric fields into a common representation. Invalid or unavailable measurements were represented as missing values rather than being silently imputed. The pipeline also documents exclusions and preserves the original scenario identity and source file.

The resulting scenario dataset was organized around timestamp, scenario identifier, frequency, channel bandwidth, RSSI DL, SNR DL, MCS DL, and observed throughput DL. E0 does not contain an observed-throughput measurement compatible with the E1-E5 throughput series; consequently, E0 is excluded from throughput comparisons but remains included in RSSI, SNR, and MCS analyses.

### 2.5 Statistical analysis

The statistical analysis was designed to evaluate whether the radio configuration was associated with differences in the measured performance variables without treating the observational data as evidence of a universal causal effect.

Normality was evaluated using the Shapiro-Wilk procedure. Because the resulting analysis was based on non-parametric group comparisons, global differences among scenarios were evaluated using the Kruskal-Wallis test. The magnitude of the global effect was quantified using epsilon-squared.

When the global comparison was significant, pairwise differences were examined using Dunn's post-hoc procedure with Holm adjustment for multiple comparisons. This procedure was applied to RSSI DL, SNR DL, MCS DL, and, separately, observed throughput DL for E1-E5.

The principal global comparisons were:

- RSSI DL: E0-E5;
- SNR DL: E0-E5;
- MCS DL: E0-E5;
- observed throughput DL: E1-E5.

The statistical workflow and the corresponding evidence tables are versioned in the repository.

### 2.6 Temporal stability

Temporal stability was evaluated separately from the central tendency of each metric. For RSSI, variability was represented by the standard deviation in dB. For SNR, MCS, and observed throughput, the coefficient of variation (CV) was calculated as the standard deviation divided by the absolute mean and expressed as a percentage.

A composite stability index was constructed from four variability components: RSSI standard deviation, SNR CV, MCS CV, and observed-throughput CV. Each component was min-max normalized across the evaluated scenarios. The normalized components were then averaged to obtain a composite variability index, and stability was defined as one minus that normalized variability index.

The resulting index is explicitly comparative within the evaluated dataset; it is not intended to represent a universal or externally calibrated scale. Because observed throughput is unavailable for E0, the four-component composite index is directly comparable only across E1-E5. E0 remains available for the signal-only stability descriptors.

### 2.7 Multiscale Temporal Robustness Analysis

Multiscale Temporal Robustness Analysis (MTRA) was introduced as a sensitivity framework to determine whether configuration-dependent differences remain detectable when the telemetry is aggregated over different temporal scales. It is not presented as a new statistical test.

The telemetry was aggregated using arithmetic means at fixed 15-, 30-, and 60-minute windows. At each temporal scale, Kruskal-Wallis tests were applied to RSSI DL, SNR DL, MCS DL, and observed throughput DL, followed by epsilon-squared effect-size estimation and Dunn pairwise comparisons with Holm adjustment.

The resulting MTRA evidence table reports the sample size, Kruskal-Wallis statistic, degrees of freedom, p-value, epsilon-squared, and number of significant Dunn-Holm comparisons at each temporal scale. The frozen table is stored as `outputs/article_tables/Table_MTRA_validated.csv`.

### 2.8 Reproducibility and traceability

The analysis is maintained in the Git repository `carloskoo1/rural-radio-link-performance`. The publication extension is developed in the `article/beyond-rssi` branch, while the reproducible thesis release remains identified by tag `v1.0.0`.

The repository contains the raw scenario organization, data-processing scripts, statistical pipeline, evidence tables, publication figures, and reproducibility documentation. The publication figures are generated by `scripts/article/generate_article_figures.js` from the frozen evidence used for the article extension.

The reproducibility level of the current publication extension is output-reproducible: the versioned figures and MTRA evidence table can be reconstructed exactly from the frozen statistical values. Full analytical reproducibility additionally depends on auditing and executing the upstream thesis statistical pipeline.

### 2.9 Scope and methodological limitations

The study evaluates one long-distance point-to-point link under the operating conditions represented by the recorded field campaign. Therefore, the results should be interpreted as configuration-dependent empirical evidence for the evaluated link and observation periods rather than as a universal characterization of all wireless links operating at the evaluated frequencies or bandwidths.

The sequential field design also means that the scenarios were observed during different calendar periods. The manuscript therefore reports configuration-associated differences and temporal robustness rather than claiming that the experimental data isolate frequency or bandwidth as independent causal factors under all environmental and operational conditions.

