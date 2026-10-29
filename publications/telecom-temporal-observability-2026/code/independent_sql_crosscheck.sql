-- Parse-checked against a synthetic SQLite schema and one eligible paired fixture.
-- Query real data ONLY against the documented frozen read-only snapshot; do NOT open the live collector database.
-- Retrospective 3x2 event-accounting reproduction. SELECT only; run with sqlite3 -readonly against frozen snapshot.
-- Do not run on the live acquisition database. Match date intervals and status as documented in campaign_schedule.csv.
WITH s(seq,f,b,t0,t1) AS (VALUES (1,6655,20,'2026-09-15T00:00:00-05:00','2026-09-18T00:00:00-05:00'),
(2,7000,40,'2026-09-18T00:00:00-05:00','2026-09-21T00:00:00-05:00'),
(3,6475,20,'2026-09-21T00:00:00-05:00','2026-09-24T00:00:00-05:00'),
(4,6655,40,'2026-09-24T00:00:00-05:00','2026-09-27T00:00:00-05:00'),
(5,6475,40,'2026-09-27T00:00:00-05:00','2026-09-30T00:00:00-05:00'),
(6,7000,20,'2026-09-30T00:00:00-05:00','2026-10-03T00:00:00-05:00'),
(7,7000,40,'2026-10-03T00:00:00-05:00','2026-10-05T00:00:00-05:00'),
(8,6655,40,'2026-10-05T00:00:00-05:00','2026-10-07T00:00:00-05:00'),
(9,6655,20,'2026-10-07T00:00:00-05:00','2026-10-09T00:00:00-05:00'),
(10,6475,40,'2026-10-09T00:00:00-05:00','2026-10-11T00:00:00-05:00'),
(11,6475,20,'2026-10-11T00:00:00-05:00','2026-10-13T00:00:00-05:00'),
(12,7000,20,'2026-10-13T00:00:00-05:00','2026-10-15T00:00:00-05:00'),
(13,6475,40,'2026-10-15T00:00:00-05:00','2026-10-17T00:00:00-05:00'),
(14,6655,20,'2026-10-17T00:00:00-05:00','2026-10-19T00:00:00-05:00'),
(15,6655,40,'2026-10-19T00:00:00-05:00','2026-10-21T00:00:00-05:00'),
(16,7000,20,'2026-10-21T00:00:00-05:00','2026-10-23T00:00:00-05:00'),
(17,6475,20,'2026-10-23T00:00:00-05:00','2026-10-25T00:00:00-05:00'),
(18,7000,40,'2026-10-25T00:00:00-05:00','2026-10-27T00:00:00-05:00')),
r AS (
 SELECT s.seq,a.timestamp_local,a.id,a.dl_rssi_dbm AS rssi,a.dl_snr_db AS snr,a.dl_mcs AS mcs
 FROM radio_link_config_telemetry a JOIN s ON a.timestamp_local>=s.t0 AND a.timestamp_local<s.t1
 WHERE a.collection_status='LINK_OPERATIONAL_DUAL'
  AND a.operating_frequency_mhz=s.f AND a.sm_operating_frequency_mhz=s.f
  AND a.channel_bandwidth_mhz=s.b AND a.sm_channel_bandwidth_mhz=s.b
),
q AS (SELECT *,LAG(timestamp_local) OVER(PARTITION BY seq ORDER BY timestamp_local,id) AS prev_ts,
 LAG(rssi) OVER(PARTITION BY seq ORDER BY timestamp_local,id) AS prev_rssi,
 LAG(snr) OVER(PARTITION BY seq ORDER BY timestamp_local,id) AS prev_snr,
 LAG(mcs) OVER(PARTITION BY seq ORDER BY timestamp_local,id) AS prev_mcs FROM r),
z AS (SELECT *,CASE WHEN rssi>-120 AND rssi<-10 AND snr IS NOT NULL
 AND prev_rssi>-120 AND prev_rssi<-10 AND prev_snr IS NOT NULL
 AND prev_ts IS NOT NULL AND unixepoch(timestamp_local)-unixepoch(prev_ts) BETWEEN 1 AND 600
 THEN 1 ELSE 0 END AS pair_ok FROM q)
