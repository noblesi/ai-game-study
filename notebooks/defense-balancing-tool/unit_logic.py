"""유닛 관리/검색/통계와 1D/2D 전투 시뮬레이션, 자동 전투 실험 메뉴(UI)를 담당하는 모듈.

- 전투 "계산 로직"은 battle_sim.py에 분리되어 있으며,
  이 파일은 메뉴/입력/출력 흐름(UX)을 중심으로 유지한다.

이 모듈의 전투 시뮬레이션 함수들은 결과를 모두 같은 dict 포맷으로 반환한다.
(예: winner, time, attacker_final_hp, defender_final_hp, attacker_attacks, defender_attacks …)

이렇게 맞춰 두면 나중에 AI/밸런싱 실험에서
- 여러 전투 결과를 로그처럼 모아서 학습 데이터로 쓰거나,
- 유닛 밸런스 비교를 자동으로 돌릴 때
결과 처리를 공통 로직으로 만들기 쉽다.
"""

import math
import uuid
from typing import List, Optional, Tuple
from unit_model import Unit
from utils import input_int, input_non_empty, select_from_list, confirm_yes_no, append_jsonl
from battle_sim import (
    simulate_duel,
    simulate_duel_2d,
    print_battle_summary,
    build_experiment_summary,
    find_unit_by_name_fuzzy,
    make_unit_from_spec,
    run_duel_trials_2d,
)

from scenario_loader import load_scenarios_from_markdown

# ============================
# 로그 스키마 v1 (SSOT)
# ============================

LOG_SCHEMA_VERSION = "v1"

def _new_log_envelope(kind: str, engine: str) -> dict:
    """JSONL 로그 레코드의 공통 메타(스키마/엔진/런ID)를 생성."""
    return {
        "schema_version": LOG_SCHEMA_VERSION,
        "kind": kind,
        "engine": engine,
        "run_id": str(uuid.uuid4()),
    }


# ============================
# 공통 유틸 함수들
# ============================

def _input_float(prompt: str, allow_negative: bool = False) -> float:
    ##소수 입력용 공통 함수 (이 파일에서만 사용)##
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("빈 값은 입력할 수 없습니다. 다시 입력해주세요.")
            continue

        try:
            value = float(raw)
        except ValueError:
            print("실수를 입력해주세요. 예: 1, 1.5, 0.75")
            continue

        if not allow_negative and value < 0:
            print("음수는 입력할 수 없습니다. 다시 입력해주세요.")
            continue

        return value


def format_unit_brief(unit: Unit) -> str:
    ##유닛 1줄 요약 포맷##
    return (
        f"{unit.name} "
        f"(Lv.{unit.level} / HP:{unit.hp} / ATK:{unit.atk} / "
        f"Role:{unit.role} / Type:{unit.attack_type} / "
        f"Cost:{unit.cost} / Range:{unit.range})"
    )


def print_unit_detail(unit: Unit) -> None:
    ##유닛 상세 정보 출력##
    print("\n[선택된 유닛 정보]")
    print(f"이름        : {unit.name}")
    print(f"역할(Role) : {unit.role}")
    print(f"레벨       : {unit.level}")
    print(f"HP         : {unit.hp}")
    print(f"ATK        : {unit.atk}")
    print(f"코스트      : {unit.cost}")
    print(f"사거리      : {unit.range}")
    print(f"공격 속도   : {unit.attack_speed}")
    print(f"이동 속도   : {unit.move_speed}")
    print(f"타겟 타입   : {unit.target_type}")
    print(f"공격 타입   : {unit.attack_type}\n")


# ============================
# 유닛 목록/검색/선택
# ============================

def print_units(units: List[Unit]) -> None:
    ##유닛 목록 출력##
    if not units:
        print("\n등록된 유닛이 없습니다.\n")
        return

    print("\n=== 유닛 목록 ===")
    for i, unit in enumerate(units, start=1):
        print(f"{i}. {format_unit_brief(unit)}")
    print()


