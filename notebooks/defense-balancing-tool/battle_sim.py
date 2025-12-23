"""전투 시뮬레이션(1D/2D) + 자동 실험용 요약 로직 모듈.

- unit_model.Unit을 입력으로 받아 전투를 시뮬레이션하고,
- 결과를 공통 dict 포맷(winner/time/... )으로 반환한다.

주의:
- 이 파일은 '계산 로직' 위주로 유지한다.
- 콘솔 메뉴(UI)는 unit_logic.py 쪽에서 담당한다.
"""

import math
from typing import Tuple, Dict, Any, List, Optional

from unit_model import Unit


def _get_unit_kind(unit: Unit) -> str:
    """role 문자열 기반으로 유닛 kind를 추정한다."""
    r = (unit.role or "").lower()
    if "air" in r:
        return "air"
    if "tower" in r:
        return "tower"
    return "ground"


def _can_attack_target(attacker: Unit, defender: Unit) -> bool:
    """attacker.target_type과 defender(kind) 기반 공격 가능 여부."""
    atk_target = (attacker.target_type or "").lower()
    def_kind = _get_unit_kind(defender)

    if atk_target == "both":
        return True
    if atk_target == "ground":
        return def_kind == "ground"
    if atk_target == "air":
        return def_kind == "air"
    if atk_target == "tower":
        return def_kind == "tower"

    # 기타 값들은 일단 느슨하게 매칭
    return atk_target == def_kind


def _is_in_attack_range(attacker: Unit, defender: Unit, distance: float) -> bool:
    """공격 타입에 따라 사거리 판정."""
    atk_type = (attacker.attack_type or "").lower()
    if atk_type == "melee":
        return distance <= 1.0
    return distance <= float(attacker.range)


# ============================
# Perk helpers (v0)
# ============================

def _perks(unit: Unit) -> List[str]:
    return list(getattr(unit, "perks", []) or [])


def _effective_combat_stats(unit: Unit, context: str) -> dict:
    """Perk를 반영한 '실전 스탯'을 계산한다.

    context:
      - "duel": 1v1
      - "swarm": 1vN
    """
    perks = _perks(unit)
    hp = float(unit.hp)
    atk = float(unit.atk)
    attack_speed = float(unit.attack_speed)
    move_speed = float(unit.move_speed)
    rng = float(unit.range)

    if "shield" in perks:
        hp *= 1.2

    if "rapid" in perks:
        attack_speed *= 1.2

    if context == "duel" and "duelist" in perks:
        atk *= 1.1
        attack_speed *= 1.1

    # 기본값으로는 정수 스탯을 유지하되, 내부 연산은 float로
    return {
        "hp": hp,
        "atk": atk,
        "attack_speed": attack_speed,
        "move_speed": move_speed,
        "range": rng,
        "perks": perks,
    }


def _apply_on_hit(attacker_perks: List[str], damage: float, attacker_hp: float, attacker_max_hp: float) -> float:
    """lifesteal 등 '적중 시' 효과를 반영해서 attacker_hp를 갱신."""
    if "lifesteal" in attacker_perks:
        heal = max(0.0, damage * 0.2)
        attacker_hp = min(attacker_hp + heal, attacker_max_hp)
    return attacker_hp


def _maybe_execute(attacker_perks: List[str], target_hp_after: float, target_max_hp: float, base_damage: float) -> float:
    """execute: 타깃 HP가 30% 이하로 내려가면 피해를 1.5배로."""
    if "execute" in attacker_perks and target_max_hp > 0:
        if target_hp_after <= 0.3 * target_max_hp:
            return base_damage * 1.5
    return base_damage


