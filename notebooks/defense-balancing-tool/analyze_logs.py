#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""JSONL(전투 시나리오 로그)을 읽어 시나리오별 요약 리포트(.md)를 자동 생성합니다.

포트폴리오/리뷰 관점에서 보기 좋게:
- 시나리오별 승률/무승부/무효(no_result) 비율 + 가중 평균(시간 등)
- 임계치 기반 플래그(밸런스 붕괴/무효 비율/긴 전투)
- Top-N(핫스팟) 테이블
"""

from __future__ import annotations

import argparse
import datetime
import os
from collections import defaultdict
from typing import Any, Dict, List, Tuple, Optional, Callable

from common.jsonl import read_jsonl, schema_of, short_id


def fmt_pct(x: Any) -> str:
    if x is None:
        return "-"
    try:
        return f"{float(x) * 100:.1f}%"
    except Exception:
        return "-"


def fmt_num(x: Any, nd: int = 2) -> str:
    if x is None:
        return "-"
    try:
        return f"{float(x):.{nd}f}"
    except Exception:
        return "-"


def unit_brief(u: Any) -> str:
    if not isinstance(u, dict):
        return "-"
    keys = [
        "name", "level", "hp", "atk", "range", "attack_speed", "move_speed",
        "target_type", "attack_type", "role", "cost",
    ]
    parts: List[str] = []
    for k in keys:
        if k in u:
            parts.append(f"{k}={u.get(k)}")
    return ", ".join(parts) if parts else "-"


def parse_dt(x: str) -> datetime.datetime:
    try:
        return datetime.datetime.fromisoformat(x)
    except Exception:
        return datetime.datetime.min


def _rate(n: int, d: int) -> Optional[float]:
    return (n / d) if d > 0 else None


def _weighted_avg(sum_w: float, w: int) -> Optional[float]:
    return (sum_w / w) if w > 0 else None


def compute_stats(recs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """scenario_title의 여러 run(summary)을 합산/가중 평균해 요약."""
    runs = len(recs)

    total_trials = 0
    wins_a = wins_d = draws = nores = 0

    w_time = 0.0
    w_a_hp = 0.0
    w_d_hp = 0.0
    w_a_attacks = 0.0
    w_d_attacks = 0.0

    for r in recs:
        s = r.get("summary") or {}
        if not isinstance(s, dict):
            continue

        t = int(s.get("trials", 0) or 0)
        total_trials += t

        wins_a += int(s.get("wins_attacker", 0) or 0)
        wins_d += int(s.get("wins_defender", 0) or 0)
        draws += int(s.get("draws", 0) or 0)
        nores += int(s.get("no_result", 0) or 0)

        if t <= 0:
            continue

        def addw(key: str, acc: str) -> None:
            nonlocal w_time, w_a_hp, w_d_hp, w_a_attacks, w_d_attacks
            v = s.get(key)
            if v is None:
                return
            try:
                fv = float(v)
            except Exception:
                return

            if acc == "time":
                w_time += fv * t
            elif acc == "a_hp":
                w_a_hp += fv * t
            elif acc == "d_hp":
                w_d_hp += fv * t
            elif acc == "a_att":
                w_a_attacks += fv * t
            elif acc == "d_att":
                w_d_attacks += fv * t

        addw("avg_time", "time")
        addw("avg_attacker_final_hp", "a_hp")
        addw("avg_defender_final_hp", "d_hp")
        addw("avg_attacker_attacks", "a_att")
        addw("avg_defender_attacks", "d_att")

    a_wr = _rate(wins_a, total_trials)
    d_wr = _rate(wins_d, total_trials)
    dr = _rate(draws, total_trials)
    nr = _rate(nores, total_trials)

    avg_time = _weighted_avg(w_time, total_trials)
    avg_a_hp = _weighted_avg(w_a_hp, total_trials)
    avg_d_hp = _weighted_avg(w_d_hp, total_trials)
    avg_a_att = _weighted_avg(w_a_attacks, total_trials)
    avg_d_att = _weighted_avg(w_d_attacks, total_trials)

    imbalance = abs((a_wr or 0.0) - (d_wr or 0.0)) if total_trials > 0 else None

    return {
        "runs": runs,
        "trials": total_trials,
        "wins_a": wins_a,
        "wins_d": wins_d,
        "draws": draws,
        "nores": nores,
        "a_wr": a_wr,
        "d_wr": d_wr,
        "draw_r": dr,
        "nores_r": nr,
        "avg_time": avg_time,
        "avg_attacker_final_hp": avg_a_hp,
        "avg_defender_final_hp": avg_d_hp,
        "avg_attacker_attacks": avg_a_att,
        "avg_defender_attacks": avg_d_att,
        "imbalance": imbalance,
    }


def build_flags(
    stats: Dict[str, Any],
    *,
    warn_win: float,
    warn_nores: float,
    warn_time: float,
) -> List[str]:
    flags: List[str] = []

    a_wr = stats.get("a_wr")
    d_wr = stats.get("d_wr")
    nr = stats.get("nores_r")
    at = stats.get("avg_time")

    if isinstance(a_wr, float) and a_wr >= warn_win:
        flags.append("A_dom")
    if isinstance(d_wr, float) and d_wr >= warn_win:
        flags.append("D_dom")
    if isinstance(nr, float) and nr >= warn_nores:
        flags.append("NoRes")
    if isinstance(at, float) and at >= warn_time:
        flags.append("Slow")

    return flags


def write_report(
    records: List[Dict[str, Any]],
    errors: List[str],
    out_path: str,
    *,
    recent_n: int,
    top_n: int,
    warn_win: float,
    warn_nores: float,
    warn_time: float,
) -> None:
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    scenario_recs = [
        r for r in records
        if r.get("kind") == "scenario_preset" and isinstance(r.get("summary"), dict)
    ]

    by_title: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for r in scenario_recs:
        by_title[r.get("scenario_title", "Untitled")].append(r)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # schema_version 분포
    ver_counts: Dict[str, int] = defaultdict(int)
    for r in records:
        ver_counts[schema_of(r)] += 1
    ver_text = ", ".join([f"{k}:{v}" for k, v in sorted(ver_counts.items(), key=lambda kv: kv[0])])

    # 시나리오 요약 stats 캐시
    scenario_rows: List[Tuple[str, Dict[str, Any]]] = []
    for title, recs in by_title.items():
        scenario_rows.append((title, compute_stats(recs)))

    md: List[str] = []
    md.append("# Scenario Summary Report\n\n")
    md.append(f"- Generated at: {now}\n")
    md.append(f"- Input records: {len(records)} (scenario_preset: {len(scenario_recs)})\n")
    md.append(f"- Schema versions: {ver_text}\n")
    if len(ver_counts) > 1:
        md.append("- ⚠️ Mixed schema versions detected. Consider migrating legacy logs to v1.\n")
    md.append(f"- Flags: win>={warn_win:.2f}, no_result>={warn_nores:.2f}, avg_time>={warn_time:.1f}\n")
    if errors:
        md.append(f"- Parse warnings: {len(errors)} (see bottom)\n")

    # =============================
    # Overview
    # =============================
    md.append("\n---\n\n## Overview\n\n")
    md.append("| Scenario | Runs | Trials | A win% | D win% | Draw% | NoRes% | Avg time | Flags |\n")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|---|\n")

    for title, st in sorted(scenario_rows, key=lambda x: x[0]):
        flags = build_flags(st, warn_win=warn_win, warn_nores=warn_nores, warn_time=warn_time)
        md.append(
            f"| {title} | {st['runs']} | {st['trials']} | {fmt_pct(st['a_wr'])} | {fmt_pct(st['d_wr'])} | "
            f"{fmt_pct(st['draw_r'])} | {fmt_pct(st['nores_r'])} | {fmt_num(st['avg_time'])} | "
            f"{', '.join(flags) if flags else '-'} |\n"
        )

    # =============================
    # Hotspots (Top-N)
    # =============================
    md.append("\n---\n\n## Hotspots (Top-N)\n\n")

    def top_table(title: str, rows: List[Tuple[str, Optional[float]]], fmt: Callable[[float], str]) -> None:
        md.append(f"### {title}\n\n")
        md.append("| rank | scenario | value |\n")
        md.append("|---:|---|---:|\n")
        shown = 0
        rank = 1
        for name, v in rows:
            if v is None:
                continue
            md.append(f"| {rank} | {name} | {fmt(v)} |\n")
            shown += 1
            rank += 1
            if shown >= top_n:
                break
        if shown == 0:
            md.append("| - | (none) | - |\n")
        md.append("\n")

    imbalance_rows = sorted(
        [(t, st.get("imbalance")) for t, st in scenario_rows],
        key=lambda x: (x[1] is None, -(x[1] or 0.0)),
    )
    top_table("Most imbalanced (|A win% - D win%|)", imbalance_rows, lambda v: fmt_pct(v))

    a_wr_rows = sorted(
        [(t, st.get("a_wr")) for t, st in scenario_rows],
        key=lambda x: (x[1] is None, -(x[1] or 0.0)),
    )
    top_table("Highest attacker win%", a_wr_rows, lambda v: fmt_pct(v))

    d_wr_rows = sorted(
        [(t, st.get("d_wr")) for t, st in scenario_rows],
        key=lambda x: (x[1] is None, -(x[1] or 0.0)),
    )
    top_table("Highest defender win%", d_wr_rows, lambda v: fmt_pct(v))

    nores_rows = sorted(
        [(t, st.get("nores_r")) for t, st in scenario_rows],
        key=lambda x: (x[1] is None, -(x[1] or 0.0)),
    )
    top_table("Highest no_result%", nores_rows, lambda v: fmt_pct(v))

    slow_rows = sorted(
        [(t, st.get("avg_time")) for t, st in scenario_rows],
        key=lambda x: (x[1] is None, -(x[1] or 0.0)),
    )
    top_table("Slowest avg_time", slow_rows, lambda v: fmt_num(v))

    # =============================
    # Details
    # =============================
    md.append("---\n\n## Details\n\n")
    for title, recs in sorted(by_title.items(), key=lambda kv: kv[0]):
        md.append(f"### {title}\n\n")

        total_trials = 0
        wins_a = wins_d = draws = nores = 0
        w_time = w_a_hp = w_d_hp = w_a_att = w_d_att = 0.0

        for r in recs:
            s = r["summary"]
            t = int(s.get("trials", 0) or 0)
            total_trials += t
            wins_a += int(s.get("wins_attacker", 0) or 0)
            wins_d += int(s.get("wins_defender", 0) or 0)
            draws += int(s.get("draws", 0) or 0)
            nores += int(s.get("no_result", 0) or 0)

            if t <= 0:
                continue

            def addw(key: str, acc: str) -> None:
                nonlocal w_time, w_a_hp, w_d_hp, w_a_att, w_d_att
                v = s.get(key)
                if v is None:
                    return
                try:
                    fv = float(v)
                except Exception:
                    return

                if acc == "time":
                    w_time += fv * t
                elif acc == "a_hp":
                    w_a_hp += fv * t
                elif acc == "d_hp":
                    w_d_hp += fv * t
                elif acc == "a_att":
                    w_a_att += fv * t
                elif acc == "d_att":
                    w_d_att += fv * t

            addw("avg_time", "time")
            addw("avg_attacker_final_hp", "a_hp")
            addw("avg_defender_final_hp", "d_hp")
            addw("avg_attacker_attacks", "a_att")
            addw("avg_defender_attacks", "d_att")

        def rate(n: int) -> Optional[float]:
            return (n / total_trials) if total_trials > 0 else None

        md.append(f"- Runs: **{len(recs)}**\n")
        md.append(f"- Total trials (sum): **{total_trials}**\n")
        md.append(
            f"- Win rates (overall): attacker **{fmt_pct(rate(wins_a))}**, defender **{fmt_pct(rate(wins_d))}**, "
            f"draw **{fmt_pct(rate(draws))}**, no_result **{fmt_pct(rate(nores))}**\n"
        )
        md.append(
            f"- Weighted averages: avg_time **{fmt_num(w_time / total_trials if total_trials else None)}**, "
            f"avg_attacker_final_hp **{fmt_num(w_a_hp / total_trials if total_trials else None)}**, "
            f"avg_defender_final_hp **{fmt_num(w_d_hp / total_trials if total_trials else None)}**, "
            f"avg_attacker_attacks **{fmt_num(w_a_att / total_trials if total_trials else None)}**, "
            f"avg_defender_attacks **{fmt_num(w_d_att / total_trials if total_trials else None)}**\n"
        )

        md.append("\n**Recent runs**\n\n")
        md.append("| logged_at | schema | engine | run_id | attacker | defender | trials | attacker_win_rate | avg_time |\n")
        md.append("|---|---|---|---|---|---|---:|---:|---:|\n")
        for r in sorted(recs, key=lambda rr: parse_dt(rr.get("logged_at", "")), reverse=True)[:recent_n]:
            s = r["summary"]
            md.append(
                f"| {r.get('logged_at', '-')} | {schema_of(r)} | {r.get('engine', '-')} | {short_id(r.get('run_id'))} | "
                f"{s.get('attacker_name', '-')} | {s.get('defender_name', '-')} | {s.get('trials', '-')} | "
                f"{fmt_pct(s.get('attacker_win_rate'))} | {fmt_num(s.get('avg_time'))} |\n"
            )

        # most recent snapshot
        recent_sorted = sorted(recs, key=lambda rr: parse_dt(rr.get("logged_at", "")), reverse=True)
        if recent_sorted:
            recent = recent_sorted[0]
            s = recent["summary"]
            md.append("\n**Unit snapshot (most recent)**\n\n")
            md.append(f"- Attacker unit: `{unit_brief(s.get('attacker_unit'))}`\n")
            md.append(f"- Defender unit: `{unit_brief(s.get('defender_unit'))}`\n")
            if "attacker_pos" in s and "defender_pos" in s:
                md.append(f"- Positions: attacker {s.get('attacker_pos')} / defender {s.get('defender_pos')}\n")
            md.append("\n")

    if errors:
        md.append("---\n\n## Parse warnings\n\n")
        for e in errors[:50]:
            md.append(f"- {e}\n")
        if len(errors) > 50:
            md.append(f"- ... and {len(errors) - 50} more\n")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("".join(md))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="logs/scenarios.jsonl")
    p.add_argument("--output", default="reports/scenario_report.md")
    p.add_argument("--recent", type=int, default=5)
    p.add_argument("--top", type=int, default=5, help="Hotspots Top-N")
    p.add_argument("--warn-win", type=float, default=0.65, help="win-rate flag threshold")
    p.add_argument("--warn-nores", type=float, default=0.05, help="no_result-rate flag threshold")
    p.add_argument("--warn-time", type=float, default=10.0, help="avg_time flag threshold")
    args = p.parse_args()

    in_path = args.input
    if args.input == "logs/scenarios.jsonl" and (not os.path.exists(in_path)) and os.path.exists("scenarios.jsonl"):
        in_path = "scenarios.jsonl"

    records, errors = read_jsonl(in_path)
    write_report(
        records,
        errors,
        args.output,
        recent_n=args.recent,
        top_n=max(1, int(args.top)),
        warn_win=float(args.warn_win),
        warn_nores=float(args.warn_nores),
        warn_time=float(args.warn_time),
    )
    print(f"[OK] wrote: {args.output} (records={len(records)})")


if __name__ == "__main__":
    main()