def search_units(units: List[Unit], keyword: str) -> List[Tuple[int, Unit]]:
    ##키워드로 유닛 검색 (원본 index, Unit) 반환##
    keyword = (keyword or "").strip().lower()
    if not keyword:
        return []

    results: List[Tuple[int, Unit]] = []
    for idx, unit in enumerate(units):
        if keyword in unit.name.lower():
            results.append((idx, unit))
    return results


def search_unit_menu(units: List[Unit]) -> None:
    ##검색만 수행하고 결과를 출력하는 메뉴##
    if not units:
        print("\n[알림] 등록된 유닛이 없습니다.\n")
        return

    keyword = input_non_empty("검색할 키워드를 입력하세요: ")
    results = search_units(units, keyword)

    if not results:
        print("\n검색 결과가 없습니다.\n")
        return

    print("\n=== 검색 결과 ===")
    for i, (_, unit) in enumerate(results, start=1):
        print(f"{i}. {format_unit_brief(unit)}")
    print()


def search_unit_menu_for_select(units: List[Unit]) -> Optional[int]:
    ##검색 → 결과 목록 → 번호 선택 → 원본 units 인덱스 반환##
    if not units:
        print("\n[알림] 등록된 유닛이 없습니다.\n")
        return None

    keyword = input_non_empty("검색할 키워드를 입력하세요: ")
    results = search_units(units, keyword)

    if not results:
        print("\n검색 결과가 없습니다.\n")
        return None

    print("\n=== 검색 결과 ===")
    for i, (_, unit) in enumerate(results, start=1):
        print(f"{i}. {format_unit_brief(unit)}")
    print("0. 취소")

    while True:
        sel = input("번호를 선택하세요: ").strip()
        try:
            num = int(sel)
        except ValueError:
            print("숫자를 입력해주세요.")
            continue

        if num == 0:
            return None
        if 1 <= num <= len(results):
            original_index = results[num - 1][0]
            return original_index

        print("범위를 벗어났습니다. 다시 입력해주세요.")


# ============================
# 유닛 추가/수정/삭제/레벨업
# ============================

def add_unit_menu(units: List[Unit]) -> None:
    ##유닛 추가 메뉴##
    print("\n[유닛 추가하기]")

    name = input_non_empty("유닛 이름을 입력하세요: ")

    # 중복 이름 체크(선택)
    if any(u.name.lower() == name.lower() for u in units):
        if not confirm_yes_no("같은 이름의 유닛이 이미 있습니다. 그래도 추가할까요? (y/n): "):
            print("유닛 추가를 취소합니다.\n")
            return

    role = input("역할(Role)을 입력하세요(예: defender/ground_enemy/air_enemy/tower): ").strip() or "ground"
    level = input_int("레벨을 입력하세요(정수): ")
    hp = input_int("HP를 입력하세요(정수): ")
    atk = input_int("ATK를 입력하세요(정수): ")
    cost = input_int("코스트를 입력하세요(정수): ")
    rng = input_int("사거리(range)를 입력하세요(정수): ")
    attack_speed = _input_float("공격 속도(초당 공격 횟수)를 입력하세요(예: 1.0): ")
    move_speed = _input_float("이동 속도(초당 이동 거리)를 입력하세요(예: 1.0): ", allow_negative=False)
    target_type = input("타겟 타입(target_type: ground/air/tower/both): ").strip() or "both"
    attack_type = input("공격 타입(attack_type: melee/ranged/magic...): ").strip() or "melee"

    unit = Unit(
        name=name,
        level=level,
        hp=hp,
        atk=atk,
        role=role,
        cost=cost,
        range=rng,
        attack_speed=attack_speed,
        move_speed=move_speed,
        target_type=target_type,
        attack_type=attack_type,
    )

    units.append(unit)
    print("\n유닛이 추가되었습니다.\n")


