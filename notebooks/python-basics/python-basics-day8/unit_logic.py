
def print_units(units):
    if not units:
        print("\n등록된 유닛이 없습니다.\n")
        return
    
    print("\n=== 유닛 목록 ===")
    for i, unit in enumerate(units, start = 1):
        print(f"{i}. {unit['name']} (Lv.{unit['level']} / HP:{unit['hp']} / ATK:{unit['atk']})")
    print()

def add_unit_menu(units):
    print("\n[유닛 추가하기]")
    name = input("유닛 이름을 입력하세요: ").strip()

    if not name:
        print("이름을 비워둘 수 없습니다.\n")
        return
    
    try:
        level = int(input("레벨을 입력하세요(정수): "))
        hp = int(input("HP를 입력하세요(정수): "))
        atk = int(input("ATK를 입력하세요(정수): "))
    except ValueError:
        print("숫자를 잘못 입력했습니다. 유닛 추가를 취소합니다.\n")
        return
    
    unit = {
        "name": name,
        "level": level,
        "hp": hp,
        "atk": atk,
    }
    units.append(unit)
    print(f"'{name}' 유닛이 추가되었습니다.\n")

def level_up_unit(units):
    if not units:
        print("\n등록된 유닛이 없어서 레벨을 올릴 수 없습니다.\n")
        return
    
    print("\n[유닛 레벨 올리기]")
    name = input("레벨을 올릴 유닛 이름을 입력하세요: ").strip()

    for unit in units:
        if unit["name"] == name:
            before = unit["level"]
            unit["level"] += 1
            print(f"'{name}'의 레벨이 {before} -> {unit['level']} 으로 증가했습니다.\n")
            return
        
    print(f"'{name}' 이름의 유닛을 찾지 못했습니다.\n")

def remove_unit_menu(units):
    if not units:
        print("\n등록된 유닛이 없어서 삭제할 수 없습니다.\n")
        return
    
    print("\n[유닛 삭제하기]")
    name = input("삭제할 유닛 이름을 입력하세요: ").strip()

    for i, unit in enumerate(units):
        if unit["name"] == name:
            del units[i]
            print(f"'{name}' 유닛을 삭제했습니다.\n")
            return
        
    print(f"'{name}' 이름의 유닛을 찾지 못했습니다.\n")

def find_units_by_name(units, keyword):
    keyword = keyword.strip().lower()
    if not keyword:
        return []
    
    result = []
    for unit in units:
        if keyword in unit["name"].lower():
            result.append(unit)
    return result

def search_unit_menu(units):
    if not units:
        print("\n [알림] 등록된 유닛이 없습니다. 먼저 유닛을 추가하세요.\n")
        return
    
    print("\n [유닛 검색]")
    keyword = input("검색할 이름(또는 일부)을 입력하세요: ").strip()

    if not keyword:
        print("검색어를 비워둘 수 없습니다.\n")
        return
    
    matched_units = find_units_by_name(units, keyword)

    if not matched_units:
        print(f"'{keyword}'(와)과 일치하는 유닛을 찾을 수 없습니다.\n")
        return
    
    print(f"\n=== 검색 결과 ({len(matched_units)}개) ===")
    for i, unit in enumerate(matched_units, start=1):
        print(f"{i}. {unit['name']} (Lv.{unit['level']} / HP:{unit['hp']} / ATK: {unit['atk']})")
    print()
