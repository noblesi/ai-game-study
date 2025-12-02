from typing import List, Optional, Tuple
from unit_model import Unit
from utils import input_int, input_non_empty, select_from_list, confirm_yes_no

# ============================
# 공통 유틸 함수들
# ============================

def format_unit_brief(unit: Unit) -> str:
    ##유닛 한 줄 표기 형식 공통화##
    return f"{unit.name} (Lv.{unit.level} / HP:{unit.hp} / ATK:{unit.atk})"

def print_unit_detail(unit: Unit) -> None:
    ##유닛 상세 정보 출력##
    print("\n[선택된 유닛 정보]")
    print(f"이름: {unit.name}")
    print(f"레벨: {unit.level}")
    print(f"HP: {unit.hp}")
    print(f"ATK: {unit.atk}\n")

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

    unit = Unit(name=name, level=level, hp=hp, atk=atk)
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

def edit_unit_menu(units: List[Unit]) -> None:
    print("\n[유닛 정보 수정하기]")

    if not units:
        print("등록된 유닛이 없습니다.\n")
        return

    ##검색을 통해 수정할 유닛 선택##
    selected_index = search_unit_menu_for_select(units)
    if selected_index is None or (0 <= selected_index < len(units)):
        print("유닛 선택을 취소했습니다.\n")
        return

    unit = units[selected_index]
    print_unit_detail(unit)

    while True:
        print("=== 수정할 유닛 정보 ===")
        print(f"현재: {format_unit_brief(unit)}")
        print("1) 이름 수정")
        print("2) 레벨 수정")
        print("3) HP 수정")
        print("4) ATK 수정")
        print("5) 취소 (수정 메뉴 종료)")

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
            print("유닛 정보 수정을 종료합니다.\n")
            return
        else:
            print("잘못된 번호입니다. 1~5 중에서 선택해주세요.\n")