from __future__ import annotations

import argparse
import random
import uuid

from unit_io import load_units_from_file
from battle_sim import simulate_duel, simulate_duel_2d, build_experiment_summary
from utils import append_jsonl


LOG_SCHEMA_VERSION = "v1"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--pairs", type=int, default=30, help="생성할 (공격자,방어자) 조합 개수")
    p.add_argument("--trials", type=int, default=100, help="조합 당 반복 전투 횟수")
    p.add_argument("--mode", choices=["1", "2"], default="2", help="1=1D, 2=2D")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--out", default="logs/experiments.jsonl")
    p.add_argument("--random-pos", action="store_true", help="(2D) 시작 좌표를 랜덤으로 섞기")
    p.add_argument("--pos-range", type=float, default=8.0, help="(2D) 랜덤 좌표 범위 (+/-)")
    args = p.parse_args()

    units = load_units_from_file()
    if len(units) < 2:
        print("[ERR] 유닛이 2개 이상 필요합니다.")
        return

    rnd = random.Random(args.seed)
    session_run_id = str(uuid.uuid4())
    engine = "simulate_duel" if args.mode == "1" else "simulate_duel_2d"

    used = set()
    max_pairs = len(units) * (len(units) - 1)
    target_pairs = min(args.pairs, max_pairs)

    print(f"[INFO] units: {len(units)}")
    print(f"[INFO] generating pairs: {target_pairs} (trials each: {args.trials})")
    print(f"[INFO] out: {args.out}")
    print(f"[INFO] run_id: {session_run_id}")

    made = 0
    while made < target_pairs:
        ai = rnd.randrange(len(units))
        di = rnd.randrange(len(units))
        if ai == di:
            continue
        key = (ai, di)
        if key in used:
            continue
        used.add(key)

        attacker = units[ai]
        defender = units[di]

        wins_attacker = wins_defender = draws = no_result = 0
        total_time = 0.0
        total_attacker_hp = 0.0
        total_defender_hp = 0.0
        total_attacker_attacks = 0
        total_defender_attacks = 0

        for _ in range(args.trials):
            if args.mode == "1":
                result = simulate_duel(attacker, defender, verbose=False)
            else:
                if args.random_pos:
                    ax = rnd.uniform(-args.pos_range, args.pos_range)
                    ay = rnd.uniform(-args.pos_range, args.pos_range)
                    dx = rnd.uniform(-args.pos_range, args.pos_range)
                    dy = rnd.uniform(-args.pos_range, args.pos_range)
                    result = simulate_duel_2d(attacker, defender, attacker_pos=(ax, ay), defender_pos=(dx, dy), verbose=False)
                else:
                    result = simulate_duel_2d(attacker, defender, verbose=False)

            winner = result["winner"]
            if winner == "attacker":
                wins_attacker += 1
            elif winner == "defender":
                wins_defender += 1
            elif winner == "draw":
                draws += 1
            else:
                no_result += 1

            total_time += result["time"]
            total_attacker_hp += result["attacker_final_hp"]
            total_defender_hp += result["defender_final_hp"]
            total_attacker_attacks += result["attacker_attacks"]
            total_defender_attacks += result["defender_attacks"]

        summary = build_experiment_summary(
            attacker=attacker,
            defender=defender,
            trials=args.trials,
            total_time=total_time,
            total_attacker_hp=total_attacker_hp,
            total_defender_hp=total_defender_hp,
            total_attacker_attacks=total_attacker_attacks,
            total_defender_attacks=total_defender_attacks,
            wins_attacker=wins_attacker,
            wins_defender=wins_defender,
            draws=draws,
            no_result=no_result,
        )

        record = {
            "schema_version": LOG_SCHEMA_VERSION,
            "kind": "auto_experiment",
            "engine": engine,
            "run_id": session_run_id,
            "spec_source": "units_runtime",
            "pair_index": made + 1,
            "summary": summary,
        }

        append_jsonl(args.out, record)
        made += 1

        if made % max(1, target_pairs // 10) == 0:
            print(f"  progress: {made}/{target_pairs}")

    print("[OK] done.")


if __name__ == "__main__":
    main()