def simulate_duel(
    attacker: Unit,
    defender: Unit,
    initial_distance: float = 5.0,
    verbose: bool = True,
) -> dict:
    """1D 거리 기반 1:1 전투(시간 이벤트 방식)."""
    a_stats = _effective_combat_stats(attacker, context="duel")
    d_stats = _effective_combat_stats(defender, context="duel")

    a_hp = float(a_stats["hp"])
    d_hp = float(d_stats["hp"])
    a_max_hp = a_hp
    d_max_hp = d_hp
    a_as = float(a_stats["attack_speed"])
    d_as = float(d_stats["attack_speed"])
    a_atk = float(a_stats["atk"])
    d_atk = float(d_stats["atk"])
    a_move = float(a_stats["move_speed"])
    d_move = float(d_stats["move_speed"])
    a_perks = a_stats["perks"]
    d_perks = d_stats["perks"]

    if a_as <= 0 and d_as <= 0:
        if verbose:
            print("양쪽 모두 공격 속도가 0이라 전투가 진행되지 않습니다.")
        return {
            "winner": "none",
            "time": 0.0,
            "attacker_final_hp": a_hp,
            "defender_final_hp": d_hp,
            "attacker_attacks": 0,
            "defender_attacks": 0,
        }

    a_interval = math.inf if a_as <= 0 else 1.0 / a_as
    d_interval = math.inf if d_as <= 0 else 1.0 / d_as

    time = 0.0
    next_a = 0.0 if a_interval < math.inf else math.inf
    next_d = 0.0 if d_interval < math.inf else math.inf
    a_attacks = 0
    d_attacks = 0

    rel_speed = max(a_move, 0.0) + max(d_move, 0.0)
    eps = 1e-9
    max_steps = 10000

    def _max_effective_range(u: Unit, eff_attack_speed: float) -> float:
        if eff_attack_speed <= 0:
            return 0.0
        if (u.attack_type or "").lower() == "melee":
            return 1.0
        return float(u.range)

    max_range = max(_max_effective_range(attacker, a_as), _max_effective_range(defender, d_as))
    if rel_speed <= 0 and initial_distance > max_range:
        if verbose:
            print("서로 사거리 안에 들어갈 수 없어 전투가 발생하지 않습니다.")
        return {
            "winner": "none",
            "time": 0.0,
            "attacker_final_hp": a_hp,
            "defender_final_hp": d_hp,
            "attacker_attacks": 0,
            "defender_attacks": 0,
        }

    for _ in range(max_steps):
        if a_hp <= 0 or d_hp <= 0:
            break

        next_event = min(next_a, next_d)
        if next_event == math.inf:
            if verbose:
                print("더 이상 공격 이벤트가 없어 전투를 종료합니다.")
            break

        time = next_event
        distance = initial_distance if rel_speed <= 0 else max(0.0, initial_distance - rel_speed * time)

        if verbose:
            print(
                f"\n[시간 {time:.2f}s] 거리:{distance:.2f}, "
                f"{attacker.name} HP:{a_hp:.1f}, {defender.name} HP:{d_hp:.1f}"
            )

        # attacker attack
        if next_a <= next_event + eps:
            if _can_attack_target(attacker, defender) and _is_in_attack_range(attacker, defender, distance):
                base = a_atk
                after = d_hp - base
                dmg = _maybe_execute(a_perks, target_hp_after=after, target_max_hp=d_max_hp, base_damage=base)
                d_hp -= dmg
                a_hp = _apply_on_hit(a_perks, damage=dmg, attacker_hp=a_hp, attacker_max_hp=a_max_hp)
                a_attacks += 1
                if verbose:
                    print(
                        f"  {attacker.name} -> {defender.name} "
                        f"({dmg:.1f} 피해, {defender.name} HP {max(d_hp, 0):.1f})"
                    )
            elif verbose:
                print(f"  {attacker.name} 공격 불가 (사거리/타겟 조건 미충족)")
            next_a += a_interval

        # defender attack
        if d_hp > 0 and next_d <= next_event + eps:
            if _can_attack_target(defender, attacker) and _is_in_attack_range(defender, attacker, distance):
                base = d_atk
                after = a_hp - base
                dmg = _maybe_execute(d_perks, target_hp_after=after, target_max_hp=a_max_hp, base_damage=base)
                a_hp -= dmg
                d_hp = _apply_on_hit(d_perks, damage=dmg, attacker_hp=d_hp, attacker_max_hp=d_max_hp)
                d_attacks += 1
                if verbose:
                    print(
                        f"  {defender.name} -> {attacker.name} "
                        f"({dmg:.1f} 피해, {attacker.name} HP {max(a_hp, 0):.1f})"
                    )
            elif verbose:
                print(f"  {defender.name} 공격 불가 (사거리/타겟 조건 미충족)")
            next_d += d_interval

    if a_hp > 0 and d_hp <= 0:
        winner = "attacker"
    elif d_hp > 0 and a_hp <= 0:
        winner = "defender"
    elif a_hp <= 0 and d_hp <= 0:
        winner = "draw"
    else:
        winner = "none"

    return {
        "winner": winner,
        "time": time,
        "attacker_final_hp": max(a_hp, 0.0),
        "defender_final_hp": max(d_hp, 0.0),
        "attacker_attacks": a_attacks,
        "defender_attacks": d_attacks,
    }


