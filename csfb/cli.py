from __future__ import annotations

import argparse
import csv
from datetime import datetime,timezone
import hashlib
import json
import platform
import subprocess
import sys
from collections import Counter
from pathlib import Path

from . import __version__
from .baselines import BASELINES
from .dataset import manifest, validate
from .generator import GENERATOR_VERSION, SEED, adversarial_cases, golden_cases, synthetic_cases
from .metrics import score
from .model import read_jsonl, write_jsonl
from .runner import run_case

ROOT=Path(__file__).resolve().parents[1]
FILES=[ROOT/"datasets/golden/cases.jsonl",ROOT/"datasets/synthetic/cases.jsonl",ROOT/"datasets/adversarial/cases.jsonl"]


def generate(count=5000):
    write_jsonl(FILES[0],golden_cases());write_jsonl(FILES[1],synthetic_cases(count));write_jsonl(FILES[2],adversarial_cases())
    man=manifest(FILES,SEED,GENERATOR_VERSION);(ROOT/"datasets/MANIFEST.json").write_text(json.dumps(man,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(man,ensure_ascii=False,indent=2))


def run(args):
    cases=[c for p in FILES for c in read_jsonl(p)]
    if args.quick:cases=cases[:min(500,len(cases))]
    if args.category:cases=[c for c in cases if c.category==args.category]
    if args.case:cases=[c for c in cases if c.id==args.case]
    if args.engine=="all":names=list(BASELINES)
    elif args.engine in BASELINES:names=[args.engine]
    elif args.engine=="external":names=["external"]
    else:raise SystemExit(f"unknown engine: {args.engine}")
    rows=[];summaries={}
    for name in names:
        erows=[]
        for c in cases:erows += run_case(c,name,args.engine_command if name=="external" else None)
        for r in erows:r["engine"]=name
        rows+=erows;summaries[name]=score(erows)
        print(f"{name}: cases={len(cases)} events={len(erows)} final_accuracy={summaries[name]['final_accuracy']} catastrophic_absolute={summaries[name]['catastrophic_absolute_rate']}")
    reports=ROOT/"reports";reports.mkdir(exist_ok=True)
    try:head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:head="uncommitted"
    man=json.loads((ROOT/"datasets/MANIFEST.json").read_text(encoding="utf-8"))
    result={"schema_version":1,"engine":{"names":names,"version":"0.1.0","git_commit":head},"benchmark":{"version":__version__,"dataset_sha256":man["sha256"],"seed":SEED,"case_count":len(cases),"input_event_count":sum(len(c.events) for c in cases),"prediction_count":len(rows),"runner_version":__version__,"timestamp_utc":datetime.now(timezone.utc).isoformat(),"python":platform.python_version(),"platform":platform.platform(),"cpu":platform.processor()},"metrics":summaries,"rows":rows}
    (reports/"results.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with (reports/"results.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ["case_id"]);w.writeheader();w.writerows(rows)
    with (reports/"failures.jsonl").open("w",encoding="utf-8",newline="\n") as f:
        for r in rows:
            if r["expected"] is not None and r["predicted"] not in ([r["expected"]]+(r["acceptable_segments"] or [])):
                f.write(json.dumps(r,ensure_ascii=False)+"\n")
    category={}
    for name in names:
        category[name]={}
        for cat in sorted({c.category for c in cases}):category[name][cat]=score([r for r in rows if r["engine"]==name and r["category"]==cat])
    result["category_metrics"]=category;(reports/"results.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    md=["# CSFB v0.1 Baseline Results","",f"- Cases: {len(cases)}",f"- Input events: {sum(len(c.events) for c in cases)}",f"- Predictions: {len(rows)}",f"- Dataset SHA256: `{man['sha256']}`",f"- Seed: {SEED}",f"- Generator: {GENERATOR_VERSION}",f"- Runner: {__version__}",f"- Git commit: `{head}`",f"- Timestamp (UTC): {result['benchmark']['timestamp_utc']}","","These are transparent reference baselines, not production-engine claims.",""]
    md += ["| Engine | Final accuracy | Within 1 | Catastrophic absolute | Wrong backward | Recovery | P95 latency (µs) |","|---|---:|---:|---:|---:|---:|---:|"]
    for name,m in summaries.items():md.append(f"| {name} | {m['final_accuracy']} | {m['within_1_accuracy']} | {m['catastrophic_absolute_rate']} | {m['wrong_backward_jump_rate']} | {m['recovery_success_rate']} | {m['latency_p95_us']} |")
    md += ["","## Failure categories","", "Highest event error counts per engine:",""]
    for name in names:
        totals=Counter(r["category"] for r in rows if r["engine"]==name and r["expected"] is not None and r["predicted"]!=r["expected"])
        md.append(f"- **{name}:** " + ", ".join(f"{c} ({n})" for c,n in totals.most_common(8)))
    (reports/"CSFB_V0_1_BASELINES.md").write_text("\n".join(md)+"\n",encoding="utf-8")


def main():
    p=argparse.ArgumentParser(prog="csfb");sp=p.add_subparsers(dest="command",required=True)
    g=sp.add_parser("generate");g.add_argument("--count",type=int,default=5000)
    v=sp.add_parser("validate");v.add_argument("--no-schema",action="store_true")
    r=sp.add_parser("run");r.add_argument("--quick",action="store_true");r.add_argument("--full",action="store_true");r.add_argument("--engine",default="all");r.add_argument("--engine-command");r.add_argument("--category");r.add_argument("--case")
    q=sp.add_parser("replay");q.add_argument("--case",required=True);q.add_argument("--engine",default="local-fuzzy");q.add_argument("--trace",action="store_true")
    sp.add_parser("report")
    a=p.parse_args()
    if a.command=="generate":generate(a.count)
    elif a.command=="validate":print(json.dumps(validate(FILES,not a.no_schema),indent=2))
    elif a.command=="run":run(a)
    elif a.command=="replay":
        c=next((c for path in FILES for c in read_jsonl(path) if c.id==a.case),None)
        if not c:raise SystemExit("case not found")
        for row in run_case(c,a.engine):print(json.dumps(row,ensure_ascii=False,indent=2) if a.trace else f"EVENT {row['event_index']} {row['event_type']} INPUT={row['text']!r} EXPECTED={row['expected']} ACTUAL={row['predicted']} ERROR={None if row['expected'] is None else row['predicted']-row['expected']}")
    elif a.command=="report":
        f=ROOT/"reports/CSFB_V0_1_BASELINES.md"
        print(f.read_text(encoding="utf-8") if f.exists() else "No report yet. Run `csfb run --full`.")

if __name__=="__main__":main()
