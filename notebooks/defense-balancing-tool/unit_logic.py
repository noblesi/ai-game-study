from typing import List, Optional, Tuple
from unit_model import Unit
from utils import input_int, input_non_empty, select_from_list, confirm_yes_no

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
            print("음수는 입력할 수 없습니다.")
            continue

        return value

def format_unit_brief(unit: Unit) -> str:
    ##유닛 한 줄 표기 형식 공통화##
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
    print(f"공격 타입   : {unit.attack_type}")
    print(f"공격 속도   : {unit.attack_speed}")
    print(f"이동 속도   : {unit.move_speed}")
    print(f"타겟 타입   : {unit.target_type}")
    print(f"레벨당 HP   : {unit.hp_per_level}")
    print(f"레벨당 ATK  : {unit.atk_per_level}\n")

def search_units(units: List[Unit], keyword: str) -> List[Tuple[int, Unit]]:
    ##이름에 keyword가 포함된 유닛을 (원본 인덱스, Unit) 튜플 목록으로 반환한다.##
    result: List[Tuple[int, Unit]] = []
    keyword = keyword.strip().lower()
    if not keyword:
        return result

    for i, unit in enumerate(units):
        if keyword in unit.name.lower():
            result.append((i, unit))

    return result

def render_search_item(item: Tuple[int, Unit], display_idx: int) -> None:
    ##검색 결과 한 줄 출력 전용 함수 (select_from_list와도 함께 사용)##
    _idx, unit = item
    print(f"{display_idx}. {format_unit_brief(unit)}")

def print_search_results(results: List[Tuple[int, Unit]], keyword: str) -> None:
    ##검색결과 목록 전체를 출력하는 함수##
    print(f"\n=== '{keyword}' 검색 결과 ({len(results)}개) ===")
    for display_idx, item in enumerate(results, start=1):
        render_search_item(item, display_idx)
    print()

def print_indexed_results(results: List[Tuple[int, Unit]], description: str) -> None:
    ##(원본인덱스, Unit) 리스트를 출력하는 공통함수##
    if not results:
        print(f"\n[알림] 조건에 맞는 유닛이 없습니다. ({description})\n")
        return
    
    print(f"\n=== {description} ({len(results)}개) ===")
    for display_idx, (_, unit) in enumerate(results, start=1):
        render_search_item((0, unit), display_idx)
    print()

def print_units_stats(units: List[Unit]) -> None:
    ##유닛들의 기본통계를 출력하는 함수##
    if not units:
        print("\n등록된 유닛이 없습니다. 통계를 표시할 수 없습니다.\n")
        return
    
    count = len(units)
    total_level = sum(u.level for u in units)
    total_hp = sum(u.hp for u in units)
    total_atk = sum(u.atk for u in units)
    total_dps = sum(u.atk * u.attack_speed for u in units)  

    avg_level = total_level / count
    avg_hp = total_hp / count
    avg_atk = total_atk / count
    avg_dps = total_dps / count  

    highest_level_unit = max(units, key=lambda u: u.level)
    highest_atk_unit = max(units, key=lambda u: u.atk)
    highest_dps_unit = max(units, key=lambda u: u.atk * u.attack_speed) 

    print("\n=== 유닛 통계 ===")
    print(f"총 유닛 수: {count}")
    print(f"평균 레벨: {avg_level:.1f}")
    print(f"평균 HP   : {avg_hp:.1f}")
    print(f"평균 ATK  : {avg_atk:.1f}")
    print(f"평균 DPS  : {avg_dps:.1f}")
    print()
    print(f"최고 레벨 유닛: {format_unit_brief(highest_level_unit)}")
    print(f"최고 ATK 유닛 : {format_unit_brief(highest_atk_unit)}")
    print(f"최고 DPS 유닛 : {format_unit_brief(highest_dps_unit)}")
    print()

# ============================
# 메뉴 함수들
# ============================

def print_units(units: List[Unit]) -> None:
    ##등록된 유닛 목록을 출력한다##
    if not units:
        print("\n등록된 유닛이 없습니다.\n")
        return
    
    print("\n=== 유닛 목록 ===")
    for i, unit in enumerate(units, start = 1):
        print(f"{i}. {format_unit_brief(unit)}")
    print()

