# Immutable evidence and acquisition provenance

## A. Historical platform reports

- Fixed existing repository commit: `d2cadaadd66da5184b2df63cc9e4fc6e34ee2ed8`.
- Source: `data/processed/dataset_escenarios_full_day.csv`; Git blob `5617f651af6fdc980c85efe71d040d9eafa4c152`.
- Original file 3,715,410 bytes; SHA-256 `ba575ced2bd2d626647e22c1da234e6f78fb9d073879120c24e10bfbe50cc39f`.
- Original source 26,107 rows across all periods; selected E1–E5 = 11,707 rows; 11,544 valid joint RSSI/SNR records.
- Periods (MHz/width MHz): E1 5660/40, E2 5660/80, E3 5730/40, E4 5730/80, E5 5805/40.
- Pair validity: both finite plausible downlink RSSI/SNR, gap not exceeding 600 s, no cross-period pairing, no skipped invalid records.
- Separate sensitivity: 450/600/900 s maximum gaps; leave-one-day-out; exact within-day state-frequency reference.

## B. Repeated 3×2 RF and TCP experiment (separately acquired)

- Radio path: Cuñacales ↔ San José, Cajamarca, approximately 12–12.5 km; one physical route.
- Campaign dates: 2026-09-15 through 2026-10-26 inclusive; analysis cutoff 2026-10-27 00:00 at UTC−05:00.
- Three nominal frequencies: 6475, 6655 and 7000 MHz; channel widths 20 and 40 MHz; **18 scheduled temporal segments**, three applications per configuration.
- Frozen private database: `weather_local_CU01_cierre.sqlite3`, 1,773,711,360 bytes, SHA-256 `2fdc7134b6a2b09da3c6370e36cd972a1759ed498eea1a2b04962186d41cccb7`.
- Frozen experimental schedule SHA-256 `ba6cb4053afbe6241642e63cf26ed33e0d93ee768784aa88e493449205549780`.
- Source campaign: 11,813 RF rows; 7,143 TCP attempts, of which 7,070 had status OK and 73 ERROR.
- RF result: 11,412 configuration-concordant dual-operational rows; 11,367 eligible adjacent pairs; 4,769 unchanged joint RSSI/SNR pairs; 2,748 nominal MCS transitions; 1,038 without concurrent joint RF transition.
- TCP: 6,834 eligible one-stream 8-second/omit-1 tests, with 3,419 DL and 3,415 UL; 300 s maximum RF association, observed eligible maximum 296 s, median 144 s. One initial 6655/20 segment has no comparable main-protocol throughput.
- Reported UTC−05:00 and UTC timestamps reconciled; source RF timestamps matched stored associations. These are checks of archived timestamps, not independent NTP calibration.
- All 11,412 eligible AP payloads matched source field labels for nominal DL/UL MCS and DL RSSI/SNR. Firmwares reported AP 5.4 and SM 5.4.0 in these records. Codes are nominal; do not compare them as modulation scalars to historical hardware.
- Archived independent Python and SQL count reconciliations, SQLite immutable read-only `quick_check`, and source-hash checks are represented in `audit/`. The audit artifacts are records of prior execution, not a claim that this GitHub upload reran inaccessible raw data.

**Article participation boundary:** The six named UNC authors are the research team of the present article. The corresponding author confirms that Luisita Adalid Mendo Urbina did not participate in the current manuscript/research. This correction does not modify the acquired 3×2 dataset or resolve historical participation in other research; those records remain independent.

## C. Comparability and inferential limits

Single physical route, sequential interventions, dissimilar instrumentation periods, repeated nested measurements, incomplete coverage and no independently adjudicated failure outcomes. The descriptive 7000/20 MHz deterioration is concordant in reported RF and TCP but is not a missed-alarm case. Do not infer causal effects of weather, frequency, firmware, or acquisition regime; no diagnostics sensitivity/specificity is estimated. TCP results are application-layer tests constrained in part by a reported 100 Mb/s Ethernet link and must not be labeled PHY capacity.

**Source-of-truth rule:** modify neither the original historical commit nor the frozen private database. Every public revision receives its own new SHA and manifest.
