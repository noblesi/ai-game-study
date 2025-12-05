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
        f"Role:{unit.role} / Cost:{unit.cost})"
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

    avg_level = total_level / count
    avg_hp = total_hp / count
    avg_atk = total_atk / count

    highest_level_unit = max(units, key=lambda u: u.level)
    highest_atk_unit = max(units, key=lambda u: u.atk)

    print("\n=== 유닛 통계 ===")
    print(f"총 유닛 수: {count}")
    print(f"평균 레벨: {avg_level:.1f}")
    print(f"평균 HP   : {avg_hp:.1f}")
    print(f"평균 ATK  : {avg_atk:.1f}")
    print()
    print(f"최고 레벨 유닛: {format_unit_brief(highest_level_unit)}")
    print(f"최고 ATK 유닛 : {format_unit_brief(highest_atk_unit)}")
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

    unit = Unit(
        name=name,
        level=level,
        hp=hp,
        atk=atk,
        role=role,
        range=range_,
        cost=cost,
        target_type=target_type,
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
        elif choice == "0":
            print("유닛 정보 수정을 종료합니다.\n")
            return
        else:
            print("잘못된 번호입니다. 0~11 중에서 선택해주세요.\n")