def add_unit_menu(units: List[Unit]) -> None:
    print("\n[유닛 추가하기]")

    name = input_non_empty("유닛 이름을 입력하세요: ")

    level = input_int("레벨을 입력하세요(0 이상의 정수): ")
    hp = input_int("HP를 입력하세요(0 이상의 정수): ")
    atk = input_int("ATK를 입력하세요(0 이상의 정수): ")

    role_raw = input(
        "역할을 입력하세요 (tower/enemy/hero, 기본값: tower): "
    ).strip()
    role = role_raw or "tower"

    range_ = input_int("사거리를 입력하세요(0 이상의 정수): ", allow_negative=False)
    cost = input_int("코스트를 입력하세요(0 이상의 정수): ", allow_negative=False)

    target_raw = input(
        "타겟 타입을 입력하세요 (ground/air/both, 기본값: ground): "
    ).strip()
    target_type = target_raw or "ground"

    attack_raw = input(
        "공격 타입을 입력하세요 (melee/ranged/magic, 기본값: melee): "
    ).strip()
    attack_type = attack_raw or "melee"

    unit = Unit(
        name=name,
        level=level,
        hp=hp,
        atk=atk,
        role=role,
        range=range_,
        cost=cost,
        target_type=target_type,
        attack_type=attack_type,   
    )
    units.append(unit)
    print(f"'{name}' 유닛을 추가했습니다.\n")


def level_up_unit_menu(units: List[Unit]) -> None:
    if not units:
        print("\n등록된 유닛이 없어서 레벨을 올릴 수 없습니다.\n")
        return

    print("\n[유닛 레벨 올리기]")

    selected_index = search_unit_menu_for_select(units)
    if selected_index is None:
        return

    unit = units[selected_index]
    before_level = unit.level
    unit.level_up()

    print(f"[완료] {unit.name}의 레벨이 {before_level} -> {unit.level}로 올랐습니다.\n")

def bulk_level_up_menu(units: List[Unit]) -> None:
    ##여러 유닛의 레벨을 한 번에 올리는 메뉴##
    if not units:
        print("\n등록된 유닛이 없어서 레벨을 올릴 수 없습니다.\n")
        return
    
    print("\n[여러 유닛 일괄 레벨 올리기]")
    print("1) 전체 유닛 레벨 올리기")
    print("2) 검색 결과에 포함된 유닛만 레벨 올리기")
    print("0) 취소")

    choice = input("번호를 선택하세요: ").strip()

    if choice == "1":
        delta = input_int("몇 레벨을 올리겠습니까? (0 이상의 정수): ", allow_negative=False)
        if delta <= 0:
            print("0 이하는 변경이 없습니다. 일괄 레벨업을 취소합니다.\n")
            return

        if not confirm_yes_no(f"정말 모든 유닛의 레벨을 {delta}만큼 올리시겠습니까? (y/n): "):
            print("일괄 레벨업을 취소했습니다.\n")
            return

        for unit in units:
            for _ in range(delta):
                unit.level_up()

        print(f"[완료] 총 {len(units)}개 유닛의 레벨을 {delta}만큼 올렸습니다.\n")

    elif choice == "2":
        keyword = input_non_empty("검색할 이름(또는 일부)을 입력하세요: ")
        search_results = search_units(units, keyword)

        if not search_results:
            print("검색 결과가 없습니다. 일괄 레벨업을 취소합니다.\n")
            return

        print_search_results(search_results, keyword)

        delta = input_int("몇 레벨을 올리겠습니까? (0 이상의 정수): ", allow_negative=False)
        if delta <= 0:
            print("0 이하는 변경이 없습니다. 일괄 레벨업을 취소합니다.\n")
            return

        if not confirm_yes_no(
            f"검색된 {len(search_results)}개 유닛의 레벨을 {delta}만큼 올리시겠습니까? (y/n): "
        ):
            print("일괄 레벨업을 취소했습니다.\n")
            return

        for _, unit in search_results:
            for _ in range(delta):
                unit.level_up()

        print(f"[완료] 검색된 {len(search_results)}개 유닛의 레벨을 {delta}만큼 올렸습니다.\n")

    elif choice == "0":
        print("일괄 레벨업을 취소했습니다.\n")
        return

    else:
        print("잘못된 번호입니다. 0~2 중에서 선택해주세요.\n")


