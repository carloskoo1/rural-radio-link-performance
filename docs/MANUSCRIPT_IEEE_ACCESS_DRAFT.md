# Beyond RSSI: Multimetric Temporal Stability and Multiscale Assessment of a Long-Distance Point-to-Point Wireless Link

**Author list:** TO BE CONFIRMED FROM THE THESIS RECORD

## Abstract

Received signal strength is widely used for operational monitoring of wireless links, but a single signal-strength indicator does not necessarily represent link adaptation, delivered throughput, or temporal stability. This study presents a field-based multidimensional assessment of a long-distance point-to-point wireless link operated under six frequency-bandwidth configurations. Downlink RSSI, SNR, MCS, and observed throughput were analyzed using non-parametric group comparisons, effect-size estimation, temporal variability measures, and a multiscale sensitivity analysis.

Kruskal-Wallis tests identified statistically significant differences among configurations for RSSI (H=5846.432, epsilon-squared=0.225), SNR (H=5385.396, epsilon-squared=0.207), MCS (H=4429.280, epsilon-squared=0.171), and observed throughput across E1-E5 (H=1659.254, epsilon-squared=0.144), with p<0.001 in all cases. A four-component comparative stability index was calculated from normalized variability in RSSI, SNR, MCS, and observed throughput. Multiscale Temporal Robustness Analysis (MTRA) evaluated persistence at 15-, 30-, and 60-minute aggregation scales. Significant differences remained detectable at all three scales, while epsilon-squared for MCS increased from 0.378 at 15 minutes to 0.536 at 60 minutes.

The findings indicate that long-distance wireless-link assessment benefits from a multidimensional and multiscale perspective in which signal strength is interpreted jointly with signal quality, link adaptation, throughput, and temporal stability. The study is limited to one field link and a sequential configuration design; consequently, results are interpreted as configuration-associated empirical evidence rather than universal causal effects.

**Keywords—** wireless link; RSSI; SNR; MCS; throughput; temporal stability; multiscale analysis; point-to-point radio; link quality.


## 1. Introduction

Long-distance point-to-point wireless links are frequently monitored through a small set of radio indicators, among which received signal strength is one of the most accessible. RSSI is useful for diagnosing gross changes in received power and for verifying link conditions, but a single signal-strength statistic does not necessarily describe the complete operational state of a wireless link. Experimental studies have shown that wireless-link behavior depends on the interaction among signal quality, modulation and coding, traffic conditions, and temporal channel dynamics. For example, measurements of IEEE 802.11ad have evaluated RSSI together with MCS and TCP/UDP throughput rather than treating received signal strength as a complete performance descriptor. [1]

This distinction becomes relevant in fixed outdoor links because a configuration that produces a favorable received-power level may not produce the same behavior at the modulation/coding or throughput layers. The physical and link layers are coupled through adaptive modulation and coding, while the delivered throughput also depends on protocol and traffic behavior. Consequently, radio-link assessment benefits from observing multiple layers of telemetry rather than relying on a single radio-strength indicator.

Temporal behavior introduces a second dimension to this problem. Fixed wireless channels can exhibit time-varying behavior and fade dynamics even when the physical endpoints remain stationary. Measurement studies of fixed wireless links have therefore examined the temporal stability of received signals and the occurrence of fades over time. [2] More recent experimental work in wireless networking likewise treats temporal stability as a relevant performance dimension rather than considering only average throughput or instantaneous link quality. [3]

A further methodological question concerns temporal aggregation. A difference observed at a fine time scale may weaken or disappear after aggregation, whereas a persistent configuration-associated difference may remain detectable at multiple temporal resolutions. Multiscale analysis is established in temporal-network research, although its objectives and methods vary substantially across application domains. [10] In wireless systems, experimental multiscale studies have evaluated performance under distinct sampling or control time scales, while link-quality research has also examined how temporal windows affect the convergence of quality metrics. [9], [10]

Despite this body of work, there remains a practical methodological gap for long-distance fixed point-to-point radio links: experimental assessments often emphasize one performance dimension, or analyze several metrics without explicitly separating central tendency, temporal variability, and robustness to temporal aggregation. A systematic field assessment that combines signal level, signal quality, link-adaptation state, measured throughput, configuration comparison, temporal stability, and multiscale sensitivity can provide a more complete characterization of the operational behavior of a link.

