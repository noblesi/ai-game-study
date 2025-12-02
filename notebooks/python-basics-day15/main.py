from unit_io import load_units_from_file, save_units_to_file
from unit_logic import (
    print_units, 
    add_unit_menu, 
    level_up_unit_menu, 
    remove_unit_menu, 
    search_unit_menu,
    edit_unit_menu,
    print_units_stats
)

def main_loop():
    units = load_units_from_file()
    while True:
        print("=== 유닛 관리 메뉴 ===")
        print("1) 유닛 목록 보기")
        print("2) 유닛 추가하기")
        print("3) 유닛 레벨 올리기")
        print("4) 유닛 삭제하기")
        print("5) 유닛 검색하기")
        print("6) 유닛 정보 수정하기")
        print("7) 유닛 통계 보기")
        print("0) 종료")

        choice = input("번호를 선택하세요: ").strip()

        if choice == "1":
            print_units(units)
        elif choice == "2":
            add_unit_menu(units)
        elif choice == "3":
            level_up_unit_menu(units)
        elif choice == "4":
            remove_unit_menu(units)
        elif choice == "5":
            search_unit_menu(units)
        elif choice == "6":
            edit_unit_menu(units)
        elif choice == "7":
            print_units_stats(units)
        elif choice == "0":
            print("프로그램을 종료합니다.")
            save_units_to_file(units)
            break
        else:
            print("잘못 입력했습니다. 다시 선택하세요.")

if __name__ == "__main__":
    main_loop()