def simulate_duel_2d(
    attacker: Unit,
    defender: Unit,
    attacker_pos: Tuple[float, float] = (0.0, 0.0),
    defender_pos: Tuple[float, float] = (5.0, 0.0),
    dt: float = 0.05,
    max_time: float = 60.0,
    verbose: bool = True,
) -> dict:
    """2D 좌표 기반 1:1 전투 시뮬레이션."""
    ax, ay = attacker_pos
    dx, dy = defender_pos

    a_stats = _effective_combat_stats(attacker, context="duel")
    d_stats = _effective_combat_stats(defender, context="duel")

    a_hp = float(a_stats["hp"])
    d_hp = float(d_stats["hp"])
    a_max_hp = a_hp
    d_max_hp = d_hp
    a_as = float(a_stats["attack_speed"])
    d_as = float(d_stats["attack_speed"])
    a_atk = float(a_stats["atk"])
    d_atk = float(d_stats["atk"])
    a_move = float(a_stats["move_speed"])
    d_move = float(d_stats["move_speed"])
    a_perks = a_stats["perks"]
    d_perks = d_stats["perks"]

    if a_as <= 0 and d_as <= 0:
        if verbose:
            print("양쪽 모두 공격 속도가 0이라 전투가 진행되지 않습니다.")
        return {
            "winner": "none",
            "time": 0.0,
            "attacker_final_hp": a_hp,
            "defender_final_hp": d_hp,
            "attacker_attacks": 0,
            "defender_attacks": 0,
            "attacker_start_pos": attacker_pos,
            "defender_start_pos": defender_pos,
            "attacker_final_pos": attacker_pos,
            "defender_final_pos": defender_pos,
        }

    a_interval = math.inf if a_as <= 0 else 1.0 / a_as
    d_interval = math.inf if d_as <= 0 else 1.0 / d_as

    a_next = a_interval if a_interval < math.inf else math.inf
    d_next = d_interval if d_interval < math.inf else math.inf

    time = 0.0
    a_attacks = 0
    d_attacks = 0
    eps = 1e-9

    attacker_start_pos = (ax, ay)
    defender_start_pos = (dx, dy)

    while time < max_time and a_hp > 0 and d_hp > 0:
        t_tick = time + dt
        next_event = min(t_tick, a_next, d_next)
        move_dt = max(0.0, next_event - time)

        # 이동(서로를 향해)
        if a_move > 0 or d_move > 0:
            vec_x = dx - ax
            vec_y = dy - ay
            dist = math.hypot(vec_x, vec_y)
            if dist > 0:
                dir_x = vec_x / dist
                dir_y = vec_y / dist
            else:
                dir_x = dir_y = 0.0

            ax += a_move * dir_x * move_dt
            ay += a_move * dir_y * move_dt

            dx -= d_move * dir_x * move_dt
            dy -= d_move * dir_y * move_dt

        time = next_event
        distance = math.hypot(dx - ax, dy - ay)

        if verbose:
            print(
                f"\n[시간 {time:.2f}s] 거리:{distance:.2f}, "
                f"{attacker.name} HP:{a_hp:.1f}, {defender.name} HP:{d_hp:.1f}"
            )

        # attacker attack
        if time + eps >= a_next:
            if _can_attack_target(attacker, defender) and _is_in_attack_range(attacker, defender, distance):
                base = a_atk
                after = d_hp - base
                dmg = _maybe_execute(a_perks, target_hp_after=after, target_max_hp=d_max_hp, base_damage=base)
                d_hp -= dmg
                a_hp = _apply_on_hit(a_perks, damage=dmg, attacker_hp=a_hp, attacker_max_hp=a_max_hp)
                a_attacks += 1
                if verbose:
                    print(
                        f"  {attacker.name} -> {defender.name} "
                        f"({dmg:.1f} 피해, {defender.name} HP {max(d_hp, 0):.1f})"
                    )
            elif verbose:
                print(f"  {attacker.name} 공격 불가 (사거리/타겟 조건 미충족)")
            a_next += a_interval

        # defender attack
        if d_hp > 0 and time + eps >= d_next:
            if _can_attack_target(defender, attacker) and _is_in_attack_range(defender, attacker, distance):
                base = d_atk
                after = a_hp - base
                dmg = _maybe_execute(d_perks, target_hp_after=after, target_max_hp=a_max_hp, base_damage=base)
                a_hp -= dmg
                d_hp = _apply_on_hit(d_perks, damage=dmg, attacker_hp=d_hp, attacker_max_hp=d_max_hp)
                d_attacks += 1
                if verbose:
                    print(
                        f"  {defender.name} -> {attacker.name} "
                        f"({dmg:.1f} 피해, {attacker.name} HP {max(a_hp, 0):.1f})"
                    )
            elif verbose:
                print(f"  {defender.name} 공격 불가 (사거리/타겟 조건 미충족)")
            d_next += d_interval

    if a_hp > 0 and d_hp <= 0:
        winner = "attacker"
    elif d_hp > 0 and a_hp <= 0:
        winner = "defender"
    elif a_hp <= 0 and d_hp <= 0:
        winner = "draw"
    else:
        winner = "none"

    return {
        "winner": winner,
        "time": time,
        "attacker_final_hp": max(a_hp, 0.0),
        "defender_final_hp": max(d_hp, 0.0),
        "attacker_attacks": a_attacks,
        "defender_attacks": d_attacks,
        "attacker_start_pos": attacker_start_pos,
        "defender_start_pos": defender_start_pos,
        "attacker_final_pos": (ax, ay),
        "defender_final_pos": (dx, dy),
    }