This study addresses that gap through a field experiment on a long-distance point-to-point wireless link operated under six radio configurations defined by frequency and channel bandwidth. The analysis considers four primary downlink metrics: RSSI, SNR, MCS, and observed throughput. Configuration-associated differences are evaluated using non-parametric statistical comparisons and epsilon-squared effect sizes. Temporal stability is assessed independently from central tendency, and a composite stability index is used as a comparative descriptor within the evaluated scenarios. Finally, Multiscale Temporal Robustness Analysis (MTRA) evaluates whether configuration-associated differences remain detectable after aggregation at 15-, 30-, and 60-minute temporal scales.

The study does not claim that RSSI is an invalid metric or that a specific frequency or bandwidth is universally optimal. Instead, it evaluates whether a multidimensional and multiscale characterization provides information that is not captured by RSSI alone.

The main contributions of this work are:

1. An experimental multidimensional characterization of a long-distance point-to-point wireless link using RSSI, SNR, MCS, and observed throughput across six frequency-bandwidth configurations.
2. A separate treatment of temporal stability that distinguishes average performance from variability and combines four normalized variability components into a comparative stability index.
3. A multiscale sensitivity framework, MTRA, that evaluates the persistence of configuration-associated differences at 15-, 30-, and 60-minute aggregation scales.
4. A reproducible evidence pipeline linking scenario data products, statistical outputs, publication tables, and figures through a version-controlled repository.

The remainder of the paper is organized as follows. Section 2 reviews previous work on multidimensional wireless-link assessment, temporal stability, and multiscale analysis. Section 3 describes the experimental methodology and statistical procedures. Section 4 presents the results. Section 5 discusses their technical and methodological implications. Section 6 addresses limitations, and Section 7 concludes the study.

## 2. Related Work

### 2.1 Signal indicators and wireless-link performance

RSSI and related received-signal indicators are widely used because they provide a direct operational measure of received power. However, their relationship with actual data performance depends on the radio technology, interference environment, modulation/coding state, bandwidth, and traffic conditions. Experimental evaluation of IEEE 802.11ad, for example, has explicitly combined RSSI measurements with different MCS configurations and TCP/UDP throughput measurements, illustrating the need to connect signal conditions with delivered performance. [1]

The distinction between signal strength and data performance is also reflected in wireless-network modeling approaches in which RSSI is used as one input to estimate data-rate potential while MCS, channel bandwidth, coding, and spatial streams contribute to the resulting physical rate. [6] These studies support a multidimensional interpretation of radio-link performance, but they do not by themselves address the temporal stability framework used in the present field experiment.

### 2.2 SNR, MCS, and throughput

SNR provides information about signal quality relative to noise and is directly relevant to the ability of adaptive modulation and coding mechanisms to select transmission states. MCS, in turn, represents a link-adaptation state that connects channel conditions with modulation and coding efficiency. Experimental work on wireless links has therefore examined SNR, MCS, and throughput jointly rather than interpreting RSSI as a sufficient descriptor. [1], [6]

The present study extends this perspective in a different direction. Rather than estimating throughput from a theoretical PHY-rate model or evaluating isolated signal-quality conditions, it uses measured field telemetry and compares the empirical distributions of RSSI, SNR, MCS, and observed throughput across sustained operating configurations.

### 2.3 Temporal variability and stability of fixed wireless links

Temporal variation is an established characteristic of wireless channels. Measurement and statistical analysis of fixed wireless links have been used to characterize signal variations, fade probability, fade depth, and environmental influences. [2] Earlier work on short-term wireless-link estimation likewise treated temporal stability as a distinct property that can be useful for network decisions. [7]

More recent wireless measurement studies continue to emphasize temporal stability. For example, experimental Wi-Fi 6 work has evaluated temporal jitter and latency under alternative MAC configurations, while recent wireless-network studies have considered temporal stability and continuity as dimensions of network performance. [3], [8]

These studies establish the importance of temporal behavior but generally address different technologies, mobility conditions, network layers, or objectives. The present work focuses specifically on a long-distance fixed point-to-point link and treats temporal variability as an explicit dimension of configuration assessment.

### 2.4 Multiscale temporal analysis

