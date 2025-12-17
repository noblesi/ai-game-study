#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSONL 로그를 로그 스키마 v1로 마이그레이션합니다.

- schema_version/run_id/engine/spec_source 등을 누락된 경우 채웁니다.
- --inplace 옵션 사용 시 원본을 .bak-YYYYMMDD-HHMMSS 로 백업 후 덮어씁니다.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import uuid
from typing import Any, Dict, List, Tuple


LOG_SCHEMA_VERSION = "v1"


def now_iso() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")


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
                    records.append(obj)
                else:
                    errors.append(f"[L{i}] not an object (dict): {type(obj).__name__}")
            except Exception as e:
                errors.append(f"[L{i}] JSON parse error: {e}")

    return records, errors


def write_jsonl(path: str, records: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def infer_engine(kind: str, r: Dict[str, Any]) -> str:
    # 최대한 “틀릴 가능성”을 줄이기 위해 보수적으로 추정
    if kind == "scenario_preset":
        return "run_duel_trials_2d"
    if kind == "auto_experiment":
        # legacy auto_experiment는 1D/2D를 확정 못하는 경우가 많아서 unknown로 둠
        return "unknown"
    return "unknown"


def infer_spec_source(kind: str) -> str:
    if kind == "scenario_preset":
        return "scenario_spec"
    if kind == "auto_experiment":
        return "units_runtime"
    return "unknown"


def migrate_record(r: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
    out = dict(r)
    changed = False

    kind = out.get("kind")
    if not isinstance(kind, str) or not kind.strip():
        kind = "unknown"
        out["kind"] = kind
        changed = True

    # schema_version
    sv = out.get("schema_version")
    if not isinstance(sv, str) or not sv.strip():
        out["schema_version"] = LOG_SCHEMA_VERSION
        changed = True

    # run_id
    rid = out.get("run_id")
    if not isinstance(rid, str) or not rid.strip():
        out["run_id"] = str(uuid.uuid4())
        changed = True

    # engine
    eng = out.get("engine")
    if not isinstance(eng, str) or not eng.strip():
        out["engine"] = infer_engine(kind, out)
        changed = True

    # spec_source
    ss = out.get("spec_source")
    if not isinstance(ss, str) or not ss.strip():
        out["spec_source"] = infer_spec_source(kind)
        changed = True

    # scenario_title/source 보정 (scenario_preset 한정)
    if kind == "scenario_preset":
        scen = out.get("scenario_spec")
        if isinstance(scen, dict):
            if (not isinstance(out.get("scenario_title"), str)) and isinstance(scen.get("title"), str):
                out["scenario_title"] = scen.get("title")
                changed = True
            if (not isinstance(out.get("scenario_source"), str)) and isinstance(scen.get("_source"), str):
                out["scenario_source"] = scen.get("_source")
                changed = True

    # logged_at (혹시 없는 경우만)
    la = out.get("logged_at")
    if not isinstance(la, str) or not la.strip():
        out["logged_at"] = now_iso()
        changed = True

    return out, changed


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="input jsonl path (e.g. logs/scenarios.jsonl)")
    p.add_argument("--output", default="", help="output jsonl path (default: <input>_v1.jsonl)")
    p.add_argument("--inplace", action="store_true", help="backup then overwrite input file")
    p.add_argument("--dry-run", action="store_true", help="do not write, only print stats")
    args = p.parse_args()

    records, errors = read_jsonl(args.input)
    if errors:
        print(f"[WARN] parse warnings: {len(errors)}")
        for e in errors[:10]:
            print(" -", e)
        if len(errors) > 10:
            print(f" - ... and {len(errors) - 10} more")

    migrated: List[Dict[str, Any]] = []
    changed_count = 0
    for r in records:
        out, changed = migrate_record(r)
        migrated.append(out)
        if changed:
            changed_count += 1

    print(f"[INFO] records: {len(records)} / changed: {changed_count}")

    if args.dry_run:
        print("[DRY-RUN] no files written.")
        return

    if args.inplace:
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = f"{args.input}.bak-{ts}"
        os.rename(args.input, backup)
        write_jsonl(args.input, migrated)
        print(f"[OK] inplace migrated: {args.input}")
        print(f"[OK] backup created : {backup}")
        return

    out_path = args.output.strip()
    if not out_path:
        if args.input.lower().endswith(".jsonl"):
            out_path = args.input[:-6] + "_v1.jsonl"
        else:
            out_path = args.input + "_v1.jsonl"

    write_jsonl(out_path, migrated)
    print(f"[OK] wrote: {out_path}")


if __name__ == "__main__":
    main()
