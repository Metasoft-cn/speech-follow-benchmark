from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import platform
import shlex
import subprocess
from pathlib import Path

from . import __version__
from .baselines import BASELINES
from .dataset import manifest, validate
from .generator import GENERATOR_VERSION, SEED, adversarial_cases, curated_cases, golden_cases, synthetic_cases
from .metrics import score
from .model import read_jsonl, write_jsonl
from .runner import run_case

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "datasets/golden/curated.jsonl",
    ROOT / "datasets/golden/template_derived.jsonl",
    ROOT / "datasets/synthetic/cases.jsonl",
    ROOT / "datasets/adversarial/cases.jsonl",
]
REPORT_PATH = ROOT / "reports/CSFB_V0_2_BASELINES.md"


def generate(count=5000):
    write_jsonl(FILES[0], curated_cases())
    write_jsonl(FILES[1], golden_cases())
    write_jsonl(FILES[2], synthetic_cases(count))
    write_jsonl(FILES[3], adversarial_cases())
    result = manifest(FILES, SEED, GENERATOR_VERSION)
    (ROOT / "datasets/MANIFEST.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def _source_fingerprint():
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
        status = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL)
        dirty = bool(status.strip())
    except Exception:
        commit = "uncommitted"
        dirty = None
    source_paths = sorted((ROOT / "csfb").glob("*.py")) + sorted((ROOT / "schema").glob("*.json")) + [ROOT / "pyproject.toml"]
    digest = hashlib.sha256()
    for path in source_paths:
        digest.update(path.relative_to(ROOT).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return {"git_commit": commit, "working_tree_dirty": dirty, "code_sha256": digest.hexdigest()}


def run(args):
    cases = [case for path in FILES for case in read_jsonl(path)]
    if args.category:
        cases = [case for case in cases if case.category == args.category]
    if args.case:
        cases = [case for case in cases if case.id == args.case]
    if args.quick:
        cases = cases[:500]

    if args.engine == "all":
        names = list(BASELINES)
    elif args.engine in BASELINES:
        names = [args.engine]
    elif args.engine == "external":
        if not args.engine_command:
            raise SystemExit("--engine external requires --engine-command")
        names = ["external"]
    else:
        raise SystemExit(f"unknown engine: {args.engine}")

    rows = []
    summaries = {}
    for name in names:
        engine_rows = []
        command = args.engine_command if name == "external" else None
        for case in cases:
            engine_rows.extend(run_case(case, name, command))
        for row in engine_rows:
            row["engine"] = name
        rows.extend(engine_rows)
        summaries[name] = score(engine_rows)
        summary = summaries[name]
        print(f"{name}: cases={len(cases)} events={len(engine_rows)} final_accuracy={summary['final_accuracy']} catastrophic_absolute={summary['catastrophic_absolute_rate']}")

    reports = Path(getattr(args, "output_dir", ROOT / "reports"))
    reports.mkdir(exist_ok=True)
    source = _source_fingerprint()
    dataset_manifest = json.loads((ROOT / "datasets/MANIFEST.json").read_text(encoding="utf-8"))
    layer_counts = {entry["path"].replace("datasets/", "").replace(".jsonl", "").replace("/", "_"): entry["case_count"] for entry in dataset_manifest["files"]}

    category_metrics = {
        name: {
            category: score([row for row in rows if row["engine"] == name and row["category"] == category])
            for category in sorted({row["category"] for row in rows})
        }
        for name in names
    }
    distance_values = sorted({row["expected_candidate_distance"] for row in rows if row.get("expected_candidate_distance") is not None})
    candidate_distance_metrics = {
        name: {
            str(distance): score([row for row in rows if row["engine"] == name and row.get("expected_candidate_distance") == distance])
            for distance in distance_values
        }
        for name in names
    }
    skip_distances = sorted({case.metadata["skip_distance"] for case in cases if case.metadata.get("skip_distance") is not None})
    skip_distance_metrics = {
        name: {
            str(distance): {
                "case_count": len({
                    case.id for case in cases
                    if case.category in ("intentional_skip", "forgotten_then_skip")
                    and case.metadata.get("skip_distance") == distance
                }),
                "metrics": score([
                    row for row in rows
                    if row["engine"] == name
                    and row.get("skip_distance") == distance
                    and row["category"] in ("intentional_skip", "forgotten_then_skip")
                ]),
            }
            for distance in skip_distances
            if any(
                case.category in ("intentional_skip", "forgotten_then_skip")
                and case.metadata.get("skip_distance") == distance
                for case in cases
            )
        }
        for name in names
    }
    language_metrics = {
        name: summaries[name]["by_language"] for name in names
    }
    region_metrics = {
        name: summaries[name]["by_region"] for name in names
    }

    result = {
        "schema_version": 1,
        "engine": {"names": names, "version": __version__, **source},
        "benchmark": {
            "version": __version__,
            "dataset_version": dataset_manifest["dataset_version"],
            "dataset_sha256": dataset_manifest["sha256"],
            "seed": SEED,
            "case_count": len(cases),
            "input_event_count": sum(len(case.events) for case in cases),
            "corpus_layer_counts": layer_counts,
            "prediction_count": len(rows),
            "runner_version": __version__,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "metrics": summaries,
        "language_metrics": language_metrics,
        "region_metrics": region_metrics,
        "category_metrics": category_metrics,
        "candidate_distance_metrics": candidate_distance_metrics,
        "skip_distance_metrics": skip_distance_metrics,
    }
    (reports / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (reports / "results.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]) if rows else ["case_id"])
        writer.writeheader()
        writer.writerows(rows)
    with (reports / "failures.jsonl").open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            if row["expected"] is not None and row["predicted"] not in ([row["expected"]] + (row["acceptable_segments"] or [])):
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")

    markdown = [
        "# CSFB v0.2.0 Preview Baseline Results",
        "",
        f"- Cases: {len(cases)}",
        f"- Input events: {sum(len(case.events) for case in cases)}",
        f"- Predictions: {len(rows)}",
        f"- Dataset SHA256: `{dataset_manifest['sha256']}`",
        f"- Seed: {SEED}",
        f"- Generator: {GENERATOR_VERSION}",
        f"- Runner: {__version__}",
        f"- Base Git commit: `{source['git_commit']}`",
        f"- Working tree dirty: {source['working_tree_dirty']}",
        f"- Code SHA256: `{source['code_sha256']}`",
        f"- Timestamp (UTC): {result['benchmark']['timestamp_utc']}",
        "",
        "These are transparent reference baselines, not production-engine claims.",
        "",
        "Corpus layers: curated review-status cases, template-derived cases, seeded synthetic cases, and adversarial cases.",
        "",
        "| Engine | Final accuracy | Within 1 | Catastrophic absolute | Wrong backward | Candidate detection | False candidate | Candidate position | Evidence count | Confirm accuracy | Cancel accuracy | P95 latency (µs) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, metrics in summaries.items():
        columns = ("final_accuracy", "within_1_accuracy", "catastrophic_absolute_rate", "wrong_backward_jump_rate", "jump_candidate_detection_rate", "false_jump_candidate_rate", "jump_candidate_position_accuracy", "jump_evidence_count_accuracy", "jump_confirmation_accuracy", "jump_cancellation_accuracy", "latency_p95_us")
        markdown.append("| " + name + " | " + " | ".join("n/a" if metrics.get(key) is None else str(metrics[key]) for key in columns) + " |")

    markdown += ["", "## Tracking safety", "", "| Engine | Wrong backward | False movement | False jump commit | Duplicate reanchor error | Catastrophic absolute | Catastrophic backward | Wrong intermediate skip jump |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for name, metrics in summaries.items():
        columns = ("wrong_backward_jump_rate", "false_movement_rate", "false_jump_commit_rate", "duplicate_reanchor_error_rate", "catastrophic_absolute_rate", "catastrophic_backward_rate", "intentional_skip_wrong_intermediate_jump_rate")
        markdown.append("| " + name + " | " + " | ".join("n/a" if metrics.get(key) is None else f"{metrics[key]:.4f}" for key in columns) + " |")

    focus = (
        ("intentional_skip", "Intentional skip"),
        ("accidental_future_phrase", "Accidental future phrase"),
        ("forgotten_word_pause", "Forgotten-word pause"),
        ("false_jump_candidate", "False candidate"),
        ("jump_confirmation", "Confirmation"),
        ("jump_cancellation", "Cancellation"),
        ("section_jump", "Section jump"),
        ("non_spoken_regions", "Skipped blocks"),
        ("non_spoken_similarity_trap", "Skip similarity trap"),
        ("spoken_override", "Spoken skip text"),
        ("duplicate", "Duplicate"),
        ("backtrack", "Backtrack"),
    )
    markdown += ["", "## Event position accuracy by intent and navigation category", "", "| Engine | " + " | ".join(label for _, label in focus) + " |", "|---|" + "---:|" * len(focus)]
    for name in names:
        values = []
        for category, _ in focus:
            metric = category_metrics[name].get(category, {}).get("event_accuracy")
            values.append("n/a" if metric is None else f"{metric:.3f}")
        markdown.append("| " + name + " | " + " | ".join(values) + " |")

    markdown += ["", "## Candidate evidence by expected jump distance", "", "| Engine | Distance (segments) | Candidate events | Detection | Candidate position | Evidence count | Confirmation |", "|---|---:|---:|---:|---:|---:|---:|"]
    for name in names:
        for distance in distance_values:
            metrics = candidate_distance_metrics[name][str(distance)]
            values = (metrics["jump_candidate_labeled_events"], metrics["jump_candidate_detection_rate"], metrics["jump_candidate_position_accuracy"], metrics["jump_evidence_count_accuracy"], metrics["jump_confirmation_accuracy"])
            markdown.append("| " + name + " | " + str(distance) + " | " + " | ".join("n/a" if value is None else f"{value:.3f}" if isinstance(value, float) else str(value) for value in values) + " |")

    markdown += ["", "## Intentional skip recovery by distance", "", "| Engine | Intentional skip distance | Cases | Recovery | Events to recover median | P95 |", "|---|---:|---:|---:|---:|---:|"]
    for name in names:
        for distance, entry in skip_distance_metrics[name].items():
            metrics = entry["metrics"]
            values = (entry["case_count"], metrics.get("intentional_skip_recovery_rate"), metrics.get("intentional_skip_events_to_recover_median"), metrics.get("intentional_skip_events_to_recover_p95"))
            markdown.append("| " + name + " | +" + str(distance) + " | " + " | ".join("n/a" if value is None else f"{value:.3f}" if isinstance(value, float) else str(value) for value in values) + " |")

    markdown += ["", "## Language breakdown", "", "| Engine | Language | Judged events | Final accuracy | Within 1 |", "|---|---|---:|---:|---:|"]
    for name in names:
        for language in ("zh", "en", "mixed"):
            metrics = language_metrics[name].get(language, {})
            values = (metrics.get("judged_events"), metrics.get("final_accuracy"), metrics.get("within_1_accuracy"))
            markdown.append("| " + name + " | " + language + " | " + " | ".join("n/a" if value is None else f"{value:.3f}" if isinstance(value, float) else str(value) for value in values) + " |")

    markdown += ["", "## Spoken and non-spoken document scenarios", "", "| Engine | Region | Judged events | Final accuracy | Within 1 |", "|---|---|---:|---:|---:|"]
    for name in names:
        for region in ("spoken_only", "non_spoken_region"):
            metrics = region_metrics[name].get(region, {})
            values = (metrics.get("judged_events"), metrics.get("final_accuracy"), metrics.get("within_1_accuracy"))
            markdown.append("| " + name + " | " + region + " | " + " | ".join("n/a" if value is None else f"{value:.3f}" if isinstance(value, float) else str(value) for value in values) + " |")

    markdown += ["", "## Failure categories", "", "Highest event error counts per engine:", ""]
    for name in names:
        totals = Counter(row["category"] for row in rows if row["engine"] == name and row["expected"] is not None and row["predicted"] != row["expected"])
        markdown.append(f"- **{name}:** " + ", ".join(f"{category} ({count})" for category, count in totals.most_common(8)))
    report_text = "\n".join(markdown) + "\n"
    REPORT_PATH.write_text(report_text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(prog="csfb")
    commands = parser.add_subparsers(dest="command", required=True)
    generate_parser = commands.add_parser("generate")
    generate_parser.add_argument("--count", type=int, default=5000)
    validate_parser = commands.add_parser("validate")
    validate_parser.add_argument("--no-schema", action="store_true")
    run_parser = commands.add_parser("run")
    run_parser.add_argument("--quick", action="store_true")
    run_parser.add_argument("--full", action="store_true")
    run_parser.add_argument("--engine", default="all")
    run_parser.add_argument("--engine-command")
    run_parser.add_argument("--category")
    run_parser.add_argument("--case")
    run_parser.add_argument("--output-dir", default=str(ROOT / "reports"))
    replay_parser = commands.add_parser("replay")
    replay_parser.add_argument("--case", required=True)
    replay_parser.add_argument("--engine", default="local-fuzzy")
    replay_parser.add_argument("--trace", action="store_true")
    commands.add_parser("report")
    args = parser.parse_args()

    if args.command == "generate":
        generate(args.count)
    elif args.command == "validate":
        print(json.dumps(validate(FILES, not args.no_schema), ensure_ascii=False, indent=2))
    elif args.command == "run":
        run(args)
    elif args.command == "replay":
        case = next((case for path in FILES for case in read_jsonl(path) if case.id == args.case), None)
        if case is None:
            raise SystemExit("case not found")
        command = args.engine_command if hasattr(args, "engine_command") else None
        for row in run_case(case, args.engine, command):
            if args.trace:
                print(json.dumps(row, ensure_ascii=False, indent=2))
            else:
                error = None if row["expected"] is None else row["predicted"] - row["expected"]
                print(f"EVENT {row['event_index']} {row['event_type']} INPUT={row['text']!r} EXPECTED={row['expected']} ACTUAL={row['predicted']} ERROR={error}")
    elif args.command == "report":
        print(REPORT_PATH.read_text(encoding="utf-8") if REPORT_PATH.exists() else "No report yet. Run `csfb run --full`.")


if __name__ == "__main__":
    main()