Multiscale analysis is used in several areas of network science to characterize dynamics that depend on the temporal or structural scale at which observations are examined. Temporal-network research has demonstrated that conclusions about dynamic network behavior can depend on the temporal scale used for analysis. [10]

In wireless experimental research, changing the aggregation window can similarly affect variance, sample size, and the apparent persistence of performance differences. Recent experimental work with wireless sensor systems, for example, has explicitly compared multiple aggregation windows and examined whether qualitative performance relationships remain stable as temporal resolution changes. [5]

The present study uses this principle as a sensitivity analysis rather than as a predictive model. MTRA does not attempt to forecast future link states or infer a universal temporal scale. Instead, it asks whether configuration-associated differences detected in the field telemetry remain statistically detectable at three predefined temporal resolutions.

### 2.5 Research gap

The reviewed literature establishes four relevant facts: (i) RSSI is useful but does not fully represent wireless performance; (ii) SNR, MCS, and throughput provide complementary information; (iii) temporal stability is a relevant property of fixed and mobile wireless systems; and (iv) temporal aggregation can affect the interpretation of dynamic network measurements. [1]-[10]

The remaining gap addressed by this study is therefore not the absence of any individual metric or statistical method. Rather, it is the integration of these dimensions into a single empirical assessment of a real long-distance point-to-point link under controlled configuration changes. The study combines multidimensional performance characterization, explicit temporal-stability analysis, and multiscale sensitivity testing within the same field experiment, while preserving the resulting evidence in a version-controlled reproducibility pipeline.

This framing deliberately avoids claiming methodological priority for MTRA or novelty for the individual statistical tests. The contribution lies in the experimental integration and evidence structure applied to the specific problem of configuration-dependent long-distance radio-link assessment.



## 3. Methods



### 3.1 Experimental design and testbed

The study used a sequential field-experiment design for a long-distance point-to-point wireless link deployed in a rural high-Andean environment in Cajamarca, Peru. The experimental factor was the radio configuration, represented by the operating frequency and channel bandwidth. The route, radio equipment, antennas, alignment, and infrastructure were maintained constant to the extent operationally possible while the configuration was changed sequentially.

Six operating scenarios were evaluated. E0 was the baseline configuration, while E1-E5 represented alternative frequency-bandwidth combinations. The repository identifies the scenarios as E0 (5800 MHz/20 MHz), E1 (5660 MHz/40 MHz), E2 (5660 MHz/80 MHz), E3 (5730 MHz/40 MHz), E4 (5730 MHz/80 MHz), and E5 (5805 MHz/40 MHz).

The experimental records cover the following observation windows in the versioned raw dataset: E0, 19-28 February 2026; E1, 2-11 April 2026; E2, 12-21 April 2026; E3, 3-12 May 2026; E4, 13-22 May 2026; and E5, 23 May-2 June 2026. The number of usable records is not identical across scenarios because the analysis retained the observations available after the documented data-cleaning and validity procedures. The descriptive dataset contains 14,400 records for E0, 2,760 for E1, 2,245 for E2, 2,381 for E3, 2,184 for E4, and 2,137 for E5.

### 3.2 Experimental configurations

| Scenario | Frequency | Channel bandwidth | Data source |
|---|---:|---:|---|
| E0 | 5800 MHz | 20 MHz | Local ePMP telemetry |
| E1 | 5660 MHz | 40 MHz | cnMaestro |
| E2 | 5660 MHz | 80 MHz | cnMaestro |
| E3 | 5730 MHz | 40 MHz | cnMaestro |
| E4 | 5730 MHz | 80 MHz | cnMaestro |
| E5 | 5805 MHz | 40 MHz | cnMaestro |

The configuration assignment and scenario metadata are defined in the repository configuration file and are used by the consolidation pipeline to normalize the raw observations.

### 3.3 Measurement variables and data sources

The primary radio-performance variables were downlink received signal strength indicator (RSSI DL), downlink signal-to-noise ratio (SNR DL), downlink modulation and coding scheme (MCS DL), and observed downlink throughput. RSSI and SNR characterize the received radio conditions, MCS represents the link's modulation/coding state, and observed throughput represents the measured data-transfer performance available in the telemetry.

The raw observations were obtained from local ePMP telemetry for E0 and from cnMaestro-derived performance records for E1-E5. The repository's data model also contains fields for uplink metrics and auxiliary counters; however, the publication extension restricts its primary analysis to the downlink variables listed above.

