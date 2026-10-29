#!/usr/bin/env python3
"""Reproduce two retrospective telemetry datasets from fixed sources, read only.

No network requests, live databases, model fitting, or prospective observations.
Python >=3.9, standard library only. Supply the frozen V4 SQL for cross-checking.
"""
import argparse
import collections as co
import csv
import datetime as dt
import hashlib
import json
import math
import pathlib
import sqlite3
import statistics as st
import sys

EXPECTED_DB='2fdc7134b6a2b09da3c6370e36cd972a1759ed498eea1a2b04962186d41cccb7'
EXPECTED_HIST='ba575ced2bd2d626647e22c1da234e6f78fb9d073879120c24e10bfbe50cc39f'
EXPECTED_SCHEDULE='ba6cb4053afbe6241642e63cf26ed33e0d93ee768784aa88e493449205549780'
CAMP='CAMPAIGN_6G_20260831'

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()

def number(v):
    try:
        x=float(v)
        return x if math.isfinite(x) else None
    except (TypeError,ValueError):return None

def time(v):
    x=dt.datetime.fromisoformat(v)
    if x.tzinfo is None:raise ValueError('Timestamp without UTC offset')
    return x

def rf_ok(x):
    return x['_s'][0] is not None and -120<x['_s'][0]<-10 and x['_s'][1] is not None

def median(v):return st.median(v) if v else None
def pct(a,b):return 100*a/b if b else None

def hist_stats(a,gap=600):
    valid=[r for r in a if rf_ok(r)]
    pairs=[(p,q) for p,q in zip(a,a[1:]) if rf_ok(p) and rf_ok(q) and 0<=(q['_t']-p['_t']).total_seconds()<=gap]
    static=[(p,q) for p,q in pairs if p['_s']==q['_s']]
    comp=[(p,q) for p,q in pairs if p['_m'] is not None and q['_m'] is not None]
    compstatic=[(p,q) for p,q in comp if p['_s']==q['_s']]
    changes=[(p,q) for p,q in comp if p['_m']!=q['_m']]
    hidden=[(p,q) for p,q in changes if p['_s']==q['_s']]
    daily=co.defaultdict(co.Counter)
    for r in valid:daily[r['_t'].date()][r['_s']]+=1
    # Exact conditional expectation under independent within-day permutations
    # of valid state labels over their fixed, valid timestamp positions.
    expected=0
    for p,q in pairs:
        d,e=p['_t'].date(),q['_t'].date();c,dst=daily[d],daily[e]
        n,m=sum(c.values()),sum(dst.values())
        if d==e:expected+=sum(k*(k-1) for k in c.values())/(n*(n-1)) if n>1 else 0
        else:expected+=sum(k*dst.get(s,0) for s,k in c.items())/(n*m)
    best=(0,0);run=0;start=None;prev=None
    for r in a:
        if not rf_ok(r):run=0;start=None;prev=None;continue
        if prev is not None and r['_s']==prev['_s'] and 0<=(r['_t']-prev['_t']).total_seconds()<=gap:run+=1
        else:run=1;start=r['_t']
        hours=(r['_t']-start).total_seconds()/3600
        if run>best[0]:best=(run,hours)
        prev=r
    traffic=[(number(p['throughput_dl']),number(q['throughput_dl'])) for p,q in static]
    traffic=[(p,q) for p,q in traffic if p is not None and q is not None]
    uplink=[(number(p['rssi_ul']),number(q['rssi_ul'])) for p,q in static]
    uplink=[(p,q) for p,q in uplink if p is not None and q is not None]
    return dict(source_rows=len(a),valid_joint_rf=len(valid),distinct_joint_rf_states=len(set(r['_s'] for r in valid)),
        eligible_adjacent_pairs=len(pairs),unchanged_adjacent_pairs=len(static),unchanged_adjacent_pct=pct(len(static),len(pairs)),
        rf_state_transitions=len(pairs)-len(static),mcs_comparable_pairs=len(comp),mcs_comparable_static_pairs=len(compstatic),
        mcs_change_pairs=len(changes),mcs_changes_during_constant_rf=len(hidden),H_pct=pct(len(hidden),len(changes)),D_pct=pct(len(hidden),len(compstatic)),
        exact_within_day_permutation_reference_pct=pct(expected,len(pairs)),longest_censored_run_n=best[0],longest_censored_run_hours=best[1],
        traffic_comparable=len(traffic),traffic_delta_ge_0p10=sum(abs(q-p)>=0.10 for p,q in traffic),
        ul_rssi_comparable=len(uplink),ul_rssi_delta_ge_1=sum(abs(q-p)>=1 for p,q in uplink),
        first=valid[0]['timestamp'],last=valid[-1]['timestamp'],days=len(daily))