SELECT seq,COUNT(*) AS dual_rows,
COUNT(DISTINCT CASE WHEN rssi>-120 AND rssi<-10 AND snr IS NOT NULL THEN printf('%.2f/%.2f',rssi,snr) END) AS distinct_rf_states,
SUM(pair_ok) AS eligible_pairs,
SUM(CASE WHEN pair_ok=1 AND rssi=prev_rssi AND snr=prev_snr THEN 1 ELSE 0 END) AS stable_pairs,
SUM(CASE WHEN pair_ok=1 AND mcs IS NOT NULL AND prev_mcs IS NOT NULL THEN 1 ELSE 0 END) AS mcs_comparable_pairs,
SUM(CASE WHEN pair_ok=1 AND mcs IS NOT NULL AND prev_mcs IS NOT NULL AND mcs!=prev_mcs THEN 1 ELSE 0 END) AS mcs_change_pairs,
SUM(CASE WHEN pair_ok=1 AND mcs IS NOT NULL AND prev_mcs IS NOT NULL AND mcs!=prev_mcs AND rssi=prev_rssi AND snr=prev_snr THEN 1 ELSE 0 END) AS hidden_mcs,
COUNT(DISTINCT mcs) AS nominal_mcs_states
FROM z GROUP BY seq ORDER BY seq;


-- Independent TCP eligibility count using the same segment schedule and RF configuration checks.
-- Distinct from the original 7,070 status=OK attempts: stricter matching retains 6,834 tests.
WITH s(seq,f,b,t0,t1) AS (VALUES (1,6655,20,'2026-09-15T00:00:00-05:00','2026-09-18T00:00:00-05:00'),
(2,7000,40,'2026-09-18T00:00:00-05:00','2026-09-21T00:00:00-05:00'),
(3,6475,20,'2026-09-21T00:00:00-05:00','2026-09-24T00:00:00-05:00'),
(4,6655,40,'2026-09-24T00:00:00-05:00','2026-09-27T00:00:00-05:00'),
(5,6475,40,'2026-09-27T00:00:00-05:00','2026-09-30T00:00:00-05:00'),
(6,7000,20,'2026-09-30T00:00:00-05:00','2026-10-03T00:00:00-05:00'),
(7,7000,40,'2026-10-03T00:00:00-05:00','2026-10-05T00:00:00-05:00'),
(8,6655,40,'2026-10-05T00:00:00-05:00','2026-10-07T00:00:00-05:00'),
(9,6655,20,'2026-10-07T00:00:00-05:00','2026-10-09T00:00:00-05:00'),
(10,6475,40,'2026-10-09T00:00:00-05:00','2026-10-11T00:00:00-05:00'),
(11,6475,20,'2026-10-11T00:00:00-05:00','2026-10-13T00:00:00-05:00'),
(12,7000,20,'2026-10-13T00:00:00-05:00','2026-10-15T00:00:00-05:00'),
(13,6475,40,'2026-10-15T00:00:00-05:00','2026-10-17T00:00:00-05:00'),
(14,6655,20,'2026-10-17T00:00:00-05:00','2026-10-19T00:00:00-05:00'),
(15,6655,40,'2026-10-19T00:00:00-05:00','2026-10-21T00:00:00-05:00'),
(16,7000,20,'2026-10-21T00:00:00-05:00','2026-10-23T00:00:00-05:00'),
(17,6475,20,'2026-10-23T00:00:00-05:00','2026-10-25T00:00:00-05:00'),
(18,7000,40,'2026-10-25T00:00:00-05:00','2026-10-27T00:00:00-05:00')),
r AS (
 SELECT s.seq,a.id FROM radio_link_config_telemetry a JOIN s
 ON a.timestamp_local>=s.t0 AND a.timestamp_local<s.t1
 WHERE a.collection_status='LINK_OPERATIONAL_DUAL'
 AND a.operating_frequency_mhz=s.f AND a.sm_operating_frequency_mhz=s.f
 AND a.channel_bandwidth_mhz=s.b AND a.sm_channel_bandwidth_mhz=s.b
),
t AS (
 SELECT s.seq,x.direction,x.measured_throughput_mbps AS mbps
 FROM active_throughput_6g x JOIN s
 ON x.timestamp_start_local>=s.t0 AND x.timestamp_start_local<s.t1
 JOIN r ON r.id=x.rf_telemetry_id AND r.seq=s.seq
 WHERE x.campaign_id='CAMPAIGN_6G_20260831'
 AND x.status='OK' AND x.protocol='TCP'
 AND x.duration_seconds=8 AND x.omit_seconds=1 AND x.parallel_streams=1
 AND x.operating_frequency_mhz=s.f AND x.channel_bandwidth_mhz=s.b
 AND abs(x.rf_time_delta_seconds)<=300 AND x.rf_time_delta_seconds IS NOT NULL
 AND x.measured_throughput_mbps>=0 AND x.direction IN ('DL','UL')
)
SELECT seq,SUM(direction='DL') AS dl_matched,SUM(direction='UL') AS ul_matched
 FROM t GROUP BY seq ORDER BY seq;