def remove_unit_menu(units: List[Unit]) -> None:
    if not units:
        print("\n등록된 유닛이 없어서 삭제할 수 없습니다.\n")
        return

    print("\n[유닛 삭제하기]")

    selected_index = search_unit_menu_for_select(units)
    if selected_index is None:
        return

    target_unit = units[selected_index]
    print(f"선택된 유닛: {format_unit_brief(target_unit)}")

    if not confirm_yes_no("정말 삭제하시겠습니까? (y/n): "):
        print("삭제를 취소했습니다.\n")
        return

    removed_unit = units.pop(selected_index)
    print(f"[완료] {removed_unit.name} 유닛을 삭제했습니다.\n")

def search_unit_menu(units: List[Unit]) -> None:
    ##단순히 검색 결과 목록만 보여주는 메뉴##
    if not units:
        print("\n[알림] 등록된 유닛이 없습니다. 먼저 유닛을 추가하세요.\n")
        return

    print("\n[유닛 검색]")
    keyword = input_non_empty("검색할 이름(또는 일부)을 입력하세요: ")

    search_results = search_units(units, keyword)

    if not search_results:
        print(f"'{keyword}'(와)과 일치하는 유닛을 찾을 수 없습니다.\n")
        return

    print_search_results(search_results, keyword)

def search_unit_menu_for_select(units: List[Unit]) -> Optional[int]:
    ##검색어로 유닛을 찾고, 번호를 선택하여 units 리스트 인덱스를 반환한다##
    if not units:
        print("\n[알림] 등록된 유닛이 없습니다.\n")
        return None

    print("\n[유닛 검색]")
    keyword = input_non_empty("검색할 이름(또는 일부)을 입력하세요: ")

    search_results = search_units(units, keyword)

    if not search_results:
        print("검색 결과가 없습니다.\n")
        return None

    selected = select_from_list(
        search_results,
        title=f"'{keyword}' 검색 결과",
        render_item=render_search_item,
        allow_cancel=True,
    )

    if selected is None:
        return None
    
    original_index, _ = search_results[selected]
    return original_index

def advanced_search_menu(units: List[Unit]) -> None:
    ##레벨/ATK/HP/코스트/역할/타겟 타입 기준으로 필터해서 보여주는 고급검색 메뉴##
    if not units:
        print("\n[알림] 등록된 유닛이 없습니다. 먼저 유닛을 추가하세요.\n")
        return

    while True:
        print("\n[고금 검색/필터]")
        print("1) 최소 레벨 이상 유닛 보기")
        print("2) 최소 ATK 이상 유닛 보기")
        print("3) 최대 HP 이하 유닛 보기")
        print("4) 최대 코스트 이하 유닛 보기")
        print("5) 역할(Role)로 필터")
        print("6) 타겟 타입으로 필터 (ground/air/both)")
        print("7) 공격 타입으로 필터 (melee/ranged/magic)")
        print("0) 돌아가기")

        choice = input("번호를 선택하세요: ").strip()

        if choice == "1":
            min_level = input_int("최소 레벨을 입력하세요: ", allow_negative=False)
            results = [
                (i, u) for i, u in enumerate(units)
                if u.level >= min_level
            ]
            print_indexed_results(results, f"레벨 >= {min_level}")

        elif choice == "2":
            min_atk = input_int("최소 ATK를 입력하세요: ", allow_negative=False)
            results = [
                (i, u) for i, u in enumerate(units)
                if u.atk >= min_atk
            ]
            print_indexed_results(results, f"ATK >= {min_atk}")
        
        elif choice == "3":
            max_hp = input_int("최대 HP를 입력하세요: ", allow_negative=False)
            results = [
                (i, u) for i, u in enumerate(units)
                if u.hp <= max_hp
            ]
            print_indexed_results(results, f"HP <= {max_hp}")
        
        elif choice == "4":
            max_cost = input_int("최대 코스트를 입력하세요: ", allow_negative=False)
            results = [
                (i, u) for i, u in enumerate(units)
                if u.cost <= max_cost
            ]
            print_indexed_results(results, f"Cost <= {max_cost}")

        elif choice == "5":
            role = input_non_empty(
                "필터할 역할(Role)을 입력하세요 (예: tower/enemy/hero): "
            )
            role_key = role.strip().lower()
            results = [
                (i, u) for i, u in enumerate(units)
                if u.role.lower() == role_key
            ]
            print_indexed_results(results, f"Role == {role_key}")

        elif choice == "6":
            target = input_non_empty(
                "필터할 타겟 타입을 입력하세요 (ground/air/both): "
            )
            target_key = target.strip().lower()
            results = [
                (i, u) for i, u in enumerate(units)
                if u.target_type.lower() == target_key
            ]
            print_indexed_results(results, f"TargetType == {target_key}")

        elif choice == "7": 
            attack = input_non_empty(
                "필터할 공격 타입을 입력하세요 (melee/ranged/magic 등): "
            )
            atk_type_key = attack.strip().lower()
            results = [
                (i, u) for i, u in enumerate(units)
                if u.attack_type.lower() == atk_type_key
            ]
            print_indexed_results(results, f"AttackType == {atk_type_key}")

        elif choice == "0":
            print("고급 검색/필터 메뉴를 종료합니다.\n")
            return
        
        else:
            print("잘못된 번호입니다. 0~6 중에서 선택해주세요.\n")

