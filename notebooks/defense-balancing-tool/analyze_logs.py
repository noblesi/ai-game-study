#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""JSONL(전투 시나리오 로그)을 읽어 시나리오별 요약 리포트(.md)를 자동 생성합니다."""

from __future__ import annotations
import argparse, datetime, json, os
from collections import defaultdict
from typing import Any, Dict, List, Tuple

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
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                errors.append(f"Line {i}: JSONDecodeError {e.msg} (col {e.colno})")
    return records, errors

def fmt_pct(x: Any) -> str:
    if x is None:
        return "-"
    try:
        return f"{float(x)*100:.1f}%"
    except Exception:
        return "-"

def fmt_num(x: Any, nd: int = 2) -> str:
    if x is None:
        return "-"
    try:
        return f"{float(x):.{nd}f}"
    except Exception:
        return "-"

def unit_brief(u):
    if not isinstance(u, dict):
        return "-"

    keys = ["name","level","hp","atk","range","attack_speed","move_speed","target_type","attack_type","role","cost"]
    parts = []
    for k in keys:
        if k in u:
            parts.append(f"{k}={u.get(k)}")  # <-- 핵심: hookup 같은 고정 문자열 말고 실제 값을 출력
    return ", ".join(parts) if parts else "-"


def parse_dt(x: str) -> datetime.datetime:
    try:
        return datetime.datetime.fromisoformat(x)
    except Exception:
        return datetime.datetime.min

def write_report(records: List[Dict[str, Any]], errors: List[str], out_path: str, recent_n: int) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    scenario_recs = [r for r in records if r.get("kind") == "scenario_preset" and isinstance(r.get("summary"), dict)]
    by_title: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for r in scenario_recs:
        by_title[r.get("scenario_title", "Untitled")].append(r)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md: List[str] = []
    md.append("# Scenario Summary Report\n\n")
    md.append(f"- Generated at: {now}\n")
    md.append(f"- Input records: {len(records)} (scenario_preset: {len(scenario_recs)})\n")
    if errors:
        md.append(f"- Parse warnings: {len(errors)} (see bottom)\n")
    md.append("\n---\n\n")

    md.append("## Overview\n\n")
    md.append("| Scenario | Runs | Total trials | Attacker win | Defender win | Draw | No result | Avg time (weighted) |\n")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|\n")

    for title, recs in sorted(by_title.items(), key=lambda kv: kv[0]):
        total_trials = 0
        wins_a = wins_d = draws = nores = 0
        w_time = 0.0
        for r in recs:
            s = r["summary"]
            t = int(s.get("trials", 0) or 0)
            total_trials += t
            wins_a += int(s.get("wins_attacker", 0) or 0)
            wins_d += int(s.get("wins_defender", 0) or 0)
            draws += int(s.get("draws", 0) or 0)
            nores += int(s.get("no_result", 0) or 0)
            if t > 0 and s.get("avg_time") is not None:
                try:
                    w_time += float(s["avg_time"]) * t
                except Exception:
                    pass
        avg_time = (w_time / total_trials) if total_trials > 0 else None
        md.append(f"| {title} | {len(recs)} | {total_trials} | {wins_a} | {wins_d} | {draws} | {nores} | {fmt_num(avg_time)} |\n")

    md.append("\n---\n\n## Details\n\n")
    for title, recs in sorted(by_title.items(), key=lambda kv: kv[0]):
        md.append(f"### {title}\n\n")
        total_trials = 0
        wins_a = wins_d = draws = nores = 0
        w_time = w_a_hp = w_d_hp = w_a_atk = w_d_atk = 0.0

        for r in recs:
            s = r["summary"]
            t = int(s.get("trials", 0) or 0)
            total_trials += t
            wins_a += int(s.get("wins_attacker", 0) or 0)
            wins_d += int(s.get("wins_defender", 0) or 0)
            draws += int(s.get("draws", 0) or 0)
            nores += int(s.get("no_result", 0) or 0)

            def addw(key: str, acc: str) -> None:
                nonlocal w_time, w_a_hp, w_d_hp, w_a_atk, w_d_atk
                if t <= 0:
                    return
                v = s.get(key)
                if v is None:
                    return
                try:
                    v = float(v)
                except Exception:
                    return
                if acc == "time": w_time += v * t
                elif acc == "a_hp": w_a_hp += v * t
                elif acc == "d_hp": w_d_hp += v * t
                elif acc == "a_atk": w_a_atk += v * t
                elif acc == "d_atk": w_d_atk += v * t

            addw("avg_time", "time")
            addw("avg_attacker_final_hp", "a_hp")
            addw("avg_defender_final_hp", "d_hp")
            addw("avg_attacker_attacks", "a_atk")
            addw("avg_defender_attacks", "d_atk")

        def rate(n: int) -> float | None:
            return (n / total_trials) if total_trials > 0 else None

        md.append(f"- Runs: **{len(recs)}**\n")
        md.append(f"- Total trials (sum): **{total_trials}**\n")
        md.append(
            f"- Win rates (overall): attacker **{fmt_pct(rate(wins_a))}**, defender **{fmt_pct(rate(wins_d))}**, "
            f"draw **{fmt_pct(rate(draws))}**, no_result **{fmt_pct(rate(nores))}**\n"
        )
        md.append(
            f"- Weighted averages: avg_time **{fmt_num(w_time/total_trials if total_trials else None)}**, "
            f"avg_attacker_final_hp **{fmt_num(w_a_hp/total_trials if total_trials else None)}**, "
            f"avg_defender_final_hp **{fmt_num(w_d_hp/total_trials if total_trials else None)}**, "
            f"avg_attacker_attacks **{fmt_num(w_a_atk/total_trials if total_trials else None)}**, "
            f"avg_defender_attacks **{fmt_num(w_d_atk/total_trials if total_trials else None)}**\n"
        )

        md.append("\n**Recent runs**\n\n")
        md.append("| logged_at | attacker | defender | trials | attacker_win_rate | avg_time |\n")
        md.append("|---|---|---|---:|---:|---:|\n")
        for r in sorted(recs, key=lambda rr: parse_dt(rr.get("logged_at","")), reverse=True)[:recent_n]:
            s = r["summary"]
            md.append(
                f"| {r.get('logged_at','-')} | {s.get('attacker_name','-')} | {s.get('defender_name','-')} | "
                f"{s.get('trials','-')} | {fmt_pct(s.get('attacker_win_rate'))} | {fmt_num(s.get('avg_time'))} |\n"
            )

        recent = sorted(recs, key=lambda rr: parse_dt(rr.get("logged_at","")), reverse=True)[0]
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
            md.append(f"- ... and {len(errors)-50} more\n")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("".join(md))

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="logs/scenarios.jsonl")
    p.add_argument("--output", default="reports/scenario_report.md")
    p.add_argument("--recent", type=int, default=5)
    args = p.parse_args()

    in_path = args.input
    if args.input == "logs/scenarios.jsonl" and (not os.path.exists(in_path)) and os.path.exists("scenarios.jsonl"):
        in_path = "scenarios.jsonl"

    records, errors = read_jsonl(in_path)
    write_report(records, errors, args.output, args.recent)
    print(f"[OK] wrote: {args.output} (records={len(records)})")

if __name__ == "__main__":
    main()
