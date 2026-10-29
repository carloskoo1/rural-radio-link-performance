# Reproducibility procedure

## Exact input identification
- Historical CSV: `data/processed/dataset_escenarios_full_day.csv` in repository commit `d2cadaadd66da5184b2df63cc9e4fc6e34ee2ed8`, checksum `ba575ced2bd2d626647e22c1da234e6f78fb9d073879120c24e10bfbe50cc39f`.
- Restricted frozen SQLite: `weather_local_CU01_cierre.sqlite3`, checksum `2fdc7134b6a2b09da3c6370e36cd972a1759ed498eea1a2b04962186d41cccb7`. Source is deliberately absent from GitHub.
- Included campaign schedule: `data/campaign_schedule.csv`, checksum `ba6cb4053afbe6241642e63cf26ed33e0d93ee768784aa88e493449205549780`.

## Software
Python 3.9+ standard library only; SQLite support as shipped with CPython. Independent SQL file is `code/independent_sql_crosscheck.sql`. No network calls or live acquisition connections are used.

## Controlled replay example
Run **only on authorized copies** of the private snapshot, with an output directory different from all source locations:

```bash
python code/reproduce_v5.py \
  --snapshot /secure/frozen/weather_local_CU01_cierre.sqlite3 \
  --schedule data/campaign_schedule.csv \
  --historical /secure/frozen/dataset_escenarios_full_day.csv \
  --sql code/independent_sql_crosscheck.sql \
  --output-dir /different/path/reproduction
```

The program validates source hashes before processing and is intended to open SQLite read-only. It computes E1–E5 gap-aware joint RF events and nominal MCS code changes, plus 18-segment RF and homogeneous TCP summaries. Independently archived outputs and SQL reconciliation evidence reside in `audit/`.

## Independently interpretable public outputs
`Table_S1` = E1–E5 event counts. `Table_S2` = gap-eligibility and day-sensitivity. `Table_S3` = later 18-segment counts, RF and TCP summaries. `Table_S4` = hourly TCP summaries. `figures/Figure_1`–`Figure_4` = the manuscript's derived visualizations.

## Limitations
These materials permit a partial public audit. The complete data-level rerun of the 3×2 experiment requires controlled access to the private SQLite snapshot; do **not** claim fully open reproduction. Different temporal campaigns must never be pooled as if they were interchangeable instruments. Nominal MCS identifiers do not establish an equivalent modulation index across devices, unaccompanied MCS transitions are not independently labeled failures, and short single-stream TCP throughput is not radio PHY capacity. No causal meteorological, acquisition or frequency effect is estimated.