# ============================
# 유닛 수정 서브 함수들
# ============================

def _edit_unit_name(unit: Unit) -> None:
    new_name = input("새 이름을 입력하세요 (빈 입력 = 변경 안함): ").strip()
    if not new_name:
        print("이름 변경을 취소했습니다.\n")
        return

    print(f"이름: {unit.name} -> {new_name}")
    unit.name = new_name
    print("이름이 변경되었습니다.\n")


def _edit_unit_level(unit: Unit) -> None:
    new_level = input_int("새 레벨을 입력하세요(0 이상의 정수): ", allow_negative=False)
    print(f"레벨: {unit.level} -> {new_level}")
    unit.level = new_level
    print("레벨이 변경되었습니다.\n")


def _edit_unit_hp(unit: Unit) -> None:
    new_hp = input_int("새 HP를 입력하세요(0 이상의 정수): ", allow_negative=False)
    print(f"HP: {unit.hp} -> {new_hp}")
    unit.hp = new_hp
    print("HP가 변경되었습니다.\n")


def _edit_unit_atk(unit: Unit) -> None:
    new_atk = input_int("새 ATK를 입력하세요(0 이상의 정수): ", allow_negative=False)
    print(f"ATK: {unit.atk} -> {new_atk}")
    unit.atk = new_atk
    print("ATK가 변경되었습니다.\n")

def _edit_unit_role(unit: Unit) -> None:
    print(f"현재 역할(Role): {unit.role}")
    raw = input("새 역할을 입력하세요 (tower/enemy/hero 등, 빈 입력 = 변경 안함): ").strip()
    if not raw:
        print("역할 변경을 취소했습니다.\n")
        return

    print(f"역할: {unit.role} -> {raw}")
    unit.role = raw
    print("역할이 변경되었습니다.\n")


def _edit_unit_cost(unit: Unit) -> None:
    new_cost = input_int("새 코스트를 입력하세요(0 이상의 정수): ", allow_negative=False)
    print(f"코스트: {unit.cost} -> {new_cost}")
    unit.cost = new_cost
    print("코스트가 변경되었습니다.\n")


def _edit_unit_range(unit: Unit) -> None:
    new_range = input_int("새 사거리를 입력하세요(0 이상의 정수): ", allow_negative=False)
    print(f"사거리: {unit.range} -> {new_range}")
    unit.range = new_range
    print("사거리가 변경되었습니다.\n")