ERA5-Land and NASA POWER are deliberately excluded from the publication analysis. They remain in the research repository as part of the original experimental project but are not used as evidence in the Beyond RSSI manuscript.

### 3.4 Data preparation and quality control

The data-processing workflow consisted of integrity checking, cleaning, field normalization, temporal synchronization, consolidation, statistical analysis, and generation of versioned outputs.

Raw scenario files were first mapped to the corresponding experimental configuration. The consolidation procedure normalized timestamps and metric names and converted numeric fields into a common representation. Invalid or unavailable measurements were represented as missing values rather than being silently imputed. The pipeline also documents exclusions and preserves the original scenario identity and source file.

The resulting scenario dataset was organized around timestamp, scenario identifier, frequency, channel bandwidth, RSSI DL, SNR DL, MCS DL, and observed throughput DL. E0 does not contain an observed-throughput measurement compatible with the E1-E5 throughput series; consequently, E0 is excluded from throughput comparisons but remains included in RSSI, SNR, and MCS analyses.

### 3.5 Statistical analysis

The statistical analysis was designed to evaluate whether the radio configuration was associated with differences in the measured performance variables without treating the observational data as evidence of a universal causal effect.

Normality was evaluated using the Shapiro-Wilk procedure. Because the resulting analysis was based on non-parametric group comparisons, global differences among scenarios were evaluated using the Kruskal-Wallis test. The magnitude of the global effect was quantified using epsilon-squared.

When the global comparison was significant, pairwise differences were examined using Dunn's post-hoc procedure with Holm adjustment for multiple comparisons. This procedure was applied to RSSI DL, SNR DL, MCS DL, and, separately, observed throughput DL for E1-E5.

The principal global comparisons were:

- RSSI DL: E0-E5;
- SNR DL: E0-E5;
- MCS DL: E0-E5;
- observed throughput DL: E1-E5.

The statistical workflow and the corresponding evidence tables are versioned in the repository.

### 3.6 Temporal stability

Temporal stability was evaluated separately from the central tendency of each metric. For RSSI, variability was represented by the standard deviation in dB. For SNR, MCS, and observed throughput, the coefficient of variation (CV) was calculated as the standard deviation divided by the absolute mean and expressed as a percentage.

A composite stability index was constructed from four variability components: RSSI standard deviation, SNR CV, MCS CV, and observed-throughput CV. Each component was min-max normalized across the evaluated scenarios. The normalized components were then averaged to obtain a composite variability index, and stability was defined as one minus that normalized variability index.

The resulting index is explicitly comparative within the evaluated dataset; it is not intended to represent a universal or externally calibrated scale. Because observed throughput is unavailable for E0, the four-component composite index is directly comparable only across E1-E5. E0 remains available for the signal-only stability descriptors.

### 3.7 Multiscale Temporal Robustness Analysis

Multiscale Temporal Robustness Analysis (MTRA) was introduced as a sensitivity framework to determine whether configuration-dependent differences remain detectable when the telemetry is aggregated over different temporal scales. It is not presented as a new statistical test.

The telemetry was aggregated using arithmetic means at fixed 15-, 30-, and 60-minute windows. At each temporal scale, Kruskal-Wallis tests were applied to RSSI DL, SNR DL, MCS DL, and observed throughput DL, followed by epsilon-squared effect-size estimation and Dunn pairwise comparisons with Holm adjustment.

The resulting MTRA evidence table reports the sample size, Kruskal-Wallis statistic, degrees of freedom, p-value, epsilon-squared, and number of significant Dunn-Holm comparisons at each temporal scale. The frozen table is stored as `outputs/article_tables/Table_MTRA_validated.csv`.

### 3.8 Reproducibility and traceability

The analysis is maintained in the Git repository `carloskoo1/rural-radio-link-performance`. The publication extension is developed in the `article/beyond-rssi` branch, while the reproducible thesis release remains identified by tag `v1.0.0`.

The repository contains the raw scenario organization, data-processing scripts, statistical pipeline, evidence tables, publication figures, and reproducibility documentation. The publication figures are generated by `scripts/article/generate_article_figures.js` from the frozen evidence used for the article extension.

The reproducibility level of the current publication extension is output-reproducible: the versioned figures and MTRA evidence table can be reconstructed exactly from the frozen statistical values. Full analytical reproducibility additionally depends on auditing and executing the upstream thesis statistical pipeline.

