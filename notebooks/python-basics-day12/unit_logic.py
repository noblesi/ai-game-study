from typing import List, Optional, Tuple
from unit_model import Unit

def print_units(units: List[Unit]) -> None:
    ##등록된 유닛 목록을 출력한다##
    if not units:
        print("\n등록된 유닛이 없습니다.\n")
        return
    
    print("\n=== 유닛 목록 ===")
    for i, unit in enumerate(units, start = 1):
        print(f"{i}. {unit.name} (Lv.{unit.level} / HP:{unit.hp} / ATK:{unit.atk})")
    print()

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

def add_unit_menu(units: List[Unit]) -> None:
    print("\n[유닛 추가하기]")
    name = input("유닛 이름을 입력하세요: ").strip()

    if not name:
        print("이름을 비워둘 수 없습니다.\n")
        return

    level = _input_positive_int("레벨을 입력하세요(0 이상의 정수): ")
    hp = _input_positive_int("HP를 입력하세요(0 이상의 정수): ")
    atk = _input_positive_int("ATK를 입력하세요(0 이상의 정수): ")

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
    print(
        f"선택된 유닛: {target_unit.name} "
        f"(Lv.{target_unit.level} / HP:{target_unit.hp} / ATK:{target_unit.atk})"
    )

    confirm = input("정말 삭제하시겠습니까? (y/n): ").strip().lower()

    if confirm != "y":
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
    keyword = input("검색할 이름(또는 일부)을 입력하세요: ").strip()

    if not keyword:
        print("검색어를 비워둘 수 없습니다.\n")
        return

    search_results = search_units(units, keyword)

    if not search_results:
        print(f"'{keyword}'(와)과 일치하는 유닛을 찾을 수 없습니다.\n")
        return

    print(f"\n=== 검색 결과 ({len(search_results)}개) ===")
    for display_idx, (_idx, unit) in enumerate(search_results, start=1):
        print(
            f"{display_idx}. {unit.name} "
            f"(Lv.{unit.level} / HP:{unit.hp} / ATK:{unit.atk})"
        )
    print()


def search_unit_menu_for_select(units: List[Unit]) -> Optional[int]:
    ##검색어로 유닛을 찾고, 번호를 선택하여 units 리스트 인덱스를 반환한다##
    print("\n[유닛 검색]")
    keyword = input("검색할 이름(또는 일부)을 입력하세요: ").strip()

    if not keyword:
        print("검색어를 비워둘 수 없습니다.\n")
        return None

    search_results = search_units(units, keyword)

    if not search_results:
        print("검색 결과가 없습니다.\n")
        return None

    print("\n[검색 결과]")
    for display_idx, (unit_idx, unit) in enumerate(search_results, start=1):
        print(
            f"{display_idx}. {unit.name} "
            f"(Lv.{unit.level} / HP:{unit.hp} / ATK:{unit.atk})"
        )
    print("0) 취소")

    while True:
        choice = input("번호를 선택하세요 (0 : 취소): ").strip()

        if choice == "0":
            print("검색을 취소합니다.\n")
            return None

        try:
            choice_num = int(choice)
        except ValueError:
            print("숫자를 입력해주세요.\n")
            continue

        if 1 <= choice_num <= len(search_results):
            selected_index, _ = search_results[choice_num - 1]
            return selected_index
        else:
            print("범위에 없는 번호입니다. 다시 선택해주세요.\n")


def _input_positive_int(prompt: str) -> int:
    ##0 이상의 정수를 입력받을 때 사용하는 공통 유틸 함수##
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if value < 0:
                print("음수는 입력할 수 없습니다. 0 이상의 정수로 다시 입력해주세요.\n")
                continue
            return value
        except ValueError:
            print("정수를 입력하세요.\n")


def edit_unit_menu(units: List[Unit]) -> None:
    print("\n[유닛 정보 수정하기]")

    if not units:
        print("등록된 유닛이 없습니다.\n")
        return

    ##검색을 통해 수정할 유닛 선택##
    selected_index = search_unit_menu_for_select(units)

    if selected_index is None or selected_index < 0 or selected_index >= len(units):
        print("유닛 선택을 취소했습니다.\n")
        return

    unit = units[selected_index]

    print("\n[선택된 유닛 정보]")
    print(f"이름: {unit.name}")
    print(f"레벨: {unit.level}")
    print(f"HP: {unit.hp}")
    print(f"ATK: {unit.atk}\n")

    while True:
        print("=== 수정할 유닛 정보 ===")
        print("1) 이름 수정")
        print("2) 레벨 수정")
        print("3) HP 수정")
        print("4) ATK 수정")
        print("5) 취소 (수정 메뉴 종료)")

        choice = input("번호를 선택하세요: ").strip()

        if choice == "1":
            new_name = input("새 이름을 입력하세요 (빈 입력 = 변경 안함): ").strip()
            if not new_name:
                print("이름 변경을 취소했습니다.\n")
            else:
                print(f"이름: {unit.name} -> {new_name}")
                unit.name = new_name
                print("이름이 변경되었습니다.\n")

        elif choice == "2":
            new_level = _input_positive_int("새 레벨을 입력하세요(0 이상의 정수): ")
            print(f"레벨: {unit.level} -> {new_level}")
            unit.level = new_level
            print("레벨이 변경되었습니다.\n")

        elif choice == "3":
            new_hp = _input_positive_int("새 HP를 입력하세요(0 이상의 정수): ")
            print(f"HP: {unit.hp} -> {new_hp}")
            unit.hp = new_hp
            print("HP가 변경되었습니다.\n")

        elif choice == "4":
            new_atk = _input_positive_int("새 ATK를 입력하세요(0 이상의 정수): ")
            print(f"ATK: {unit.atk} -> {new_atk}")
            unit.atk = new_atk
            print("ATK가 변경되었습니다.\n")

        elif choice == "5":
            print("유닛 정보 수정을 종료합니다.\n")
            return

        else:
            print("잘못된 번호입니다. 1~5 중에서 선택해주세요.\n")