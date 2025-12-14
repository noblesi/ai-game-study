"""전투 시뮬레이션(1D/2D) + 자동 실험용 요약 로직 모듈.

- unit_model.Unit을 입력으로 받아 전투를 시뮬레이션하고,
- 결과를 공통 dict 포맷(winner/time/... )으로 반환한다.

주의:
- 이 파일은 '계산 로직' 위주로 유지한다.
- 콘솔 메뉴(UI)는 unit_logic.py 쪽에서 담당한다.
"""

import math
from typing import List, Optional, Tuple

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


def simulate_duel(
    attacker: Unit,
    defender: Unit,
    initial_distance: float = 5.0,
    verbose: bool = True,
) -> dict:
    """1D 거리 기반 1:1 전투(시간 이벤트 방식)."""
    a_hp = float(attacker.hp)
    d_hp = float(defender.hp)

    if attacker.attack_speed <= 0 and defender.attack_speed <= 0:
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

    a_interval = math.inf if attacker.attack_speed <= 0 else 1.0 / attacker.attack_speed
    d_interval = math.inf if defender.attack_speed <= 0 else 1.0 / defender.attack_speed

    time = 0.0
    next_a = 0.0 if a_interval < math.inf else math.inf
    next_d = 0.0 if d_interval < math.inf else math.inf
    a_attacks = 0
    d_attacks = 0

    rel_speed = max(attacker.move_speed, 0.0) + max(defender.move_speed, 0.0)
    eps = 1e-9
    max_steps = 10000

    def _max_effective_range(u: Unit) -> float:
        if u.attack_speed <= 0:
            return 0.0
        if (u.attack_type or "").lower() == "melee":
            return 1.0
        return float(u.range)

    max_range = max(_max_effective_range(attacker), _max_effective_range(defender))
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
                d_hp -= attacker.atk
                a_attacks += 1
                if verbose:
                    print(
                        f"  {attacker.name} -> {defender.name} "
                        f"({attacker.atk} 피해, {defender.name} HP {max(d_hp, 0):.1f})"
                    )
            elif verbose:
                print(f"  {attacker.name} 공격 불가 (사거리/타겟 조건 미충족)")
            next_a += a_interval

        # defender attack
        if d_hp > 0 and next_d <= next_event + eps:
            if _can_attack_target(defender, attacker) and _is_in_attack_range(defender, attacker, distance):
                a_hp -= defender.atk
                d_attacks += 1
                if verbose:
                    print(
                        f"  {defender.name} -> {attacker.name} "
                        f"({defender.atk} 피해, {attacker.name} HP {max(a_hp, 0):.1f})"
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

    a_hp = float(attacker.hp)
    d_hp = float(defender.hp)

    if attacker.attack_speed <= 0 and defender.attack_speed <= 0:
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

    a_interval = math.inf if attacker.attack_speed <= 0 else 1.0 / attacker.attack_speed
    d_interval = math.inf if defender.attack_speed <= 0 else 1.0 / defender.attack_speed

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
        if attacker.move_speed > 0 or defender.move_speed > 0:
            vec_x = dx - ax
            vec_y = dy - ay
            dist = math.hypot(vec_x, vec_y)
            if dist > 0:
                dir_x = vec_x / dist
                dir_y = vec_y / dist
            else:
                dir_x = dir_y = 0.0

            ax += attacker.move_speed * dir_x * move_dt
            ay += attacker.move_speed * dir_y * move_dt

            dx -= defender.move_speed * dir_x * move_dt
            dy -= defender.move_speed * dir_y * move_dt

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
                d_hp -= attacker.atk
                a_attacks += 1
                if verbose:
                    print(
                        f"  {attacker.name} -> {defender.name} "
                        f"({attacker.atk} 피해, {defender.name} HP {max(d_hp, 0):.1f})"
                    )
            elif verbose:
                print(f"  {attacker.name} 공격 불가 (사거리/타겟 조건 미충족)")
            a_next += a_interval

        # defender attack
        if d_hp > 0 and time + eps >= d_next:
            if _can_attack_target(defender, attacker) and _is_in_attack_range(defender, attacker, distance):
                a_hp -= defender.atk
                d_attacks += 1
                if verbose:
                    print(
                        f"  {defender.name} -> {attacker.name} "
                        f"({defender.atk} 피해, {attacker.name} HP {max(a_hp, 0):.1f})"
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
