# Temporal Observability of Wireless Backhaul — research reproducibility archive

**Manuscript:** *Temporal Observability of Wireless Backhaul: Evidence from Two High-Andean RF and TCP Field Campaigns*.
**Target journal:** Telecom (MDPI). **Archive status:** 2026-10-28 pre-submission reproducibility package; no journal acceptance, publication or DOI is implied. **Release:** v1.0.0-rc1.

This archive documents two observational data collections on **one high-Andean point-to-point link** between Cuñacales and San José, Cajamarca, Peru. The historical E1–E5 telemetry periods and later repeated 3×2 RF/TCP campaign were acquired in different periods and instrumentation contexts. They are **not independent spatial replicas**; their descriptive percentages are not estimates of a causal acquisition effect.

## Scientific endpoints and verified summaries

1. Historical E1–E5: 11,707 source rows; 11,544 valid joint downlink RSSI/SNR observations. E4 adjacent joint-RF persistence = **2146/2155 (99.58%)**; 1352/1361 (99.34%) nominal MCS changes lacked a concurrent joint RF transition.
2. Later 3×2 campaign: **18 segments**, 11,412 configuration-concordant RF records, 11,367 eligible adjacent pairs; 4769 unchanged joint RF pairs (**41.95%**); 1038/2748 nominal MCS changes unaccompanied by joint RF transitions (**37.77%**).
3. Active TCP: 6,834 eligible tests (3,419 downlink, 3,415 uplink). 7000 MHz/20 MHz repeated segment downlink summaries: 63.66, 60.63 and 21.40 Mb/s, with lower reported RSSI/SNR in the third repetition. These are *medians of hourly medians*, not radio PHY capacity or causal frequency effects.

## Repository map

| Directory/file | Contents |
|---|---|
| `code/reproduce_v5.py` | Standard-library Python reference implementation (frozen, read-only source inputs) |
| `code/independent_sql_crosscheck.sql` | Read-only SQL crosscheck; no live-database modification |
| `data/Table_S1_historical_reproduced.csv` | Historical state-event counts |
| `data/Table_S2_historical_sensitivity.csv` | Historical gap and leave-one-day-out sensitivity |
| `data/Table_S3_campaign_18_segments_reproduced.csv` | Segment RF/MCS/TCP eligible counts and summaries |
| `data/Table_S4_hourly_TCP.csv` | Hourly TCP summary values |
| `data/campaign_schedule.csv` | Frozen 18-segment schedule |
| `audit/` | Reconciliation, rounding and independently archived comparisons |
| `figures/` | Figures 1–4 in the manuscript |
| `PROVENANCE.md` | Source dataset commit, private snapshot hashes, definition of analytic populations |
| `DATA_ACCESS.md` | Public versus restricted-data boundaries |
| `REPRODUCE.md` | Reproduction steps, validation and limitations |
| `AUTHORS.md`, `AUTHOR_BIOGRAPHIES.md` | Authorship order, institutional contacts and academic biographies |
| `CONTRIBUTIONS_CREDIT_PENDING.md` | CRediT roles intentionally pending individual author confirmation |
| `FUNDING_AND_DISCLOSURES.md` | Research ownership, financing and disclosure status |
| `SHA256SUMS.txt` and `release_manifest.json` | Immutable artifact checksums and source manifest |

## Provenance

**Dataset A** remains stored at the existing [fixed historical source commit](https://github.com/carloskoo1/rural-radio-link-performance/tree/d2cadaadd66da5184b2df63cc9e4fc6e34ee2ed8), file `data/processed/dataset_escenarios_full_day.csv`. Original source SHA-256: `ba575ced2bd2d626647e22c1da234e6f78fb9d073879120c24e10bfbe50cc39f`.

**Dataset B** is a *restricted* frozen 1,773,711,360-byte SQLite snapshot with SHA-256 `2fdc7134b6a2b09da3c6370e36cd972a1759ed498eea1a2b04962186d41cccb7`. It is **not deposited**; no full open-source replay without authorized data access is asserted. See `DATA_ACCESS.md`.

## Reproduction and scope

Run `python code/reproduce_v5.py --help`; see `REPRODUCE.md` for a command using separately supplied frozen input copies. Treat nominal MCS states as categorical codes, never comparable numerical modulation indexes across firmwares. Adjacent RF reports must meet validity and maximum-gap rules. RF-to-TCP matching uses an allowed gap of up to 300 s; it is not simultaneous radio sampling.

**Do not add private source SQLite, device payloads, administration IPs, credentials, or any data from the separate prospective campaign.** See `SECURITY.md`. No reuse license is asserted for the whole dataset pending explicit rights clearance. Cite the exact commit SHA for future scientific claims; a mutable branch URL is not a permanent version identifier.

## Authors

Carlos J. Koo Labrín (corresponding author); Néstor E. Muñoz Abanto; Víctor Sánchez Cáceres; Marisol Tapia Romero; José Camilo Micha Ortiz; Rosel Burga Cabrera. All are faculty of Universidad Nacional de Cajamarca and participants in the Advanced Telecommunications Laboratory. Their institutional contacts are documented in `AUTHORS.md`. Luisita Adalid Mendo Urbina is acknowledged for the original 3×2 thesis field campaign and stewardship; individual authorship criteria and CRediT assignment remain subject to review.