def level_up_unit_menu(units: List[Unit]) -> None:
    ##유닛 레벨업 메뉴##
    if not units:
        print("\n[알림] 등록된 유닛이 없습니다.\n")
        return

    print("\n[유닛 레벨 올리기]")
    idx = search_unit_menu_for_select(units)
    if idx is None:
        print("레벨업을 취소합니다.\n")
        return

    unit = units[idx]
    unit.level_up()
    print(f"\n{unit.name}이(가) 레벨업! (Lv.{unit.level}, HP:{unit.hp}, ATK:{unit.atk})\n")


def remove_unit_menu(units: List[Unit]) -> None:
    ##유닛 삭제 메뉴##
    if not units:
        print("\n[알림] 등록된 유닛이 없습니다.\n")
        return

    print("\n[유닛 삭제하기]")
    idx = search_unit_menu_for_select(units)
    if idx is None:
        print("삭제를 취소합니다.\n")
        return

    unit = units[idx]
    print_unit_detail(unit)

    if confirm_yes_no("정말 삭제할까요? (y/n): "):
        units.pop(idx)
        print("삭제되었습니다.\n")
    else:
        print("삭제를 취소했습니다.\n")


def edit_unit_menu(units: List[Unit]) -> None:
    ##유닛 정보 수정 메뉴##
    if not units:
        print("\n[알림] 등록된 유닛이 없습니다.\n")
        return

    print("\n[유닛 정보 수정하기]")
    idx = search_unit_menu_for_select(units)
    if idx is None:
        print("수정을 취소합니다.\n")
        return

    unit = units[idx]
    print_unit_detail(unit)

    while True:
        print("수정할 항목을 선택하세요:")
        print("1) 이름")
        print("2) 역할(Role)")
        print("3) 레벨")
        print("4) HP")
        print("5) ATK")
        print("6) 코스트")
        print("7) 사거리(range)")
        print("8) 공격 속도(attack_speed)")
        print("9) 이동 속도(move_speed)")
        print("10) 타겟 타입(target_type)")
        print("11) 공격 타입(attack_type)")
        print("0) 완료")

        choice = input("번호를 선택하세요: ").strip()

        if choice == "0":
            print("수정을 완료했습니다.\n")
            return
        elif choice == "1":
            unit.name = input_non_empty("새 이름: ")
        elif choice == "2":
            unit.role = input("새 역할(Role): ").strip() or unit.role
        elif choice == "3":
            unit.level = input_int("새 레벨(정수): ")
        elif choice == "4":
            unit.hp = input_int("새 HP(정수): ")
        elif choice == "5":
            unit.atk = input_int("새 ATK(정수): ")
        elif choice == "6":
            unit.cost = input_int("새 코스트(정수): ")
        elif choice == "7":
            unit.range = input_int("새 사거리(range)(정수): ")
        elif choice == "8":
            unit.attack_speed = _input_float("새 공격 속도(예: 1.0): ")
        elif choice == "9":
            unit.move_speed = _input_float("새 이동 속도(예: 1.0): ", allow_negative=False)
        elif choice == "10":
            unit.target_type = input("새 타겟 타입(ground/air/tower/both): ").strip() or unit.target_type
        elif choice == "11":
            unit.attack_type = input("새 공격 타입(melee/ranged/magic...): ").strip() or unit.attack_type
        else:
            print("잘못된 선택입니다. 다시 입력해주세요.")

        print("\n[변경 후 유닛 정보]")
        print_unit_detail(unit)


# ============================
# 통계/프리셋/대량 작업
# ============================

def print_units_stats(units: List[Unit]) -> None:
    ##유닛 통계 출력##
    if not units:
        print("\n[알림] 등록된 유닛이 없습니다.\n")
        return

    avg_level = sum(u.level for u in units) / len(units)
    avg_hp = sum(u.hp for u in units) / len(units)
    avg_atk = sum(u.atk for u in units) / len(units)

    print("\n=== 유닛 통계 ===")
    print(f"총 유닛 수 : {len(units)}")
    print(f"평균 레벨  : {avg_level:.2f}")
    print(f"평균 HP    : {avg_hp:.2f}")
    print(f"평균 ATK   : {avg_atk:.2f}\n")