def simulate_swarm_2d(
    attacker: Unit,
    defenders: List[Unit],
    attacker_pos: Tuple[float, float] = (0.0, 0.0),
    defender_positions: Optional[List[Tuple[float, float]]] = None,
    dt: float = 0.05,
    max_time: float = 60.0,
    verbose: bool = False,
) -> dict:
    """2D 좌표 기반 1:N 전투(스웜) 시뮬레이션.

    규칙(초기 버전):
    - 공격자는 가장 가까운 생존 수비자를 타겟팅
    - 수비자들은 공격자만 타겟팅
    - 이동: 서로를 향해 이동(가장 가까운 타겟/공격자)
    - Perk는 _effective_combat_stats(context="swarm") 기준으로 적용
    """
    ax, ay = attacker_pos
    a_stats = _effective_combat_stats(attacker, context="swarm")
    a_hp = float(a_stats["hp"])
    a_max_hp = a_hp
    a_as = float(a_stats["attack_speed"])
    a_atk = float(a_stats["atk"])
    a_move = float(a_stats["move_speed"])
    a_rng = float(a_stats["range"])
    a_perks = a_stats["perks"]

    # defender stats
    d_stats_list = [_effective_combat_stats(d, context="swarm") for d in defenders]
    d_hp = [float(s["hp"]) for s in d_stats_list]
    d_max_hp = d_hp[:]
    d_as = [float(s["attack_speed"]) for s in d_stats_list]
    d_atk = [float(s["atk"]) for s in d_stats_list]
    d_move = [float(s["move_speed"]) for s in d_stats_list]
    d_rng = [float(s["range"]) for s in d_stats_list]
    d_perks = [s["perks"] for s in d_stats_list]

    # positions
    if defender_positions is None:
        # 기본: 공격자 기준 오른쪽에 살짝 퍼뜨려 배치
        base_x, base_y = attacker_pos[0] + 5.0, attacker_pos[1]
        defender_positions = [(base_x + 0.6 * i, base_y + 0.4 * ((-1) ** i)) for i in range(len(defenders))]
    else:
        defender_positions = list(defender_positions)

    if len(defender_positions) != len(defenders):
        raise ValueError("defender_positions length must match defenders")

    # cooldowns
    a_cd = 0.0
    d_cd = [0.0 for _ in defenders]

    a_attacks = 0
    d_attacks = 0

    time = 0.0
    eps = 1e-9

    def _alive_indices() -> List[int]:
        return [i for i, hp in enumerate(d_hp) if hp > 0]

    def _dist_to(i: int) -> float:
        dx, dy = defender_positions[i]
        return math.hypot(dx - ax, dy - ay)

    def _nearest_alive() -> Optional[int]:
        alive = _alive_indices()
        if not alive:
            return None
        return min(alive, key=_dist_to)

    while time < max_time and a_hp > 0:
        alive = _alive_indices()
        if not alive:
            break

        target_i = _nearest_alive()
        assert target_i is not None

        # ---- movement ----
        # attacker -> target
        tx, ty = defender_positions[target_i]
        vec_x = tx - ax
        vec_y = ty - ay
        dist = math.hypot(vec_x, vec_y)
        if dist > eps:
            dir_x = vec_x / dist
            dir_y = vec_y / dist
        else:
            dir_x = dir_y = 0.0
        ax += a_move * dir_x * dt
        ay += a_move * dir_y * dt

        # defenders -> attacker
        for i in alive:
            dx, dy = defender_positions[i]
            vx = ax - dx
            vy = ay - dy
            dd = math.hypot(vx, vy)
            if dd > eps:
                ux = vx / dd
                uy = vy / dd
            else:
                ux = uy = 0.0
            defender_positions[i] = (dx + d_move[i] * ux * dt, dy + d_move[i] * uy * dt)

        # ---- cooldown tick ----
        a_cd = max(0.0, a_cd - dt)
        for i in alive:
            d_cd[i] = max(0.0, d_cd[i] - dt)

        # ---- attacks ----
        # attacker attack (single target + cleave)
        if a_as > 0 and a_cd <= eps:
            # recalc nearest + distance after move
            target_i = _nearest_alive()
            if target_i is not None:
                tx, ty = defender_positions[target_i]
                dist_t = math.hypot(tx - ax, ty - ay)
                if dist_t <= a_rng:
                    base = a_atk
                    after = d_hp[target_i] - base
                    dmg = _maybe_execute(a_perks, target_hp_after=after, target_max_hp=d_max_hp[target_i], base_damage=base)
                    d_hp[target_i] -= dmg
                    a_hp = _apply_on_hit(a_perks, damage=dmg, attacker_hp=a_hp, attacker_max_hp=a_max_hp)
                    a_attacks += 1

                    # cleave: 주변 1명에게 50% (swarm only)
                    if "cleave" in a_perks:
                        # 다른 생존자 중 가장 가까운 1명
                        others = [i for i in _alive_indices() if i != target_i]
                        if others:
                            # target 기준 거리
                            def _dist_to_target(j: int) -> float:
                                xj, yj = defender_positions[j]
                                return math.hypot(xj - tx, yj - ty)

                            splash_i = min(others, key=_dist_to_target)
                            if _dist_to_target(splash_i) <= 1.5:
                                splash = max(1.0, dmg * 0.5)
                                d_hp[splash_i] -= splash

                    a_cd = 1.0 / a_as

        # defenders attack attacker
        for i in alive:
            if d_as[i] <= 0:
                continue
            if d_cd[i] > eps:
                continue
            dx, dy = defender_positions[i]
            dist_a = math.hypot(dx - ax, dy - ay)
            if dist_a <= d_rng[i]:
                base = d_atk[i]
                after = a_hp - base
                dmg = _maybe_execute(d_perks[i], target_hp_after=after, target_max_hp=a_max_hp, base_damage=base)
                a_hp -= dmg
                d_hp[i] = _apply_on_hit(d_perks[i], damage=dmg, attacker_hp=d_hp[i], attacker_max_hp=d_max_hp[i])
                d_attacks += 1
                d_cd[i] = 1.0 / d_as[i]

        time += dt

        if verbose and int(time / dt) % 20 == 0:
            alive_cnt = len(_alive_indices())
            print(f"[t={time:.2f}] a_hp={a_hp:.1f} alive_def={alive_cnt}")

    if a_hp > 0 and not _alive_indices():
        winner = "attacker"
    elif a_hp <= 0:
        winner = "defender"
    else:
        winner = "none"

    return {
        "winner": winner,
        "time": time,
        "attacker_final_hp": max(a_hp, 0.0),
        "defender_final_hp": max(sum(max(h, 0.0) for h in d_hp), 0.0),
        "defenders_remaining": len(_alive_indices()),
        "attacker_attacks": a_attacks,
        "defender_attacks": d_attacks,
        "attacker_start_pos": attacker_pos,
        "defender_start_pos": defender_positions,
        "attacker_final_pos": (ax, ay),
        "defender_final_pos": defender_positions,
    }