### 3.9 Scope and methodological limitations

The study evaluates one long-distance point-to-point link under the operating conditions represented by the recorded field campaign. Therefore, the results should be interpreted as configuration-dependent empirical evidence for the evaluated link and observation periods rather than as a universal characterization of all wireless links operating at the evaluated frequencies or bandwidths.

The sequential field design also means that the scenarios were observed during different calendar periods. The manuscript therefore reports configuration-associated differences and temporal robustness rather than claiming that the experimental data isolate frequency or bandwidth as independent causal factors under all environmental and operational conditions.



## 4. Results

### 4.1 Configuration-dependent performance

The descriptive results show measurable differences among the six radio configurations across RSSI DL, SNR DL, and MCS DL. RSSI DL means ranged from -76.668 dBm in E1 to -74.396 dBm in E2, while SNR DL means ranged from 19.936 dB in E3 to 21.678 dB in E2. Mean MCS ranged from 103.300 in E2 to 104.995 in E0. Observed throughput was available for E1-E5 and ranged from 0.588 Mb/s in E2 to 0.791 Mb/s in E4.

The global Kruskal-Wallis analysis identified statistically significant differences among scenarios for all four analyzed metrics. RSSI DL: H = 5846.432, df = 5, p < 0.001, epsilon-squared = 0.225. SNR DL: H = 5385.396, df = 5, p < 0.001, epsilon-squared = 0.207. MCS DL: H = 4429.280, df = 5, p < 0.001, epsilon-squared = 0.171. Observed throughput DL, evaluated across E1-E5: H = 1659.254, df = 4, p < 0.001, epsilon-squared = 0.144.

The post-hoc Dunn analysis with Holm adjustment showed multiple statistically significant pairwise differences: 14/15 comparisons for RSSI DL, 13/15 for SNR DL, 13/15 for MCS DL, and 7/10 for observed throughput DL.

These results indicate that the measured performance distributions differed across the tested configurations. Because the scenarios were evaluated sequentially during different calendar periods, the results are reported as configuration-associated differences rather than as a universal causal effect attributable exclusively to frequency or bandwidth.

### 4.2 Temporal stability

The configuration differences were not limited to mean performance. RSSI DL standard deviation ranged from 0.673 dB in E4 to 1.092 dB in E1 among E1-E5. SNR DL standard deviation ranged from 0.424 dB in E3 to 1.047 dB in E4. MCS standard deviation ranged from 0.645 in E5 to 1.805 in E2. Observed-throughput standard deviation ranged from 0.375 Mb/s in E2 to 0.428 Mb/s in E4.

SNR CV ranged from 2.128% in E3 to 5.081% in E4. MCS CV ranged from 0.614% in E5 to 1.747% in E2. Observed-throughput CV ranged from 49.716% in E3 to 63.839% in E2.

A four-component composite stability index was calculated from normalized RSSI standard deviation, SNR CV, MCS CV, and observed-throughput CV. The index is a relative measure within the evaluated dataset. Across E1-E5, the values were E3 = 0.9120, E4 = 0.5566, E5 = 0.5446, E1 = 0.2572, and E2 = 0.2302. E0 is not directly comparable in this four-component publication index because observed throughput is unavailable.

The stability analysis provides information not captured by mean performance alone. The scenario with the largest mean throughput is not necessarily the scenario with the smallest relative variability, supporting the analysis of central tendency and stability as separate dimensions.

### 4.3 Multiscale temporal robustness

MTRA evaluated whether configuration-associated differences persisted after aggregation at 15-, 30-, and 60-minute scales.

At 15 minutes, epsilon-squared values were 0.424775 for RSSI, 0.348985 for SNR, 0.378132 for MCS, and 0.131903 for observed throughput. Sample sizes were 4,848, 4,848, 4,849, and 3,876, respectively; all global tests had p < 0.001.

At 30 minutes, epsilon-squared values were 0.451989 for RSSI, 0.361207 for SNR, 0.456772 for MCS, and 0.133342 for observed throughput. Sample sizes were 2,434, 2,434, 2,435, and 1,952.

At 60 minutes, epsilon-squared values were 0.479519 for RSSI, 0.370641 for SNR, 0.535934 for MCS, and 0.138797 for observed throughput. Sample sizes were 1,223, 1,223, 1,223, and 983.