def bulk_add_units_menu(units: List[Unit]) -> None:
    ##유닛 대량 추가(프리셋)##
    presets = [
        Unit("Knight", 1, 200, 25, role="defender", cost=3, range=1, attack_speed=1.0, move_speed=1.0, target_type="ground", attack_type="melee"),
        Unit("Archer", 1, 120, 18, role="defender", cost=2, range=4, attack_speed=1.2, move_speed=1.0, target_type="ground", attack_type="ranged"),
        Unit("Goblin", 1, 100, 15, role="ground_enemy", cost=1, range=1, attack_speed=1.2, move_speed=1.2, target_type="tower", attack_type="melee"),
        Unit("Wyvern", 1, 180, 30, role="air_enemy", cost=4, range=1, attack_speed=1.0, move_speed=1.5, target_type="tower", attack_type="melee"),
        Unit("AntiAirTower", 1, 150, 40, role="tower", cost=5, range=4, attack_speed=0.8, move_speed=0.0, target_type="air", attack_type="ranged"),
    ]

    print("\n[유닛 대량 추가(프리셋)]")
    print("아래 프리셋 유닛들을 한 번에 추가합니다.")
    for u in presets:
        print(f"- {format_unit_brief(u)}")

    if not confirm_yes_no("추가할까요? (y/n): "):
        print("취소했습니다.\n")
        return

    units.extend(presets)
    print("\n프리셋 유닛을 추가했습니다.\n")


def bulk_level_up_menu(units: List[Unit]) -> None:
    ##테스트용 대량 레벨업##
    if not units:
        print("\n[알림] 등록된 유닛이 없습니다.\n")
        return

    print("\n[유닛 대량 레벨업(테스트용)]")
    amount = input_int("모든 유닛을 몇 레벨 올릴까요? (정수): ")
    if amount <= 0:
        print("0 이하 입력으로 취소했습니다.\n")
        return

    for u in units:
        u.level += amount
        u.hp += u.hp_per_level * amount
        u.atk += u.atk_per_level * amount
    print(f"\n모든 유닛 레벨을 +{amount} 했습니다. (HP/ATK 성장치 포함)\n")


# ============================
# 전투 메뉴(UI)
# ============================

def battle_simulation_menu(units: List[Unit]) -> None:
    ##유닛 2개를 골라 1:1 전투를 시뮬레이션하는 메뉴##
    if not units:
        print("\n[알림] 등록된 유닛이 없습니다. 먼저 유닛을 추가하세요.\n")
        return

    print("\n[전투 시뮬레이션 - 1 대 1]")
    print("선택한 두 유닛이 현재 스탯(HP / ATK / 공격 속도 기준)으로 싸웠을 때,")
    print("어느 쪽이 이기는지와 걸리는 시간을 확인할 수 있습니다.\n")

    print("[공격자 선택]")
    attacker_index = search_unit_menu_for_select(units)
    if attacker_index is None:
        print("전투 시뮬레이션을 취소합니다.\n")
        return

    print("[방어자 선택]")
    defender_index = search_unit_menu_for_select(units)
    if defender_index is None:
        print("전투 시뮬레이션을 취소합니다.\n")
        return

    attacker = units[attacker_index]
    defender = units[defender_index]

    print("\n=== 선택된 유닛 ===")
    print("[공격자]")
    print_unit_detail(attacker)
    print("[방어자]")
    print_unit_detail(defender)

    if not confirm_yes_no("이 구성으로 전투 시뮬레이션을 실행할까요? (y/n): "):
        print("전투 시뮬레이션을 취소했습니다.\n")
        return

    verbose = confirm_yes_no("전투 로그를 턴마다 출력할까요? (y/n): ")

    print("\n=== 전투 시작 ===")
    result = simulate_duel_2d(attacker, defender, verbose=verbose)
    print_battle_summary(attacker, defender, result)


