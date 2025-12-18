from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List, Tuple

REQUIRED_TOP = ["kind", "engine", "run_id", "spec_source", "summary"]
REQUIRED_SUMMARY = ["trials", "attacker_win_rate", "defender_win_rate", "avg_time"]


def read_jsonl(path: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    records: List[Dict[str, Any]] = []
    errors: List[str] = []
    if not os.path.exists(path):
        return records, [f"File not found: {path}"]

    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj, dict):
                    obj["_line"] = i  # 디버깅용
                    records.append(obj)
                else:
                    errors.append(f"[L{i}] not a dict ({type(obj).__name__})")
            except Exception as e:
                errors.append(f"[L{i}] JSON parse error: {e}")
    return records, errors


def schema_of(r: Dict[str, Any]) -> str:
    v = r.get("schema_version")
    return v if isinstance(v, str) and v.strip() else "legacy"


def validate_record(r: Dict[str, Any], strict_v1: bool) -> List[str]:
    issues: List[str] = []
    line = r.get("_line", "?")

    sv = schema_of(r)
    if strict_v1 and sv != "v1":
        issues.append(f"[L{line}] schema_version is legacy (strict_v1 enabled)")

    for k in REQUIRED_TOP:
        if k not in r:
            issues.append(f"[L{line}] missing top-level key: {k}")

    if "summary" in r:
        s = r.get("summary")
        if not isinstance(s, dict):
            issues.append(f"[L{line}] summary is not a dict")
        else:
            for k in REQUIRED_SUMMARY:
                if k not in s:
                    issues.append(f"[L{line}] missing summary key: {k}")

            trials = s.get("trials", 0)
            try:
                if int(trials) <= 0:
                    issues.append(f"[L{line}] trials <= 0 ({trials})")
            except Exception:
                issues.append(f"[L{line}] trials not int-like ({trials})")

    kind = r.get("kind")
    if kind == "scenario_preset":
        if "scenario_spec" not in r:
            issues.append(f"[L{line}] scenario_preset missing scenario_spec")

    return issues


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="logs/scenarios.jsonl")
    p.add_argument("--strict-v1", action="store_true", help="legacy 로그를 오류로 처리")
    p.add_argument("--max", type=int, default=50, help="표시할 최대 이슈 수")
    args = p.parse_args()

    records, parse_errors = read_jsonl(args.input)
    issues: List[str] = []

    issues.extend(parse_errors)
    for r in records:
        issues.extend(validate_record(r, strict_v1=args.strict_v1))

    print(f"[INFO] file: {args.input}")
    print(f"[INFO] records: {len(records)}")
    print(f"[INFO] issues: {len(issues)}")

    if issues:
        print("[ISSUES]")
        for msg in issues[: args.max]:
            print(" -", msg)
        if len(issues) > args.max:
            print(f" - ... and {len(issues) - args.max} more")
        raise SystemExit(1)

    print("[OK] validation passed.")


if __name__ == "__main__":
    main()