def _edit_unit_attack_type(unit: Unit) -> None:
    print(f"현재 공격 타입: {unit.attack_type}")
    raw = input(
        "새 공격 타입을 입력하세요 (melee/ranged/magic 등, 빈 입력 = 변경 안함): "
    ).strip()
    if not raw:
        print("공격 타입 변경을 취소했습니다.\n")
        return
    
    print(f"공격 타입: {unit.attack_type} -> {raw}")
    unit.attack_type = raw
    print("공격 타입이 변경되었습니다.\n")


def _edit_unit_target_type(unit: Unit) -> None:
    print(f"현재 타겟 타입: {unit.target_type}")
    raw = input("새 타겟 타입을 입력하세요 (ground/air/both, 빈 입력 = 변경 안함): ").strip()
    if not raw:
        print("타겟 타입 변경을 취소했습니다.\n")
        return

    print(f"타겟 타입: {unit.target_type} -> {raw}")
    unit.target_type = raw
    print("타겟 타입이 변경되었습니다.\n")

def _edit_unit_attack_speed(unit: Unit) -> None:
    new_aspd = _input_float("새 공격 속도를 입력하세요 (예: 1, 1.5): ", allow_negative=False)
    print(f"공격 속도: {unit.attack_speed} -> {new_aspd}")
    unit.attack_speed = new_aspd
    print("공격 속도가 변경되었습니다.\n")


def _edit_unit_move_speed(unit: Unit) -> None:
    new_mspd = _input_float("새 이동 속도를 입력하세요 (예: 1, 0.8): ", allow_negative=False)
    print(f"이동 속도: {unit.move_speed} -> {new_mspd}")
    unit.move_speed = new_mspd
    print("이동 속도가 변경되었습니다.\n")


def _edit_unit_growth(unit: Unit) -> None:
    print(f"현재 레벨당 HP 증가량: {unit.hp_per_level}")
    new_hp_per_level = input_int(
        "레벨당 HP 증가량을 입력하세요(0 이상의 정수): ",
        allow_negative=False,
    )

    print(f"현재 레벨당 ATK 증가량: {unit.atk_per_level}")
    new_atk_per_level = input_int(
        "레벨당 ATK 증가량을 입력하세요(0 이상의 정수): ",
        allow_negative=False,
    )

    print(
        f"레벨당 HP: {unit.hp_per_level} -> {new_hp_per_level}, "
        f"레벨당 ATK: {unit.atk_per_level} -> {new_atk_per_level}"
    )
    unit.hp_per_level = new_hp_per_level
    unit.atk_per_level = new_atk_per_level
    print("성장 계수가 변경되었습니다.\n")

def edit_unit_menu(units: List[Unit]) -> None:
    print("\n[유닛 정보 수정하기]")

    if not units:
        print("등록된 유닛이 없습니다.\n")
        return

    ##검색을 통해 수정할 유닛 선택##
    selected_index = search_unit_menu_for_select(units)
    if selected_index is None:
        print("유닛 선택을 취소했습니다.\n")
        return
    if not (0 <= selected_index < len(units)):
        print("잘못된 유닛 선택입니다.\n")
        return

    unit = units[selected_index]

    while True:
        print_unit_detail(unit)
        print("=== 수정할 유닛 정보 선택 ===")
        print(f"현재: {format_unit_brief(unit)}")
        print("1) 이름 수정")
        print("2) 레벨 수정")
        print("3) HP 수정")
        print("4) ATK 수정")
        print("5) 역할(Role) 수정")
        print("6) 코스트 수정")
        print("7) 사거리 수정")
        print("8) 공격 속도 수정")
        print("9) 이동 속도 수정")
        print("10) 타겟 타입 수정")
        print("11) 성장 계수(레벨당 HP/ATK) 수정")
        print("12) 공격 타입 수정")
        print("0) 취소 (수정 메뉴 종료)")

        choice = input("번호를 선택하세요: ").strip()

        if choice == "1":
            _edit_unit_name(unit)
        elif choice == "2":
            _edit_unit_level(unit)
        elif choice == "3":
            _edit_unit_hp(unit)
        elif choice == "4":
            _edit_unit_atk(unit)
        elif choice == "5":
            _edit_unit_role(unit)
        elif choice == "6":
            _edit_unit_cost(unit)
        elif choice == "7":
            _edit_unit_range(unit)
        elif choice == "8":
            _edit_unit_attack_speed(unit)
        elif choice == "9":
            _edit_unit_move_speed(unit)
        elif choice == "10":
            _edit_unit_target_type(unit)
        elif choice == "11":
            _edit_unit_growth(unit)
        elif choice == "12":
            _edit_unit_attack_type(unit)
        elif choice == "0":
            print("유닛 정보 수정을 종료합니다.\n")
            return
        else:
            print("잘못된 번호입니다. 0~11 중에서 선택해주세요.\n")