def print_battle_summary(attacker: Unit, defender: Unit, result: dict) -> None:
    """전투 결과 요약 출력(1D/2D 공통)."""
    print("\n=== 전투 결과 요약 ===")
    print(f"승자                : {result.get('winner', 'none')}")
    print(f"총 경과 시간        : {float(result.get('time', 0.0)):.2f}초")
    print(f"공격자 공격 횟수    : {result.get('attacker_attacks', 0)}")
    print(f"방어자 공격 횟수    : {result.get('defender_attacks', 0)}")
    print(f"공격자 최종 HP      : {float(result.get('attacker_final_hp', 0.0)):.1f}")
    print(f"방어자 최종 HP      : {float(result.get('defender_final_hp', 0.0)):.1f}")

    if "attacker_start_pos" in result:
        print("\n[2D 좌표 정보]")
        print(f"공격자 시작/종료 좌표: {result.get('attacker_start_pos')} -> {result.get('attacker_final_pos')}")
        print(f"방어자 시작/종료 좌표: {result.get('defender_start_pos')} -> {result.get('defender_final_pos')}")
    print()


def build_experiment_summary(
    attacker: Unit,
    defender: Unit,
    trials: int,
    total_time: float,
    total_attacker_hp: float,
    total_defender_hp: float,
    total_attacker_attacks: int,
    total_defender_attacks: int,
    wins_attacker: int,
    wins_defender: int,
    draws: int,
    no_result: int,
) -> dict:
    """자동 전투 실험 결과를 1개의 dict로 정리(로그/AI 분석용)."""
    summary = {
        "attacker_name": attacker.name,
        "defender_name": defender.name,
        "attacker_level": attacker.level,
        "defender_level": defender.level,
        "trials": trials,
        "wins_attacker": wins_attacker,
        "wins_defender": wins_defender,
        "draws": draws,
        "no_result": no_result,
        "attacker_unit": attacker.to_dict(),
        "defender_unit": defender.to_dict(),
    }

    if trials > 0:
        summary.update(
            {
                "attacker_win_rate": wins_attacker / trials,
                "defender_win_rate": wins_defender / trials,
                "draw_rate": draws / trials,
                "no_result_rate": no_result / trials,
                "avg_time": total_time / trials,
                "avg_attacker_final_hp": total_attacker_hp / trials,
                "avg_defender_final_hp": total_defender_hp / trials,
                "avg_attacker_attacks": total_attacker_attacks / trials,
                "avg_defender_attacks": total_defender_attacks / trials,
            }
        )
    else:
        summary.update(
            {
                "attacker_win_rate": 0.0,
                "defender_win_rate": 0.0,
                "draw_rate": 0.0,
                "no_result_rate": 0.0,
                "avg_time": 0.0,
                "avg_attacker_final_hp": 0.0,
                "avg_defender_final_hp": 0.0,
                "avg_attacker_attacks": 0.0,
                "avg_defender_attacks": 0.0,
            }
        )

    return summary


