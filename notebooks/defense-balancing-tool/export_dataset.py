#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSONL 로그(전투 실험)를 읽어서 ML/분석용 CSV 데이터셋으로 export.

- 입력: logs/scenarios.jsonl, logs/experiments.jsonl 등
- 출력: datasets/battle_dataset_v1.csv (기본)
- 레코드 단위: "실험 1회(summary 1개)" = CSV 1행
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from collections import defaultdict
from typing import Any, Dict, List, Tuple


UNIT_KEYS = [
    "name", "level", "hp", "atk",
    "role", "cost", "range",
    "attack_speed", "move_speed",
    "target_type", "attack_type",
    "hp_per_level", "atk_per_level",
]


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
                    errors.append(f"{path} L{i}: not a dict ({type(obj).__name__})")
            except Exception as e:
                errors.append(f"{path} L{i}: JSON parse error: {e}")
    return records, errors


def schema_of(r: Dict[str, Any]) -> str:
    v = r.get("schema_version")
    return v if isinstance(v, str) and v.strip() else "legacy"


def short_id(x: Any, n: int = 8) -> str:
    if not isinstance(x, str):
        return "-"
    x = x.strip()
    return x[:n] if x else "-"


def flatten_unit(u: Any, prefix: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    if not isinstance(u, dict):
        # 키는 만들어두되 값은 비움(일관된 컬럼 유지)
        for k in UNIT_KEYS:
            out[f"{prefix}{k}"] = None
        return out

    for k in UNIT_KEYS:
        out[f"{prefix}{k}"] = u.get(k)
    return out

def to_float(x: Any) -> float | None:
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).strip()
    if not s:
        return None
    try:
        return float(s)
    except Exception:
        return None

def safe_div(num: float | None, den: float | None) -> float | None:
    if num is None or den is None:
        return None
    if den == 0:
        return None
    return num / den


def majority_winner(s: Dict[str, Any]) -> str:
    """trials 요약에서 다수결 승자 라벨."""
    try:
        wa = float(s.get("attacker_win_rate", 0.0) or 0.0)
        wd = float(s.get("defender_win_rate", 0.0) or 0.0)
        dr = float(s.get("draw_rate", 0.0) or 0.0)
    except Exception:
        return "unknown"

    m = max(wa, wd, dr)
    if m == wa and wa > wd and wa > dr:
        return "attacker"
    if m == wd and wd > wa and wd > dr:
        return "defender"
    if m == dr and dr > wa and dr > wd:
        return "draw"
    return "tie"