def _get_unit_kind(unit: Unit) -> str:
    ##role로부터 유닛이 ground/ari/tower 계열인지 유추##
    r = unit.role.lower()
    if "air" in r:
        return "air"
    if "tower" in r:
        return "tower"
    # boss_enemy, ground_enemy 등은 모두 지상으로 취급
    return "ground"

def _can_attack_target(attacker: Unit, defender: Unit) -> bool:
    ##attacker.target_type 과 defender.role(또는 kind)를 비교해서 공격 가능 여부를 판단##
    atk_target = attacker.target_type.lower()
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
    ##공격 타입에 따라 사거리 판정##
    atk_type = attacker.attack_type.lower()
    if atk_type == "melee":
        melee_range = 1.0
        return distance <= melee_range
    else:
        # ranged, magic 등의 경우 Unit.range 사용
        return distance <= attacker.range

def simulate_duel(attacker: Unit, defender: Unit,
                  initial_distance: float = 5.0,
                  verbose: bool = True) -> dict:
    """
    사거리/이동속도/타겟타입/공격타입을 고려한 1:1 전투 시뮬레이션

    - 1차원 레인 위에 두 유닛을 두고,
      시간에 따라 거리 = initial_distance - (move_speed 합) * t 로 줄어듦
    - 공격 속도 → 1 / attack_speed 간격으로 공격 이벤트 발생
    - 근접/원거리/마법, ground/air/both 타겟 타입 등을 사용
    """

    a_hp = attacker.hp
    d_hp = defender.hp

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
    
    # 1) 공격 간격 계산
    a_interval = float("inf") if attacker.attack_speed <= 0 else 1.0 / attacker.attack_speed
    d_interval = float("inf") if defender.attack_speed <= 0 else 1.0 / defender.attack_speed

    time = 0.0
    next_a = 0.0 if a_interval != float("inf") else float("inf")
    next_d = 0.0 if d_interval != float("inf") else float("inf")
    a_attacks = 0
    d_attacks = 0

    # 2) 상대방 방향으로의 상대 속도 (타워는 move_speed=0)
    rel_speed = max(attacker.move_speed, 0.0) + max(defender.move_speed, 0.0)
    eps = 1e-9
    max_steps = 10000

    def _max_effective_range(u: Unit) -> float:
        if u.attack_speed <= 0:
            return 0.0
        if u.attack_type.lower() == "melee":
            return 1.0
        return float(u.range)
    
    # 3) 아무도 움직이지 않고, 서로 사거리 밖이면 전투 불가
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

    # 4) 메인 루프
    for _ in range(max_steps):
        if a_hp <= 0 or d_hp <= 0:
            break

        next_event = min(next_a, next_d)
        if next_event == float("inf"):
            if verbose:
                print("더 이상 공격 이벤트가 없어 전투를 종료합니다.")
            break

        time = next_event

        # 현재 시간에서의 거리 계산
        if rel_speed > 0:
            distance = max(0.0, initial_distance - rel_speed * time)
        else:
            distance = initial_distance

        if verbose:
            print(f"\n[시간 {time:.2f}s] 거리:{distance:.2f}, "
                  f"{attacker.name} HP:{a_hp}, {defender.name} HP:{d_hp}")

        # 공격자 턴
        if next_a <= next_event + eps:
            if _can_attack_target(attacker, defender) and _is_in_attack_range(attacker, defender, distance):
                d_hp -= attacker.atk
                a_attacks += 1
                if verbose:
                    print(f"  {attacker.name} -> {defender.name} "
                          f"({attacker.atk} 피해, {defender.name} HP {max(d_hp, 0)})")
            else:
                if verbose:
                    print(f"  {attacker.name} 공격 불가 (사거리/타겟 조건 미충족)")
            next_a += a_interval

        # 방어자 턴
        if d_hp > 0 and next_d <= next_event + eps:
            if _can_attack_target(defender, attacker) and _is_in_attack_range(defender, attacker, distance):
                a_hp -= defender.atk
                d_attacks += 1
                if verbose:
                    print(f"  {defender.name} -> {attacker.name} "
                          f"({defender.atk} 피해, {attacker.name} HP {max(a_hp, 0)})")
            else:
                if verbose:
                    print(f"  {defender.name} 공격 불가 (사거리/타겟 조건 미충족)")
            next_d += d_interval

        if a_hp <= 0 or d_hp <= 0:
            break

    else:
        if verbose:
            print("[주의] 최대 스텝에 도달하여 전투를 강제 종료했습니다.")

    # 5) 승패 판정
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
        "attacker_final_hp": max(a_hp, 0),
        "defender_final_hp": max(d_hp, 0),
        "attacker_attacks": a_attacks,
        "defender_attacks": d_attacks,
    }