Significant Dunn-Holm comparisons remained substantial across scales: RSSI 14/15 at 15 minutes and 13/15 at 30 and 60 minutes; SNR 13/15 at all three scales; MCS 13/15 at all three scales; observed throughput 7/10 at 15 minutes and 6/10 at 30 and 60 minutes.

The MTRA results show that configuration-associated differences detected in the raw telemetry remain detectable after aggregation at all three evaluated temporal scales. MTRA is interpreted as a temporal sensitivity assessment, not as evidence that one temporal resolution is intrinsically superior.

### 4.4 Evidence traceability

Descriptive statistics are stored in outputs/tables/tabla_4_1_descriptivos_principales.csv; Kruskal-Wallis results in outputs/tables/tabla_4_2_kruskal_wallis.csv; significant Dunn-Holm comparisons in outputs/tables/tabla_4_3_dunn_significativas.csv; stability descriptors in outputs/tables/tabla_4_6_estabilidad_por_escenario.csv; the composite stability calculation in outputs/tables/rc1_indice_estabilidad.csv; and MTRA evidence in outputs/article_tables/Table_MTRA_validated.csv.

Publication figures are Fig. 2 configuration-dependent performance profiles, Fig. 3 mean performance versus temporal variability, Fig. 4 MTRA effect sizes, and Fig. 5 metric-specific stability across temporal scales.


## 5. Discussion

### 5.1 Configuration dependence extends beyond RSSI

The results show that changing the radio configuration was associated with differences not only in received signal level but also in SNR, MCS, and observed throughput. The Kruskal-Wallis results and epsilon-squared values indicate that the scenario distributions were not interchangeable within the experimental dataset.

An important observation is that the metrics do not move as a single undifferentiated performance variable. E2 presented the highest mean RSSI (-74.396 dBm) and SNR (21.678 dB), but its mean MCS (103.300) and observed throughput (0.588 Mb/s) were not the highest among the scenarios with throughput measurements. Conversely, E4 presented the highest observed throughput mean (0.791 Mb/s) while its mean SNR was 20.616 dB and its mean MCS was 103.672. This divergence indicates that received signal strength alone does not provide a complete description of link performance in the evaluated configurations.

The result supports the central motivation of a beyond-RSSI analysis: a configuration can exhibit favorable signal-level statistics while presenting a different behavior in link adaptation and measured throughput. RSSI should therefore be interpreted as one component of a multidimensional performance state rather than as a sufficient proxy for end-to-end radio-link performance.

### 5.2 Signal quality, link adaptation, and throughput should be interpreted jointly

The observed differences among SNR, MCS, and throughput suggest that the relationship between physical-layer indicators and measured throughput is mediated by link adaptation and by characteristics of the measured traffic path. The present dataset does not establish a mechanistic causal model connecting a specific frequency or bandwidth to a specific MCS state or throughput value. It does show that the distributions of these metrics differ across configurations and that those differences remain statistically detectable.

The contrast between E2 and E4 is particularly relevant. E2 had the highest mean RSSI and SNR, but E4 had the highest observed throughput mean. This prevents a one-dimensional interpretation in which the configuration with the strongest received signal necessarily provides the highest measured throughput. The evidence instead supports joint inspection of received power, signal quality, modulation/coding state, and throughput.

### 5.3 Temporal stability adds information beyond mean performance

The stability analysis demonstrates that average performance and temporal variability describe different properties of a configuration. E3 had an observed-throughput CV of 49.716%, whereas E2 reached 63.839%. At the same time, E4 had the highest mean observed throughput (0.791 Mb/s) but an observed-throughput CV of 54.131%. Consequently, configuration assessment should distinguish expected performance from consistency of that performance.

The composite stability index formalizes this multidimensional comparison by combining normalized variability components from RSSI, SNR, MCS, and observed throughput. The index should be interpreted only as a comparative measure within this experiment because its normalization depends on the evaluated scenario set. It is not an externally calibrated reliability score.

Within E1-E5, the index values range from 0.2302 to 0.9120. This spread demonstrates that configurations can occupy substantially different regions of the variability space. The practical implication is that configuration assessment should consider central tendency and stability as separate dimensions.
### 5.4 Multiscale robustness of the configuration differences

