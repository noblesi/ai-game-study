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
import math
from collections import defaultdict
from typing import Any, Dict, List, Tuple, Set

from common.jsonl import read_jsonl, schema_of, short_id
from common.parse import to_float, safe_div
from common.perk import load_perk_catalog


UNIT_KEYS = [
    "name", "level", "hp", "atk",
    "role", "cost", "range",
    "attack_speed", "move_speed",
    "target_type", "attack_type",
    "hp_per_level", "atk_per_level",
]

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

def _as_point(v: Any) -> Tuple[float, float] | None:
    """JSON에서 읽은 좌표(list/tuple)를 (x,y)로 변환."""
    if isinstance(v, (list, tuple)) and len(v) >= 2:
        x = to_float(v[0])
        y = to_float(v[1])
        if x is None or y is None:
            return None
        return (x, y)
    return None

def _perk_sig(perks: Any) -> str:
    """perks(list[str]) -> signature 문자열(정렬 + 중복제거)."""
    if not isinstance(perks, list):
        return "none"
    uniq = sorted({str(p).strip() for p in perks if str(p).strip()})
    return "+".join(uniq) if uniq else "none"

def _dist_bucket(dist: Any, step: float = 1.0) -> str:
    """start_distance를 버킷 문자열로 변환(연속값 유사 샘플을 묶기 위함)."""
    d = to_float(dist)
    if d is None:
        return "na"
    if step <= 0:
        step = 1.0
    try:
        return str(int(d // step))
    except Exception:
        return "na"

def _as_points(v: Any) -> List[Tuple[float, float]]:
    """스웜 defender_pos처럼 좌표 리스트를 [(x,y),...]로 변환."""
    if not isinstance(v, list):
        return []
    pts: List[Tuple[float, float]] = []
    for it in v:
        p = _as_point(it)
        if p is not None:
            pts.append(p)
    return pts

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

    # perk 목록을 고정 컬럼으로 쓰기 위해 catalog에서 id를 확정
    perk_catalog = load_perk_catalog()
    perk_ids = sorted(perk_catalog.keys())

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

        # start distance (2D용)
        # - duel: attacker_pos ↔ defender_pos
        # - swarm: attacker_pos ↔ (defender_pos 리스트 중 최소 거리) 또는 defender_pos가 1개 점이면 그대로
        start_distance = None
        ap = _as_point(row["attacker_pos"])
        enc_tmp = str(s.get("encounter_type", "duel") or "duel").strip().lower()
        dp_raw = row["defender_pos"]
        if ap is not None:
            if enc_tmp == "swarm" and isinstance(dp_raw, list) and dp_raw and isinstance(dp_raw[0], (list, tuple)):
                dps = _as_points(dp_raw)
                if dps:
                    start_distance = min(math.hypot(px - ap[0], py - ap[1]) for px, py in dps)
            else:
                dp = _as_point(dp_raw)
                if dp is not None:
                    start_distance = math.hypot(dp[0] - ap[0], dp[1] - ap[1])

        row["start_distance"] = start_distance


        # 전투 타입(duel/swarm) + swarm일 때 defender 수
        row["encounter_type"] = s.get("encounter_type", "duel")
        try:
            row["defender_count"] = int(s.get("defender_count", 1) or 1)
        except Exception:
            row["defender_count"] = 1

        # unit features
        row.update(flatten_unit(s.get("attacker_unit"), "a_"))
        row.update(flatten_unit(s.get("defender_unit"), "d_"))

        # ===== perk features (count + one-hot) =====
        a_unit = s.get("attacker_unit") if isinstance(s.get("attacker_unit"), dict) else {}
        d_unit = s.get("defender_unit") if isinstance(s.get("defender_unit"), dict) else {}

        a_perks = a_unit.get("perks") or []
        d_perks = d_unit.get("perks") or []
        a_set = set(a_perks) if isinstance(a_perks, list) else set()
        d_set = set(d_perks) if isinstance(d_perks, list) else set()

        row["a_perk_count"] = len(a_set)
        row["d_perk_count"] = len(d_set)
        row["perk_count_adv"] = len(a_set) - len(d_set)

        for pid in perk_ids:
            a_has = 1 if pid in a_set else 0
            d_has = 1 if pid in d_set else 0
            row[f"a_has_perk_{pid}"] = a_has
            row[f"d_has_perk_{pid}"] = d_has
            row[f"perk_adv_{pid}"] = a_has - d_has

        # ===== group key (for Group Split) =====
        # a_name / d_name 컬럼은 flatten_unit(UNIT_KEYS에 name 포함)로 이미 생성됨
        a_name = row.get("a_name")
        d_name = row.get("d_name")
        if isinstance(a_name, str) and isinstance(d_name, str) and a_name.strip() and d_name.strip():
            encounter = str(row.get("encounter_type") or "duel").lower()
            count = row.get("defender_count")
            row["pair_key"] = f"{a_name.strip()}__vs__{d_name.strip()}__{encounter}__x{count}"

            # 더 강한(세분화된) 그룹키: 레벨/퍼크/거리버킷까지 포함
            a_lv = row.get("a_level")
            d_lv = row.get("d_level")
            a_sig = _perk_sig(a_perks)
            d_sig = _perk_sig(d_perks)
            dist_b = _dist_bucket(row.get("start_distance"), step=1.0)
            row["pair_key_full"] = (
                f"{a_name.strip()}@L{a_lv}|{a_sig}"
                f"__vs__"
                f"{d_name.strip()}@L{d_lv}|{d_sig}"
                f"__{encounter}__x{count}__dist{dist_b}"
            )
        else:
            row["pair_key"] = None
            row["pair_key_full"] = None

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
        "pair_key_full",
        "trials", "wins_attacker", "wins_defender", "draws", "no_result",
        "attacker_win_rate", "defender_win_rate", "draw_rate", "no_result_rate", "avg_time",
        "attacker_pos", "defender_pos", "start_distance", "encounter_type", "defender_count",
        *[f"a_{k}" for k in UNIT_KEYS],
        *[f"d_{k}" for k in UNIT_KEYS],
        "a_perk_count", "d_perk_count", "perk_count_adv",
        *[f"a_has_perk_{pid}" for pid in perk_ids],
        *[f"d_has_perk_{pid}" for pid in perk_ids],
        *[f"perk_adv_{pid}" for pid in perk_ids],
        "a_dps", "d_dps",
        "a_ttk_est", "d_ttk_est",
        "dps_adv", "range_adv", "ttk_adv",

        "label_majority_winner", "label_attacker_better",
    ]

    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, None) for k in fieldnames})

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