def _normalize_name(name: str) -> str:
    return "".join(name.lower().split())


def _find_unit_by_name_fuzzy(units: List[Unit], query_name: str) -> Optional[Unit]:
    """이름 유사 매칭으로 Unit 찾기(최초 1개 반환)."""
    q = _normalize_name(query_name)
    if not q:
        return None

    # 1) exact normalize match
    for u in units:
        if _normalize_name(u.name) == q:
            return u

    # 2) contains
    for u in units:
        if q in _normalize_name(u.name):
            return u

    return None


def _make_unit_from_spec(spec: dict) -> Unit:
    """시나리오 spec(dict)로 임시 유닛 생성."""
    return Unit(
        name=spec.get("name", "Unknown"),
        level=int(spec.get("level", 1)),
        hp=int(spec.get("hp", 100)),
        atk=int(spec.get("atk", 10)),
        role=spec.get("role", "ground"),
        cost=int(spec.get("cost", 0)),
        range=int(spec.get("range", 1)),
        attack_speed=float(spec.get("attack_speed", 1.0)),
        move_speed=float(spec.get("move_speed", 1.0)),
        target_type=spec.get("target_type", "both"),
        attack_type=spec.get("attack_type", "melee"),
        perks=list(spec.get("perks") or []),
    )


def _run_duel_trials_2d(
    attacker: Unit,
    defender: Unit,
    trials: int,
    attacker_pos: Tuple[float, float] = (0.0, 0.0),
    defender_pos: Tuple[float, float] = (5.0, 0.0),
    verbose_each: bool = False,
) -> dict:
    """2D 듀얼을 trials만큼 반복 실행하고 요약 dict 반환."""
    wins_attacker = 0
    wins_defender = 0
    draws = 0
    no_result = 0

    total_time = 0.0
    total_attacker_hp = 0.0
    total_defender_hp = 0.0
    total_attacker_attacks = 0
    total_defender_attacks = 0

    for _ in range(trials):
        result = simulate_duel_2d(
            attacker=attacker,
            defender=defender,
            attacker_pos=attacker_pos,
            defender_pos=defender_pos,
            verbose=verbose_each,
        )

        total_time += result.get("time", 0.0)
        total_attacker_hp += result.get("attacker_final_hp", 0.0)
        total_defender_hp += result.get("defender_final_hp", 0.0)
        total_attacker_attacks += result.get("attacker_attacks", 0)
        total_defender_attacks += result.get("defender_attacks", 0)

        winner = result.get("winner", "none")
        if winner == "attacker":
            wins_attacker += 1
        elif winner == "defender":
            wins_defender += 1
        elif winner == "draw":
            draws += 1
        else:
            no_result += 1

    summary = build_experiment_summary(
        attacker=attacker,
        defender=defender,
        trials=trials,
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

    summary["attacker_pos"] = attacker_pos
    summary["defender_pos"] = defender_pos
    summary["encounter_type"] = "duel"
    summary["defender_count"] = 1
    return summary


def _run_swarm_trials_2d(
    attacker: Unit,
    defender_proto: Unit,
    defender_count: int,
    trials: int,
    attacker_pos: Tuple[float, float] = (0.0, 0.0),
    defender_pos: Tuple[float, float] = (5.0, 0.0),
    verbose_each: bool = False,
) -> dict:
    """2D 스웜을 trials만큼 반복 실행하고 요약 dict 반환."""
    wins_attacker = 0
    wins_defender = 0
    draws = 0
    no_result = 0

    total_time = 0.0
    total_attacker_hp = 0.0
    total_defender_hp = 0.0
    total_attacker_attacks = 0
    total_defender_attacks = 0
    total_defenders_remaining = 0

    for _ in range(trials):
        defenders = [Unit.from_dict(defender_proto.to_dict()) for _ in range(defender_count)]
        positions = [(defender_pos[0] + 0.6 * i, defender_pos[1] + 0.4 * ((-1) ** i)) for i in range(defender_count)]

        result = simulate_swarm_2d(
            attacker=attacker,
            defenders=defenders,
            attacker_pos=attacker_pos,
            defender_positions=positions,
            verbose=verbose_each,
        )

        total_time += result.get("time", 0.0)
        total_attacker_hp += result.get("attacker_final_hp", 0.0)
        total_defender_hp += result.get("defender_final_hp", 0.0)
        total_attacker_attacks += result.get("attacker_attacks", 0)
        total_defender_attacks += result.get("defender_attacks", 0)
        total_defenders_remaining += result.get("defenders_remaining", 0)

        winner = result.get("winner", "none")
        if winner == "attacker":
            wins_attacker += 1
        elif winner == "defender":
            wins_defender += 1
        elif winner == "draw":
            draws += 1
        else:
            no_result += 1

    summary = build_experiment_summary(
        attacker=attacker,
        defender=defender_proto,
        trials=trials,
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

    summary["attacker_pos"] = attacker_pos
    summary["defender_pos"] = defender_pos
    summary["encounter_type"] = "swarm"
    summary["defender_count"] = int(defender_count)
    if trials > 0:
        summary["avg_defenders_remaining"] = total_defenders_remaining / trials
    else:
        summary["avg_defenders_remaining"] = 0.0
    return summary


# ============================================================
# Public API wrappers (unit_logic.py에서 underscore 함수 import 방지용)
# ============================================================

def normalize_name(name: str) -> str:
    """이름 정규화(공백/대소문자)."""
    return _normalize_name(name)


def find_unit_by_name_fuzzy(units: List[Unit], query_name: str) -> Optional[Unit]:
    """저장된 유닛 목록에서 이름을 '느슨하게' 매칭해서 1개를 찾는다."""
    return _find_unit_by_name_fuzzy(units, query_name)


def make_unit_from_spec(spec: dict) -> Unit:
    """스펙(dict)으로 임시 Unit 생성."""
    return _make_unit_from_spec(spec)


def run_duel_trials_2d(
    attacker: Unit,
    defender: Unit,
    trials: int,
    attacker_pos: Tuple[float, float] = (0.0, 0.0),
    defender_pos: Tuple[float, float] = (5.0, 0.0),
    verbose_each: bool = False,
) -> dict:
    """2D 전투를 trials 만큼 반복 실행해서 build_experiment_summary() dict를 반환."""
    return _run_duel_trials_2d(
        attacker=attacker,
        defender=defender,
        trials=trials,
        attacker_pos=attacker_pos,
        defender_pos=defender_pos,
        verbose_each=verbose_each,
    )


def run_swarm_trials_2d(
    attacker: Unit,
    defender_template: Unit,
    defender_count: int,
    trials: int,
    attacker_pos: Tuple[float, float] = (0.0, 0.0),
    defender_pos: Tuple[float, float] = (5.0, 0.0),
    defender_spread: float | None = None,
    verbose_each: bool = False,
) -> Dict[str, Any]:
    """
    1대다(swarm) 전투를 간단하게 근사하는 유틸 함수.

    구현 아이디어:
    - defender_template를 HP/ATK가 defender_count 배인 '집단 유닛'으로 합쳐서
      1:1 전투를 돌린다. (simulate_duel_2d / _run_duel_trials_2d 그대로 재사용)
    - summary에는:
        - attacker_unit / defender_unit: 집단 유닛 기준 스펙(to_dict)
        - encounter_type: "swarm"
        - defender_count, defender_spread
      을 넣어서 export_dataset / 분석 쪽에서 구분 가능하게 만든다.
    """
    n = max(1, int(defender_count))

    # 집단 효과를 근사하기 위한 '합쳐진 수비 유닛'
    agg = Unit.from_dict(defender_template.to_dict())
    agg.name = f"{defender_template.name} x{n}"
    agg.hp *= n
    agg.atk *= n
    agg.cost *= n

    raw_summary = _run_duel_trials_2d(
        attacker=attacker,
        defender=agg,
        trials=trials,
        attacker_pos=attacker_pos,
        defender_pos=defender_pos,
        verbose_each=verbose_each,
    )

    summary = dict(raw_summary)
    summary["encounter_type"] = "swarm"
    summary["defender_count"] = n
    summary["defender_spread"] = defender_spread
    return summary