def auto_battle_experiment_menu(units: List[Unit]) -> None:
    """전투 실험 자동화 메뉴."""
    if not units:
        print("\n[알림] 등록된 유닛이 없습니다. 먼저 유닛을 추가하세요.\n")
        return

    print("\n[자동 전투 실험]")
    print("선택한 두 유닛을 여러 번 싸우게 해서(동일 조건 반복),")
    print("승률/평균 전투 시간/평균 남은 HP 등을 요약합니다.\n")

    print("[공격자 선택]")
    attacker_index = search_unit_menu_for_select(units)
    if attacker_index is None:
        print("자동 전투 실험을 취소합니다.\n")
        return

    print("[방어자 선택]")
    defender_index = search_unit_menu_for_select(units)
    if defender_index is None:
        print("자동 전투 실험을 취소합니다.\n")
        return

    attacker = units[attacker_index]
    defender = units[defender_index]

    trials = input_int("실험 횟수(trials)를 입력하세요 (예: 100): ")
    if trials <= 0:
        print("실험 횟수는 1 이상이어야 합니다.\n")
        return

    print("\n전투 모델을 선택하세요:")
    print("1) 1D (거리 감소 + 사거리 판정)")
    print("2) 2D (좌표 이동 + 사거리 판정)")
    mode = input("번호를 선택하세요 (기본: 2): ").strip() or "2"

    verbose_each = confirm_yes_no("각 전투의 로그를 출력할까요? (y/n): ")

    wins_attacker = 0
    wins_defender = 0
    draws = 0
    no_result = 0

    total_time = 0.0
    total_attacker_hp = 0.0
    total_defender_hp = 0.0
    total_attacker_attacks = 0
    total_defender_attacks = 0

    print("\n=== 자동 전투 실험 시작 ===")
    for i in range(trials):
        if mode == "1":
            result = simulate_duel(attacker, defender, verbose=verbose_each)
        else:
            result = simulate_duel_2d(attacker, defender, verbose=verbose_each)

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

        if not verbose_each and (i + 1) % max(1, trials // 10) == 0:
            print(f"  진행 중... {i+1}/{trials}")

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

    print("\n=== 실험 결과 요약(dict) ===")
    print(summary)
    print()

    if confirm_yes_no("이 결과를 JSONL로 저장할까요? (y/n): "):
        path = input("저장 경로(기본: logs/experiments.jsonl): ").strip() or "logs/experiments.jsonl"
        record = {
            **_new_log_envelope("auto_experiment", "simulate_duel" if mode == "1" else "simulate_duel_2d"),
            "spec_source": "units_runtime",
            "summary": summary,
        }
        append_jsonl(path, record)

        print(f"[저장 완료] {path}\n")

def battle_scenarios_menu(units: List[Unit]) -> None:
    """battle_scenarios_*.md에 맞춘 '프리셋 시나리오' 실행 메뉴."""
    md_scenarios = load_scenarios_from_markdown()
    if md_scenarios:
        scenarios = md_scenarios
    else:
        scenarios = [
        {
            "title": "Knight vs Goblin (근접 기본 밸런스)",
            "attacker_spec": {
                "name": "Knight",
                "level": 1,
                "hp": 200,
                "atk": 25,
                "role": "defender",
                "range": 1,
                "attack_speed": 1.0,
                "move_speed": 1.0,
                "target_type": "ground",
                "attack_type": "melee",
            },
            "defender_spec": {
                "name": "Goblin",
                "level": 1,
                "hp": 100,
                "atk": 15,
                "role": "ground",
                "range": 1,
                "attack_speed": 1.2,
                "move_speed": 1.2,
                "target_type": "ground",
                "attack_type": "melee",
            },
            "trials": 100,
            "attacker_pos": (0.0, 0.0),
            "defender_pos": (5.0, 0.0),
            "verbose_each": False,
        },
        {
            "title": "AntiAirTower vs Wyvern (대공 타워 검증)",
            "attacker_spec": {
                "name": "AntiAirTower",
                "level": 1,
                "hp": 150,
                "atk": 40,
                "role": "tower",
                "range": 4,
                "attack_speed": 0.8,
                "move_speed": 0.0,
                "target_type": "air",
                "attack_type": "ranged",
            },
            "defender_spec": {
                "name": "Wyvern",
                "level": 1,
                "hp": 180,
                "atk": 30,
                "role": "air_enemy",
                "range": 1,
                "attack_speed": 1.0,
                "move_speed": 1.5,
                "target_type": "tower",
                "attack_type": "melee",
            },
            "trials": 100,
            "attacker_pos": (0.0, 0.0),
            "defender_pos": (6.0, 0.0),
            "verbose_each": False,
        },
        {
            "title": "Assassin vs Giant (속도/공속 상성 테스트)",
            "attacker_spec": {
                "name": "Assassin",
                "level": 1,
                "hp": 80,
                "atk": 35,
                "role": "ground",
                "range": 1,
                "attack_speed": 1.8,
                "move_speed": 1.8,
                "target_type": "ground",
                "attack_type": "melee",
            },
            "defender_spec": {
                "name": "Giant",
                "level": 1,
                "hp": 300,
                "atk": 60,
                "role": "ground_enemy",
                "range": 1,
                "attack_speed": 0.6,
                "move_speed": 0.6,
                "target_type": "ground",
                "attack_type": "melee",
            },
            "trials": 100,
            "attacker_pos": (0.0, 0.0),
            "defender_pos": (4.0, 0.0),
            "verbose_each": False,
        },
    ]

    print("\n=== 전투 시나리오 프리셋 ===")
    for i, s in enumerate(scenarios, start=1):
        print(f"{i}) {s['title']}")
    print("0) 취소")

    sel = input("번호를 선택하세요: ").strip()
    if sel == "0":
        print("취소했습니다.\n")
        return
    try:
        idx = int(sel) - 1
        if idx < 0 or idx >= len(scenarios):
            raise ValueError
    except ValueError:
        print("잘못된 번호입니다.\n")
        return

    scenario = scenarios[idx]

    # 시나리오 실행은 "시나리오 스펙"을 단일 소스(SSOT)로 사용한다.
    # units.json 스펙과 섞이면 결과 재현/비교가 어려워질 수 있다.
    attacker = make_unit_from_spec(scenario["attacker_spec"])
    defender = make_unit_from_spec(scenario["defender_spec"])
    trials = int(scenario.get("trials", 100))
    attacker_pos = tuple(scenario.get("attacker_pos", (0.0, 0.0)))
    defender_pos = tuple(scenario.get("defender_pos", (5.0, 0.0)))
    verbose_each = bool(scenario.get("verbose_each", False))

    print("\n=== 선택된 시나리오 ===")
    print(f"- {scenario['title']}")
    print(f"- trials: {trials}")
    print(f"- attacker_pos: {attacker_pos}")
    print(f"- defender_pos: {defender_pos}\n")

    print("[공격자]")
    print_unit_detail(attacker)
    print("[방어자]")
    print_unit_detail(defender)

    if not confirm_yes_no("이 구성으로 시나리오 실험을 실행할까요? (y/n): "):
        print("시나리오 실행을 취소했습니다.\n")
        return

    print("\n=== 자동 전투 실험 시작 ===")
    summary = run_duel_trials_2d(
        attacker=attacker,
        defender=defender,
        trials=trials,
        attacker_pos=attacker_pos,
        defender_pos=defender_pos,
        verbose_each=verbose_each,
    )

    print("\n=== 시나리오 실험 요약(dict) ===")
    print(summary)
    print()

    if confirm_yes_no("이 결과를 JSONL로 저장할까요? (y/n): "):
        path = input("저장 경로(기본: logs/scenarios.jsonl): ").strip() or "logs/scenarios.jsonl"
        record = {
            **_new_log_envelope("scenario_preset", "run_duel_trials_2d"),
            "scenario_title": scenario.get("title"),
            "scenario_source": scenario.get("_source"),
            "spec_source": "scenario_spec",
            "scenario_spec": scenario,
            "summary": summary,
        }

        append_jsonl(path, record)
        print(f"[저장 완료] {path}\n")