def export_csv(records: List[Dict[str, Any]], out_path: str, kinds: List[str], min_trials: int) -> None:
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    rows: List[Dict[str, Any]] = []
    stats = defaultdict(int)

    for r in records:
        kind = r.get("kind", "unknown")
        if kinds and kind not in kinds:
            stats["skip_kind"] += 1
            continue

        s = r.get("summary")
        if not isinstance(s, dict):
            stats["skip_no_summary"] += 1
            continue

        trials = int(s.get("trials", 0) or 0)
        if trials < min_trials:
            stats["skip_min_trials"] += 1
            continue

        row: Dict[str, Any] = {}

        # meta
        row["logged_at"] = r.get("logged_at")
        row["schema_version"] = schema_of(r)
        row["kind"] = kind
        row["engine"] = r.get("engine")
        row["run_id"] = r.get("run_id")
        row["run_id_short"] = short_id(r.get("run_id"))
        row["spec_source"] = r.get("spec_source")

        # scenario meta (있을 때만)
        row["scenario_title"] = r.get("scenario_title")
        row["scenario_source"] = r.get("scenario_source")

        # summary core
        row["trials"] = trials
        row["wins_attacker"] = s.get("wins_attacker")
        row["wins_defender"] = s.get("wins_defender")
        row["draws"] = s.get("draws")
        row["no_result"] = s.get("no_result")

        row["attacker_win_rate"] = s.get("attacker_win_rate")
        row["defender_win_rate"] = s.get("defender_win_rate")
        row["draw_rate"] = s.get("draw_rate")
        row["no_result_rate"] = s.get("no_result_rate")
        row["avg_time"] = s.get("avg_time")

        # positions (2D 시나리오면 종종 존재)
        row["attacker_pos"] = s.get("attacker_pos")
        row["defender_pos"] = s.get("defender_pos")

        # 전투 타입(duel/swarm) + swarm일 때 defender 수
        row["encounter_type"] = s.get("encounter_type", "duel")
        try:
            row["defender_count"] = int(s.get("defender_count", 1) or 1)
        except Exception:
            row["defender_count"] = 1

        # unit features
        row.update(flatten_unit(s.get("attacker_unit"), "a_"))
        row.update(flatten_unit(s.get("defender_unit"), "d_"))

        # ===== group key (for Group Split) =====
        # a_name / d_name 컬럼은 flatten_unit(UNIT_KEYS에 name 포함)로 이미 생성됨
        a_name = row.get("a_name")
        d_name = row.get("d_name")
        if isinstance(a_name, str) and isinstance(d_name, str) and a_name.strip() and d_name.strip():
            encounter = str(row.get("encounter_type") or "duel").lower()
            count = row.get("defender_count")
            row["pair_key"] = f"{a_name.strip()}__vs__{d_name.strip()}__{encounter}__x{count}"
        else:
            row["pair_key"] = None

        # ===== derived features (DPS/TTK/Adv) =====
        a_hp = to_float(row.get("a_hp"))
        a_atk = to_float(row.get("a_atk"))
        a_rng = to_float(row.get("a_range"))
        a_as = to_float(row.get("a_attack_speed"))

        d_hp = to_float(row.get("d_hp"))
        d_atk = to_float(row.get("d_atk"))
        d_rng = to_float(row.get("d_range"))
        d_as = to_float(row.get("d_attack_speed"))

        a_dps = (a_atk * a_as) if (a_atk is not None and a_as is not None) else None
        d_dps = (d_atk * d_as) if (d_atk is not None and d_as is not None) else None

        # TTK 추정: 상대 HP / 내 DPS
        a_ttk_est = safe_div(d_hp, a_dps)  # attacker가 defender를 잡는 데 걸리는 시간(추정)
        d_ttk_est = safe_div(a_hp, d_dps)  # defender가 attacker를 잡는 데 걸리는 시간(추정)

        row["a_dps"] = a_dps
        row["d_dps"] = d_dps
        row["a_ttk_est"] = a_ttk_est
        row["d_ttk_est"] = d_ttk_est

        # advantage(차이 피처)
        row["dps_adv"] = (a_dps - d_dps) if (a_dps is not None and d_dps is not None) else None
        row["range_adv"] = (a_rng - d_rng) if (a_rng is not None and d_rng is not None) else None
        # ttk_adv: (defender가 attacker를 잡는 시간) - (attacker가 defender를 잡는 시간)
        # 값이 클수록 attacker가 유리(내가 상대를 더 빨리 잡거나, 상대가 나를 더 늦게 잡음)
        row["ttk_adv"] = (d_ttk_est - a_ttk_est) if (d_ttk_est is not None and a_ttk_est is not None) else None

        # labels
        row["label_majority_winner"] = majority_winner(s)
        try:
            wa = float(s.get("attacker_win_rate", 0.0) or 0.0)
            wd = float(s.get("defender_win_rate", 0.0) or 0.0)
            row["label_attacker_better"] = 1 if wa > wd else 0
        except Exception:
            row["label_attacker_better"] = None

        rows.append(row)
        stats["ok"] += 1

    # 컬럼 고정(대략 “메타 → 요약 → 유닛 → 라벨” 순)
    fieldnames = [
        "logged_at", "schema_version", "kind", "engine", "run_id", "run_id_short", "spec_source",
        "scenario_title", "scenario_source",
        "pair_key",
        "trials", "wins_attacker", "wins_defender", "draws", "no_result",
        "attacker_win_rate", "defender_win_rate", "draw_rate", "no_result_rate", "avg_time",
        "attacker_pos", "defender_pos", "encounter_type", "defender_count",
        *[f"a_{k}" for k in UNIT_KEYS],
        *[f"d_{k}" for k in UNIT_KEYS],

        "a_dps", "d_dps",
        "a_ttk_est", "d_ttk_est",
        "dps_adv", "range_adv", "ttk_adv",

        "label_majority_winner", "label_attacker_better",
    ]

    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)

    print(f"[OK] wrote: {out_path} (rows={len(rows)})")
    if stats:
        print("[STATS]")
        for k in sorted(stats.keys()):
            print(f" - {k}: {stats[k]}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", action="append", default=["logs/scenarios.jsonl"],
                   help="jsonl path (repeatable). default: logs/scenarios.jsonl")
    p.add_argument("--output", default="datasets/battle_dataset_v1.csv")
    p.add_argument("--kinds", default="scenario_preset,auto_experiment",
                   help="comma-separated kinds to include (default: scenario_preset,auto_experiment)")
    p.add_argument("--min-trials", type=int, default=1)
    args = p.parse_args()

    kinds = [x.strip() for x in (args.kinds or "").split(",") if x.strip()]
    all_records: List[Dict[str, Any]] = []
    all_errors: List[str] = []

    for path in args.input:
        recs, errs = read_jsonl(path)
        all_records.extend(recs)
        all_errors.extend(errs)

    if all_errors:
        print(f"[WARN] parse warnings: {len(all_errors)} (showing up to 10)")
        for e in all_errors[:10]:
            print(" -", e)

    export_csv(all_records, args.output, kinds=kinds, min_trials=args.min_trials)


if __name__ == "__main__":
    main()
