## 4. Discussion

### 4.1 Configuration dependence extends beyond RSSI

The results show that changing the radio configuration was associated with differences not only in received signal level but also in SNR, MCS, and observed throughput. The Kruskal-Wallis results and epsilon-squared values indicate that the scenario distributions were not interchangeable within the experimental dataset.

An important observation is that the metrics do not move as a single undifferentiated performance variable. E2 presented the highest mean RSSI (-74.396 dBm) and SNR (21.678 dB), but its mean MCS (103.300) and observed throughput (0.588 Mb/s) were not the highest among the scenarios with throughput measurements. Conversely, E4 presented the highest observed throughput mean (0.791 Mb/s) while its mean SNR was 20.616 dB and its mean MCS was 103.672. This divergence indicates that received signal strength alone does not provide a complete description of link performance in the evaluated configurations.

The result supports the central motivation of a beyond-RSSI analysis: a configuration can exhibit favorable signal-level statistics while presenting a different behavior in link adaptation and measured throughput. RSSI should therefore be interpreted as one component of a multidimensional performance state rather than as a sufficient proxy for end-to-end radio-link performance.

### 4.2 Signal quality, link adaptation, and throughput should be interpreted jointly

The observed differences among SNR, MCS, and throughput suggest that the relationship between physical-layer indicators and measured throughput is mediated by link adaptation and by characteristics of the measured traffic path. The present dataset does not establish a mechanistic causal model connecting a specific frequency or bandwidth to a specific MCS state or throughput value. It does show that the distributions of these metrics differ across configurations and that those differences remain statistically detectable.

The contrast between E2 and E4 is particularly relevant. E2 had the highest mean RSSI and SNR, but E4 had the highest observed throughput mean. This prevents a one-dimensional interpretation in which the configuration with the strongest received signal necessarily provides the highest measured throughput. The evidence instead supports joint inspection of received power, signal quality, modulation/coding state, and throughput.

### 4.3 Temporal stability adds information beyond mean performance

The stability analysis demonstrates that average performance and temporal variability describe different properties of a configuration. E3 had an observed-throughput CV of 49.716%, whereas E2 reached 63.839%. At the same time, E4 had the highest mean observed throughput (0.791 Mb/s) but an observed-throughput CV of 54.131%. Consequently, configuration assessment should distinguish expected performance from consistency of that performance.

The composite stability index formalizes this multidimensional comparison by combining normalized variability components from RSSI, SNR, MCS, and observed throughput. The index should be interpreted only as a comparative measure within this experiment because its normalization depends on the evaluated scenario set. It is not an externally calibrated reliability score.

Within E1-E5, the index values range from 0.2302 to 0.9120. This spread demonstrates that configurations can occupy substantially different regions of the variability space. The practical implication is that configuration assessment should consider central tendency and stability as separate dimensions.
### 4.4 Multiscale robustness of the configuration differences

MTRA provides a second dimension of evidence by testing the persistence of configuration-associated differences under temporal aggregation. The epsilon-squared values remain non-negligible at 15, 30, and 60 minutes for all four metrics, and the global tests remain significant at each scale.

The persistence is especially visible for MCS, whose epsilon-squared changes from 0.378 at 15 minutes to 0.457 at 30 minutes and 0.536 at 60 minutes. RSSI changes from 0.425 to 0.452 and 0.480 across the three scales. For observed throughput, epsilon-squared remains close to 0.13 across all scales. These patterns indicate that temporal aggregation does not eliminate the configuration structure present in the data.

MTRA should nevertheless be interpreted as a sensitivity analysis rather than as evidence that longer aggregation windows are intrinsically preferable. Aggregation changes temporal granularity and the number of observations and can alter variance and effect-size estimates. Its value here is that the main configuration differences remain detectable under three predefined temporal resolutions.

### 4.5 Methodological implications for radio-link monitoring

The combined results suggest that monitoring of long-distance point-to-point wireless links should not rely on a single signal indicator. The evaluated evidence supports simultaneous observation of RSSI, SNR, MCS, throughput, and temporal variability.

This does not imply that every deployment requires the same composite index or temporal windows used in this study. Rather, the experiment demonstrates a methodological pattern: configuration evaluation can be strengthened by separating central tendency from variability and by testing whether observed differences persist across temporal aggregation scales.

The repository implementation reinforces this methodological contribution because the statistical evidence, figures, and analysis definitions are versioned as a connected artifact. This allows the reported results to be traced from scenario-level data products to publication figures.

### 4.6 Limitations and threats to interpretation

Several limitations delimit the interpretation of the findings.

First, the experiment concerns one long-distance point-to-point link and therefore does not establish that the observed configuration patterns generalize to other links, terrains, antenna systems, radio platforms, or propagation conditions.

Second, the six scenarios were evaluated sequentially over different calendar periods. Although this reflects the field nature of the experiment, calendar-period effects and configuration effects cannot be completely separated by the current design. Accordingly, the manuscript uses configuration-associated language rather than attributing the observed differences exclusively to frequency or channel bandwidth.

Third, observed throughput is unavailable for E0 in a form directly comparable with E1-E5. E0 is therefore excluded from throughput comparisons and from the four-component publication stability index. This restriction should remain explicit in the article.

Fourth, the composite stability index is internally normalized across the evaluated scenarios. Its numerical scale should not be interpreted as a universal engineering threshold.

Finally, the current publication branch reproduces the frozen statistical outputs used to generate the article figures, but the publication generator itself does not independently recompute every upstream statistical test from raw observations. Full analytical reproducibility therefore depends on the upstream thesis pipeline and its audit. This distinction is documented in the repository and should remain visible in the final manuscript.

### 4.7 Implications for future experiments

The present evidence suggests several directions for a stronger subsequent experimental design. Repeated alternation among configurations within shorter controlled blocks would reduce confounding between configuration and calendar period. Replication across additional links and environmental conditions would provide evidence about external validity. A future campaign could also preserve synchronized throughput measurements for every configuration, including the baseline, allowing the stability index to be evaluated on a common metric set.

These extensions define the experimental steps needed to distinguish more strongly between configuration effects and time-varying field conditions.