def battle_simulation_menu(units: List[Unit]) -> None:
    ##유닛 2개를 골라 1:1 전투를 시뮬레이션하는 메뉴##
    if not units:
        print("\n[알림] 등록된 유닛이 없습니다. 먼저 유닛을 추가하세요.\n")
        return

    print("\n[전투 시뮬레이션 - 1 대 1]")
    print("선택한 두 유닛이 현재 스탯(HP / ATK / 공격 속도 기준)으로 싸웠을 때,")
    print("어느 쪽이 이기는지와 걸리는 시간을 확인할 수 있습니다.\n")

    # 1) 공격자 선택
    print("[공격자 선택]")
    attacker_index = search_unit_menu_for_select(units)
    if attacker_index is None:
        print("전투 시뮬레이션을 취소합니다.\n")
        return

    # 2) 방어자 선택
    print("[방어자 선택]")
    defender_index = search_unit_menu_for_select(units)
    if defender_index is None:
        print("전투 시뮬레이션을 취소합니다.\n")
        return

    attacker = units[attacker_index]
    defender = units[defender_index]

    # 3) 선택 결과 출력
    print("\n=== 선택된 유닛 ===")
    print("[공격자]")
    print_unit_detail(attacker)
    print("[방어자]")
    print_unit_detail(defender)

    if not confirm_yes_no("이 구성으로 전투 시뮬레이션을 실행할까요? (y/n): "):
        print("전투 시뮬레이션을 취소했습니다.\n")
        return

    verbose = confirm_yes_no("전투 로그를 턴마다 출력할까요? (y/n): ")

    # 4) 전투 실행
    print("\n=== 전투 시작 ===")
    result = simulate_duel(attacker, defender, verbose=verbose)

    # 5) 결과 요약 출력
    print("\n=== 전투 결과 요약 ===")
    print(f"총 경과 시간      : {result['time']:.2f}초")
    print(f"공격자 공격 횟수  : {result['attacker_attacks']}")
    print(f"방어자 공격 횟수  : {result['defender_attacks']}")
    print(f"공격자 최종 HP    : {result['attacker_final_hp']}")
    print(f"방어자 최종 HP    : {result['defender_final_hp']}")

    winner = result["winner"]
    if winner == "attacker":
        print(f"승자: 공격자 {attacker.name}")
    elif winner == "defender":
        print(f"승자: 방어자 {defender.name}")
    elif winner == "draw":
        print("결과: 동시 사망 (무승부)")
    else:
        print("결과: 어느 쪽도 상대를 쓰러뜨리지 못했습니다.")
    print()

    # 2D 위치 요약
    ax0, ay0 = result["attacker_start_pos"]
    dx0, dy0 = result["defender_start_pos"]
    ax1, ay1 = result["attacker_final_pos"]
    dx1, dy1 = result["defender_final_pos"]

    final_dist = math.hypot(dx1 - ax1, dy1 - ay1)

    print("\n[공간 요약]")
    print(f"공격자: 시작 ({ax0:.2f}, {ay0:.2f}) -> 최종 ({ax1:.2f}, {ay1:.2f})")
    print(f"방어자: 시작 ({dx0:.2f}, {dy0:.2f}) -> 최종 ({dx1:.2f}, {dy1:.2f})")
    print(f"최종 거리: {final_dist:.2f}")
    print()