MTRA provides a second dimension of evidence by testing the persistence of configuration-associated differences under temporal aggregation. The epsilon-squared values remain non-negligible at 15, 30, and 60 minutes for all four metrics, and the global tests remain significant at each scale.

The persistence is especially visible for MCS, whose epsilon-squared changes from 0.378 at 15 minutes to 0.457 at 30 minutes and 0.536 at 60 minutes. RSSI changes from 0.425 to 0.452 and 0.480 across the three scales. For observed throughput, epsilon-squared remains close to 0.13 across all scales. These patterns indicate that temporal aggregation does not eliminate the configuration structure present in the data.

MTRA should nevertheless be interpreted as a sensitivity analysis rather than as evidence that longer aggregation windows are intrinsically preferable. Aggregation changes temporal granularity and the number of observations and can alter variance and effect-size estimates. Its value here is that the main configuration differences remain detectable under three predefined temporal resolutions.

### 5.5 Methodological implications for radio-link monitoring

The combined results suggest that monitoring of long-distance point-to-point wireless links should not rely on a single signal indicator. The evaluated evidence supports simultaneous observation of RSSI, SNR, MCS, throughput, and temporal variability.

This does not imply that every deployment requires the same composite index or temporal windows used in this study. Rather, the experiment demonstrates a methodological pattern: configuration evaluation can be strengthened by separating central tendency from variability and by testing whether observed differences persist across temporal aggregation scales.

The repository implementation reinforces this methodological contribution because the statistical evidence, figures, and analysis definitions are versioned as a connected artifact. This allows the reported results to be traced from scenario-level data products to publication figures.

## 6. Limitations

Several limitations delimit the interpretation of the findings.

First, the experiment concerns one long-distance point-to-point link and therefore does not establish that the observed configuration patterns generalize to other links, terrains, antenna systems, radio platforms, or propagation conditions.

Second, the six scenarios were evaluated sequentially over different calendar periods. Although this reflects the field nature of the experiment, calendar-period effects and configuration effects cannot be completely separated by the current design. Accordingly, the manuscript uses configuration-associated language rather than attributing the observed differences exclusively to frequency or channel bandwidth.

Third, observed throughput is unavailable for E0 in a form directly comparable with E1-E5. E0 is therefore excluded from throughput comparisons and from the four-component publication stability index. This restriction should remain explicit in the article.

Fourth, the composite stability index is internally normalized across the evaluated scenarios. Its numerical scale should not be interpreted as a universal engineering threshold.

Finally, the current publication branch reproduces the frozen statistical outputs used to generate the article figures, but the publication generator itself does not independently recompute every upstream statistical test from raw observations. Full analytical reproducibility therefore depends on the upstream thesis pipeline and its audit. This distinction is documented in the repository and should remain visible in the final manuscript.

### 6.1 Implications for future experiments

The present evidence suggests several directions for a stronger subsequent experimental design. Repeated alternation among configurations within shorter controlled blocks would reduce confounding between configuration and calendar period. Replication across additional links and environmental conditions would provide evidence about external validity. A future campaign could also preserve synchronized throughput measurements for every configuration, including the baseline, allowing the stability index to be evaluated on a common metric set.

These extensions define the experimental steps needed to distinguish more strongly between configuration effects and time-varying field conditions.


## 7. Conclusions

This study evaluated a long-distance point-to-point wireless link using a multidimensional and multiscale experimental framework. Six frequency-bandwidth configurations were compared using RSSI, SNR, MCS, and observed throughput, complemented by temporal variability and multiscale sensitivity analysis.

The results show statistically significant configuration-associated differences across the evaluated metrics. More importantly, signal strength alone does not provide a complete description of operational link performance: the configuration with the highest mean RSSI and SNR did not have the highest observed throughput. This supports the use of joint telemetry involving signal level, signal quality, link-adaptation state, and delivered performance.

Temporal stability provided an additional dimension of comparison. The observed variability differed across configurations, and the composite stability index showed that configurations can occupy substantially different regions of the performance-variability space. The index is interpreted as an internal comparative descriptor rather than as a universal reliability scale.

MTRA showed that configuration-associated differences remained detectable at 15-, 30-, and 60-minute aggregation scales. This supports predefined temporal sensitivity checks when analyzing long-duration field telemetry because conclusions based on a single aggregation window may not fully characterize the persistence of observed differences.

