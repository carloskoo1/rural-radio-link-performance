# Introduction and Related Work draft — Beyond RSSI

## 1. Introduction

Long-distance point-to-point wireless links are frequently monitored through a small set of radio indicators, among which received signal strength is one of the most accessible. RSSI is useful for diagnosing gross changes in received power and for verifying link conditions, but a single signal-strength statistic does not necessarily describe the complete operational state of a wireless link. Experimental studies have shown that wireless-link behavior depends on the interaction among signal quality, modulation and coding, traffic conditions, and temporal channel dynamics. For example, measurements of IEEE 802.11ad have evaluated RSSI together with MCS and TCP/UDP throughput rather than treating received signal strength as a complete performance descriptor. [1]

This distinction becomes relevant in fixed outdoor links because a configuration that produces a favorable received-power level may not produce the same behavior at the modulation/coding or throughput layers. The physical and link layers are coupled through adaptive modulation and coding, while the delivered throughput also depends on protocol and traffic behavior. Consequently, radio-link assessment benefits from observing multiple layers of telemetry rather than relying on a single radio-strength indicator.

Temporal behavior introduces a second dimension to this problem. Fixed wireless channels can exhibit time-varying behavior and fade dynamics even when the physical endpoints remain stationary. Measurement studies of fixed wireless links have therefore examined the temporal stability of received signals and the occurrence of fades over time. [2] More recent experimental work in wireless networking likewise treats temporal stability as a relevant performance dimension rather than considering only average throughput or instantaneous link quality. [3]

A further methodological question concerns temporal aggregation. A difference observed at a fine time scale may weaken or disappear after aggregation, whereas a persistent configuration-associated difference may remain detectable at multiple temporal resolutions. Multiscale analysis is established in temporal-network research, although its objectives and methods vary substantially across application domains. [4] In wireless systems, recent experimental studies have also compared performance under different temporal windows to determine whether observed behavior is robust to aggregation. [5]

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

Multiscale analysis is used in several areas of network science to characterize dynamics that depend on the temporal or structural scale at which observations are examined. Temporal-network research has demonstrated that conclusions about dynamic network behavior can depend on the temporal scale used for analysis. [4]

In wireless experimental research, changing the aggregation window can similarly affect variance, sample size, and the apparent persistence of performance differences. Recent experimental work with wireless sensor systems, for example, has explicitly compared multiple aggregation windows and examined whether qualitative performance relationships remain stable as temporal resolution changes. [5]

The present study uses this principle as a sensitivity analysis rather than as a predictive model. MTRA does not attempt to forecast future link states or infer a universal temporal scale. Instead, it asks whether configuration-associated differences detected in the field telemetry remain statistically detectable at three predefined temporal resolutions.

### 2.5 Research gap

The reviewed literature establishes four relevant facts: (i) RSSI is useful but does not fully represent wireless performance; (ii) SNR, MCS, and throughput provide complementary information; (iii) temporal stability is a relevant property of fixed and mobile wireless systems; and (iv) temporal aggregation can affect the interpretation of dynamic network measurements. [1]-[8]

The remaining gap addressed by this study is therefore not the absence of any individual metric or statistical method. Rather, it is the integration of these dimensions into a single empirical assessment of a real long-distance point-to-point link under controlled configuration changes. The study combines multidimensional performance characterization, explicit temporal-stability analysis, and multiscale sensitivity testing within the same field experiment, while preserving the resulting evidence in a version-controlled reproducibility pipeline.

This framing deliberately avoids claiming methodological priority for MTRA or novelty for the individual statistical tests. The contribution lies in the experimental integration and evidence structure applied to the specific problem of configuration-dependent long-distance radio-link assessment.