import math
from typing import Tuple
from unit_model import Unit

def simulate_duel_2d(
    attacker: Unit,
    defender: Unit,
    attacker_pos: Tuple[float, float] = (0.0, 0.0),
    defender_pos: Tuple[float, float] = (5.0, 0.0),
    dt: float = 0.05,       # 이동/거리 업데이트 간격
    max_time: float = 60.0, # 최대 전투 시간
    verbose: bool = True,
) -> dict:
    """
    2D 좌표 기반 1:1 전투 시뮬레이션

    - 공격자 / 방어자의 위치를 (x, y)로 관리
    - 각 틱마다 서로를 향해 이동 (move_speed 사용)
    - 공격 속도(attack_speed)에 따라 공격 타이밍 계산
    - 사거리 판정은 거리(distance)에 대해 _is_in_attack_range() 사용
    """

    ax, ay = attacker_pos
    dx, dy = defender_pos

    a_hp = float(attacker.hp)
    d_hp = float(defender.hp)

    # 양쪽 다 공격 속도가 0이면 전투 불가
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

    # 다음 공격 시각 (이벤트 타임)
    a_interval = math.inf if attacker.attack_speed <= 0 else 1.0 / attacker.attack_speed
    d_interval = math.inf if defender.attack_speed <= 0 else 1.0 / defender.attack_speed

    a_next = a_interval if a_interval < math.inf else math.inf
    d_next = d_interval if d_interval < math.inf else math.inf

    time = 0.0
    a_attacks = 0
    d_attacks = 0
    eps = 1e-9

    # 시작 위치 기록
    attacker_start_pos = (ax, ay)
    defender_start_pos = (dx, dy)

    while time < max_time and a_hp > 0 and d_hp > 0:
        # 1) 다음 '움직임 틱'과 '공격 이벤트' 중 가장 가까운 시간까지 진행
        t_tick = time + dt
        next_event = min(t_tick, a_next, d_next)
        move_dt = max(0.0, next_event - time)

        # 2) 서로를 향해 이동
        if attacker.move_speed > 0 or defender.move_speed > 0:
            vec_x = dx - ax
            vec_y = dy - ay
            dist = math.hypot(vec_x, vec_y)
            if dist > 0:
                dir_x = vec_x / dist
                dir_y = vec_y / dist
            else:
                dir_x = dir_y = 0.0

            # 공격자는 상대 방향으로, 방어자는 반대 방향으로 이동
            ax += attacker.move_speed * dir_x * move_dt
            ay += attacker.move_speed * dir_y * move_dt

            dx -= defender.move_speed * dir_x * move_dt
            dy -= defender.move_speed * dir_y * move_dt

        time = next_event

        # 3) 현재 거리 계산
        distance = math.hypot(dx - ax, dy - ay)

        if verbose:
            print(
                f"\n[시간 {time:.2f}s] "
                f"거리:{distance:.2f}, "
                f"{attacker.name} HP:{a_hp:.1f}, "
                f"{defender.name} HP:{d_hp:.1f}"
            )

        # 4) 공격자 공격 처리
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

        # 5) 방어자 공격 처리
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

        # 6) 사망 체크
        if a_hp <= 0 or d_hp <= 0:
            break

    # 7) 승패 판정
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
        "attacker_final_hp": max(a_hp, 0),
        "defender_final_hp": max(d_hp, 0),
        "attacker_attacks": a_attacks,
        "defender_attacks": d_attacks,
        "attacker_start_pos": attacker_start_pos,
        "defender_start_pos": defender_start_pos,
        "attacker_final_pos": (ax, ay),
        "defender_final_pos": (dx, dy),
    }