The principal methodological contribution is the integration of multidimensional performance metrics, temporal stability, multiscale sensitivity, and reproducible evidence traceability in a real long-distance point-to-point field experiment. The findings should not be generalized beyond the evaluated link and observation periods without additional replicated experiments.

Future work should alternate configurations within shorter controlled blocks, replicate the experiment across additional links and propagation environments, and acquire synchronized throughput measurements for every configuration, including the baseline.


## Data and Code Availability

The analysis artifacts are maintained in the public repository: https://github.com/carloskoo1/rural-radio-link-performance. The repository contains the scenario organization, processing scripts, statistical outputs, publication figures, evidence matrix, and reproducibility documentation. The publication extension is maintained in the article/beyond-rssi branch.

## Acknowledgment

The manuscript drafting process used OpenAI ChatGPT for language organization, synthesis, and editorial assistance. Quantitative results, experimental descriptions, statistical values, and repository evidence were derived from the project's versioned research artifacts and were not generated from model inference. The final authors are responsible for verification of all scientific content, citations, authorship, and submission materials.

## References

[1] K. Nguyen, M. G. Kibria, K. Ishizu, and F. Kojima, â€œPerformance Evaluation of IEEE 802.11ad in Evolving Wi-Fi Networks,â€ Wireless Communications and Mobile Computing, vol. 2019, Article ID 4089365, 2019, doi: 10.1155/2019/4089365.

[2] L. Ahumada, R. Feick, R. A. Valenzuela, and C. Morales, â€œMeasurement and Characterization of the Temporal Behavior of Fixed Wireless Links,â€ IEEE Transactions on Vehicular Technology, vol. 54, no. 6, pp. 1913â€“1922, 2005, doi: 10.1109/TVT.2005.858189.

[3] R. Feick, R. A. Valenzuela, and L. Ahumada, â€œExperimental Results on the Level Crossing Rate and Average Fade Duration for Urban Fixed Wireless Channels,â€ IEEE Transactions on Wireless Communications, vol. 6, no. 1, pp. 175â€“179, 2007, doi: 10.1109/TWC.2007.05074.

[10] R. A. Valenzuela, R. Feick, P. Alegre, M. RodrÃ­guez, L. Ahumada, and D. Chizhik, â€œLong Term Fade Margin for 90% Availability in Fixed Wireless Links With Diversity,â€ IEEE Wireless Communications Letters, vol. 9, no. 10, pp. 1648â€“1652, 2020, doi: 10.1109/LWC.2020.2999564.

[5] V. Kolar, S. Razak, P. MÃ¤hÃ¶nen, and N. B. Abu-Ghazaleh, â€œLink Quality Analysis and Measurement in Wireless Mesh Networks,â€ Ad Hoc Networks, vol. 9, no. 8, pp. 1430â€“1447, 2011, doi: 10.1016/j.adhoc.2011.03.005.

[6] J. Mao, Y. Zhao, and Y. Xia, â€œRevisiting Link Quality Metrics and Models for Multichannel Low-Power Lossy Networks,â€ Sensors, vol. 23, no. 3, p. 1303, 2023, doi: 10.3390/s23031303.

[7] â€œAssessing Link Quality in IEEE 802.11 Wireless Networks: Which Is the Right Metric?â€ in Proc. IEEE 19th International Symposium on Personal, Indoor and Mobile Radio Communications (PIMRC), 2008, doi: 10.1109/PIMRC.2008.4699837.

[8] â€œRevisiting Link Quality Metrics for Wireless Sensor Networks,â€ in Proc. 2019 IEEE 5th International Conference on Computer and Communications (ICCC), 2019, doi: 10.1109/ICCC47050.2019.9064098.

[9] â€œFaster or Slower: Convergence of Link Quality Metrics in Wireless Sensor Networks,â€ in Proc. 2020 IEEE 6th International Conference on Computer and Communications (ICCC), 2020, doi: 10.1109/ICCC51575.2020.9345076.





[10] J. Dong and W.-J. Kim, “Experimental Analysis and Implementation of a Multiscale Wireless/Wired Networked Control System,” International Journal of Control, Automation and Systems, vol. 12, pp. 102–110, 2014, doi: 10.1007/s12555-013-9156-2.