def historical(p):
    allrows=list(csv.DictReader(p.open(encoding='utf-8-sig')))
    result=[];sensitivity=[]
    for scen in ('E1','E2','E3','E4','E5'):
        a=[r for r in allrows if r['escenario']==scen]
        for r in a:r['_t']=time(r['timestamp']);r['_s']=(number(r['rssi_dl']),number(r['snr_dl']));r['_m']=number(r['mcs_dl'])
        a.sort(key=lambda r:r['_t']);s=hist_stats(a);s['scenario']=scen;result.append(s)
        for gap in (450,600,900):sensitivity.append(dict(scenario=scen,gap_seconds=gap,**hist_stats(a,gap)))
        if scen=='E4':
            lod=[hist_stats([r for r in a if r['_t'].date()!=d]) for d in sorted({r['_t'].date() for r in a})]
    return result,sensitivity,dict(source_rows_all=len(allrows),E4_leave_day_out_P_pct=[min(r['unchanged_adjacent_pct'] for r in lod),max(r['unchanged_adjacent_pct'] for r in lod)],E4_leave_day_out_H_pct=[min(r['H_pct'] for r in lod),max(r['H_pct'] for r in lod)])

def write_csv(p,rows):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for a in ('snapshot','schedule','historical','sql','output_dir'):p.add_argument('--'+a.replace('_','-'),type=pathlib.Path,required=True)
    args=p.parse_args();db=args.snapshot.resolve(strict=True);schedule=args.schedule.resolve(strict=True);hist=args.historical.resolve(strict=True);sql=args.sql.resolve(strict=True);out=args.output_dir.resolve()
    if out==db.parent or db.parent in out.parents:raise ValueError('Output cannot be inside the frozen-source directory')
    out.mkdir(parents=True,exist_ok=True)
    hashes=dict(snapshot_sha256=sha(db),schedule_sha256=sha(schedule),historical_sha256=sha(hist))
    assert list(hashes.values())==[EXPECTED_DB,EXPECTED_SCHEDULE,EXPECTED_HIST],hashes
    hr,hs,ha=historical(hist)
    write_csv(out/'historical_reproduced.csv',hr);write_csv(out/'historical_sensitivity.csv',hs)
    segs=[]
    for s in csv.DictReader(schedule.open(encoding='utf-8-sig')):
        if s['phase']=='EXPERIMENT':segs.append(dict(seq=int(s['sequence']),f=float(s['frequency_mhz']),b=float(s['bandwidth_mhz']),start=time(s['start_local']),end=time(s['end_local']),scenario=s['scenario_id']))
    assert len(segs)==18
    def segment(t):return next((s for s in segs if s['start']<=t<s['end']),None)
    c=sqlite3.connect(db.as_uri()+'?mode=ro&immutable=1',uri=True);c.row_factory=sqlite3.Row;c.execute('pragma query_only=on')
    quick=c.execute('pragma quick_check(1)').fetchone()[0];assert quick=='ok'
    rfcols='id,timestamp_utc,timestamp_local,collection_status,operating_frequency_mhz,sm_operating_frequency_mhz,channel_bandwidth_mhz,sm_channel_bandwidth_mhz,dl_rssi_dbm,dl_snr_db,dl_mcs,ul_mcs,ul_rssi_dbm,ul_snr_db'
    allrf=[dict(r) for r in c.execute('select '+rfcols+' from radio_link_config_telemetry order by timestamp_local,id')]
    rfbyid={r['id']:r for r in allrf};dual=co.defaultdict(list);rawrf=[]
    def concordant(r,s):return r['collection_status']=='LINK_OPERATIONAL_DUAL' and r['operating_frequency_mhz']==r['sm_operating_frequency_mhz']==s['f'] and r['channel_bandwidth_mhz']==r['sm_channel_bandwidth_mhz']==s['b']
    def clock_stats(rows,local,utc):
        diffs=[abs((time(r[local])-time(r[utc])).total_seconds()) for r in rows]
        return dict(rows=len(rows),local_offsets=dict(co.Counter(str(time(r[local]).utcoffset()) for r in rows)),max_utc_local_difference_s=max(diffs),difference_gt_1s=sum(v>1 for v in diffs))
    for r in allrf:
        r['_t']=time(r['timestamp_local']);s=segment(r['_t'])
        if s:
            rawrf.append(r);r['_seg']=s['seq']
            if concordant(r,s):dual[s['seq']].append(r)
    tcpcols='id,campaign_id,timestamp_start_local,timestamp_start_utc,timestamp_end_local,timestamp_end_utc,rf_telemetry_id,rf_timestamp_local,rf_time_delta_seconds,direction,status,protocol,duration_seconds,omit_seconds,parallel_streams,measured_throughput_mbps,operating_frequency_mhz,channel_bandwidth_mhz'
    tcp=[dict(r) for r in c.execute('select '+tcpcols+' from active_throughput_6g order by timestamp_start_local,id') if segment(time(r['timestamp_start_local']))]
    exclusions=co.Counter();selected=[];join=co.Counter();delta_max=0;copy_mismatch=0
    delta_hist=co.Counter();eligible_delta=[];hourly=co.defaultdict(list)
    strata=co.Counter((r['campaign_id'],r['status'],r['protocol']) for r in tcp)
    for r in tcp:
        t=time(r['timestamp_start_local']);s=segment(t);r['_seg']=s['seq'];source=rfbyid.get(r['rf_telemetry_id'])
        if source:
            join['linked_rf_rows']+=1
            recomputed=abs((time(r['timestamp_start_utc'])-time(source['timestamp_utc'])).total_seconds())
            recorded=number(r['rf_time_delta_seconds']);err=None if recorded is None else abs(recorded-recomputed)
            if err is not None:delta_max=max(delta_max,err);delta_hist[err]+=1
            if recorded is None or err>1:join['delta_difference_gt_1s_or_missing']+=1
            if r['rf_timestamp_local']!=source['timestamp_local']:copy_mismatch+=1
        else:join['missing_linked_rf']+=1
        reason=None
        if r['campaign_id']!=CAMP:reason='campaign_id'
        elif r['status']!='OK':reason='unsuccessful_status'
        elif r['protocol']!='TCP':reason='not_tcp'
        elif (r['duration_seconds'],r['omit_seconds'],r['parallel_streams'])!=(8,1,1):reason='nonhomogeneous_protocol'
        elif (r['operating_frequency_mhz'],r['channel_bandwidth_mhz'])!=(s['f'],s['b']):reason='tcp_configuration'
        elif source is None or source.get('_seg')!=s['seq'] or not concordant(source,s):reason='rf_configuration_or_segment'
        elif number(r['rf_time_delta_seconds']) is None or abs(r['rf_time_delta_seconds'])>300:reason='rf_delta_gt_300s_or_missing'
        elif r['direction'] not in ('DL','UL'):reason='direction'
        elif number(r['measured_throughput_mbps']) is None or r['measured_throughput_mbps']<0:reason='throughput'
        elif recomputed>300:reason='recomputed_delta_gt_300s'
        if reason:exclusions[reason]+=1;continue
        r['_recomputed_delta']=recomputed;selected.append(r);eligible_delta.append(recomputed)
        hourly[(s['seq'],r['direction'],t.strftime('%Y-%m-%dT%H'))].append(r['measured_throughput_mbps'])
    sr=[]
    for s in segs:
        a=dual[s['seq']];pairs=[]
        for r in a:r['_s']=(r['dl_rssi_dbm'],r['dl_snr_db'])
        for p0,q in zip(a,a[1:]):
            if 0<(q['_t']-p0['_t']).total_seconds()<=600 and rf_ok(p0) and rf_ok(q):pairs.append((p0,q))
        static=[(p0,q) for p0,q in pairs if p0['_s']==q['_s']]
        comp=[(p0,q) for p0,q in pairs if p0['dl_mcs'] is not None and q['dl_mcs'] is not None]
        changes=[(p0,q) for p0,q in comp if p0['dl_mcs']!=q['dl_mcs']]
        hidden=[(p0,q) for p0,q in changes if p0['_s']==q['_s']]
        z=dict(segment=s['seq'],scenario=s['scenario'],frequency_mhz=s['f'],bandwidth_mhz=s['b'],rf_rows=len(a),rf_pairs=len(pairs),rf_static_pairs=len(static),rf_static_pct=pct(len(static),len(pairs)),mcs_comparable=len(comp),mcs_transitions=len(changes),mcs_unaccompanied=len(hidden),H_pct=pct(len(hidden),len(changes)))
        for d in ('DL','UL'):
            v=[st.median(values) for (seq,direction,h),values in hourly.items() if seq==s['seq'] and direction==d]
            z['tcp_'+d.lower()+'_count']=sum(r['_seg']==s['seq'] and r['direction']==d for r in selected)
            z['tcp_'+d.lower()+'_valid_hours']=len(v);z['tcp_'+d.lower()+'_median_hourly_medians']=median(v)
        rf_hours=co.defaultdict(list)
        for r in a:rf_hours[r['_t'].strftime('%Y-%m-%dT%H')].append(r)
        for k in ('dl_rssi_dbm','ul_rssi_dbm','dl_snr_db','ul_snr_db'):
            z[k+'_median_hourly_medians']=median([st.median([r[k] for r in v if number(r[k]) is not None]) for v in rf_hours.values() if any(number(r[k]) is not None for r in v)])
        sr.append(z)
    # Cross-check Python event counts against the independent frozen V4 SQL.
    sql_results=[]
    sql_text='\n'.join(line for line in sql.read_text().splitlines() if not line.lstrip().startswith('--'))
    for statement in sql_text.split(';'):
        if 'SELECT' in statement.upper():sql_results.append([dict(x) for x in c.execute(statement)])
    assert len(sql_results)==2
    mapping={'dual_rows':'rf_rows','eligible_pairs':'rf_pairs','stable_pairs':'rf_static_pairs','mcs_comparable_pairs':'mcs_comparable','mcs_change_pairs':'mcs_transitions','hidden_mcs':'mcs_unaccompanied'}
    for r in sql_results[0]:
        z=next(z for z in sr if z['segment']==r['seq'])
        for a,b in mapping.items():assert r[a]==z[b],(r['seq'],a,r[a],z[b])
    for r in sql_results[1]:
        z=next(z for z in sr if z['segment']==r['seq'])
        assert (r['dl_matched'],r['ul_matched'])==(z['tcp_dl_count'],z['tcp_ul_count'])
    fields={'dl_mcs':'connectedSTADLMCS','ul_mcs':'connectedSTAULMCS','dl_rssi_dbm':'connectedSTADLRSSI','dl_snr_db':'connectedSTADLSNR'}
    matches=co.Counter();missing=co.Counter();mismatches=co.Counter();fw=co.Counter();apfw=co.Counter()
    for r in c.execute('select id,station_raw_json,dashboard_raw_json from radio_link_config_telemetry'):
        orig=rfbyid[r['id']];s=segment(orig['_t'])
        if not s or not concordant(orig,s):continue
        j=json.loads(r['station_raw_json']);ap=json.loads(r['dashboard_raw_json'])
        fw[str(j.get('connectedSTASoftwareVersion'))]+=1;apfw[str(ap.get('cambiumCurrentuImageVersion'))]+=1
        for dest,src in fields.items():
            val=number(j.get(src))
            if val is None:missing[dest]+=1
            elif val==orig[dest]:matches[dest]+=1
            else:mismatches[dest]+=1
    c.close()
    totals={k:sum(r[k] for r in sr) for k in ['rf_rows','rf_pairs','rf_static_pairs','mcs_transitions','mcs_unaccompanied','tcp_dl_count','tcp_ul_count']}
    hrows=[]
    for (seg,direction,hour),v in sorted(hourly.items()):hrows.append(dict(segment=seg,direction=direction,hour_local=hour,n_tests=len(v),median_tcp_mbps=st.median(v)))
    write_csv(out/'campaign_18_segments_reproduced.csv',sr);write_csv(out/'campaign_hourly_tcp.csv',hrows)
    audit=dict(generated_utc=dt.datetime.now(dt.timezone.utc).isoformat(),python=sys.version,source=hashes,quick_check=quick,read_only=True,immutable=True,
        historical=ha,historical_main=hr,campaign_totals=totals,campaign_raw_rf_rows=len(rawrf),campaign_raw_tcp_attempts=len(tcp),tcp_sequential_exclusions=dict(exclusions),
        tcp_campaign_status_protocol=[dict(campaign_id=k[0],status=k[1],protocol=k[2],n=v) for k,v in strata.items()],
        clock_rf=clock_stats(rawrf,'timestamp_local','timestamp_utc'),clock_tcp=clock_stats(tcp,'timestamp_start_local','timestamp_start_utc'),
        join_clock=dict(join,rf_timestamp_copy_mismatches=copy_mismatch,max_recorded_vs_recomputed_difference_s=delta_max,recorded_vs_recomputed_difference_distribution=dict(delta_hist),eligible_max_recomputed_gap_s=max(eligible_delta),eligible_median_gap_s=st.median(eligible_delta)),
        raw_payload_audit=dict(field_mapping=fields,matches=dict(matches),missing=dict(missing),mismatches=dict(mismatches),sm_firmware=dict(fw),ap_firmware=dict(apfw)),
        sql_python_crosscheck='all segment event counts and TCP counts match',historical_git_blob='5617f651af6fdc980c85efe71d040d9eafa4c152',
        prospective_included=False,source_db_sha256_after=sha(db))
    assert audit['source_db_sha256_after']==EXPECTED_DB
    (out/'audit_v5.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(status='ok',totals=totals,clock=audit['join_clock'],historical=[{k:r[k] for k in ['scenario','eligible_adjacent_pairs','unchanged_adjacent_pairs','mcs_change_pairs','mcs_changes_during_constant_rf','exact_within_day_permutation_reference_pct']} for r in hr],raw_payload=audit['raw_payload_audit'],output_dir=str(out)),ensure_ascii=False))

if __name__=='__main__':main()
