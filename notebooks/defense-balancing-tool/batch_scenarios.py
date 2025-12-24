from __future__ import annotations

import argparse
import os
import uuid

from unit_io import load_units_from_file
from scenario_loader import load_scenarios_from_markdown
from battle_sim import find_unit_by_name_fuzzy, run_duel_trials_2d, run_swarm_trials_2d
from utils import append_jsonl


LOG_SCHEMA_VERSION = "v1"


def _clone_with_level(base, level: int):
    u = type(base).from_dict(base.to_dict())
    level = max(1, int(level))
    if level != u.level:
        delta = level - u.level
        u.hp += u.hp_per_level * delta
        u.atk += u.atk_per_level * delta
        u.level = level
    return u


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="logs/scenarios.jsonl")
    p.add_argument("--default-trials", type=int, default=200)
    p.add_argument("--reset", action="store_true", help="out 파일을 비우고 새로 씀")
    args = p.parse_args()

    units = load_units_from_file()
    if not units:
        print("[ERR] units.json 로드 실패(유닛 0개).")
        return

    duel_scenarios = load_scenarios_from_markdown("battle_scenarios_duel.md")
    swarm_scenarios = load_scenarios_from_markdown("battle_scenarios_swarm.md")
    scenarios = duel_scenarios + swarm_scenarios

    if not scenarios:
        print("[ERR] 시나리오 프리셋을 못 읽었습니다. md 파일/코드블록(json) 확인!")
        return

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    if args.reset and os.path.exists(args.out):
        open(args.out, "w", encoding="utf-8").close()

    session_run_id = str(uuid.uuid4())
    print(f"[INFO] scenarios: {len(scenarios)}")
    print(f"[INFO] out: {args.out}")
    print(f"[INFO] run_id: {session_run_id}")

    for i, sc in enumerate(scenarios, start=1):
        title = sc.get("title", f"Scenario {i}")
        encounter = str(sc.get("encounter_type", "duel")).lower().strip()

        a_name = sc.get("attacker_name", "")
        d_name = sc.get("defender_name", "")
        a_lv = int(sc.get("attacker_level", 1) or 1)
        d_lv = int(sc.get("defender_level", 1) or 1)

        attacker_base = find_unit_by_name_fuzzy(units, a_name)
        defender_base = find_unit_by_name_fuzzy(units, d_name)

        if attacker_base is None or defender_base is None:
            print(f"[SKIP] {title} (unit resolve failed) a={a_name} d={d_name}")
            continue

        attacker = _clone_with_level(attacker_base, a_lv)
        defender_template = _clone_with_level(defender_base, d_lv)

        trials = int(sc.get("trials") or args.default_trials)

        ax, ay = sc.get("attacker_pos", [0.0, 0.0])
        dx, dy = sc.get("defender_pos", [5.0, 0.0])
        attacker_pos = (float(ax), float(ay))
        defender_pos = (float(dx), float(dy))

        if encounter == "swarm":
            defender_count = int(sc.get("defender_count", 2) or 2)
            defender_spread = sc.get("defender_spread", None)
            summary = run_swarm_trials_2d(
                attacker=attacker,
                defender_template=defender_template,
                defender_count=defender_count,
                trials=trials,
                attacker_pos=attacker_pos,
                defender_pos=defender_pos,
                defender_spread=defender_spread,
                verbose_each=False,
            )
            engine = "run_swarm_trials_2d"
        else:
            summary = run_duel_trials_2d(
                attacker=attacker,
                defender=defender_template,
                trials=trials,
                attacker_pos=attacker_pos,
                defender_pos=defender_pos,
                verbose_each=False,
            )
            engine = "run_duel_trials_2d"

        record = {
            "schema_version": LOG_SCHEMA_VERSION,
            "kind": "scenario_preset",
            "engine": engine,
            "run_id": session_run_id,
            "spec_source": "units_ssot",
            "scenario_title": title,
            "scenario_source": sc.get("_source"),
            "scenario_spec": sc,
            "resolved_units": {
                "attacker": attacker.to_dict(),
                "defender_template": defender_template.to_dict(),
            },
            "summary": summary,
        }

        append_jsonl(args.out, record)
        if i % max(1, len(scenarios) // 10) == 0:
            print(f"  progress: {i}/{len(scenarios)}")

    print("[OK] done.")


if __name__ == "__main__":
    main()