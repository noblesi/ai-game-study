from typing import Sequence, Callable, TypeVar

T = TypeVar("T")

def input_int(prompt: str, allow_negative: bool = False) -> int:
    ##정수 입력을 공통으로 처리하는 함수(빈 값/문자/음수 처리)##
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("빈 값은 입력할 수 없습니다. 다시 입력해주세요.")
            continue

        try:
            value = int(raw)
        except ValueError:
            print("정수를 입력해주세요.")
            continue

        if not allow_negative and value < 0:
            print("음수는 입력할 수 없습니다.")
            continue

        return value
    
def input_non_empty(prompt: str) -> str:
    ##빈 문자열을 허용하지 않는 문자열 입력용 함수##
    while True:
        value = input(prompt).strip()
        if not value:
            print("빈 값은 입력할 수 없습니다. 다시 입력해주세요.")
            continue

        return value
    
def confirm_yes_no(prompt: str) -> bool:
    ##y/n 확인 입력 공통 함수##
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("y 또는 n으로 입력해주세요.")
    

def select_from_list(
        items: Sequence[T],
        title: str,
        render_item: Callable[[T, int], None] | None = None,
        allow_cancel: bool = True
) -> int | None:
    ##공통 '번호 선택' 메뉴 함수##
    ##items: 선택 대상 리스트##
    ##title: 위에 출력할 제목##
    ##render_item: 각 아이템 출력 함수 (item, index) -> None##
    ##return: 선택한 인덱스 (0 기반). 취소 시 None##
    if not items:
        print("선택할 항목이 없습니다.")
        return None
    
    print()
    print(f"=== {title} ===")

    ##목록 출력
    for idx, item in enumerate(items, start=1):
        if render_item:
            render_item(item, idx)
        else:
            print(f"{idx}) {item}")
    print()

    while True:
        if allow_cancel:
            raw = input("번호를 선택하세요(취소: 0): ").strip()
        else:
            raw = input("번호를 선택하세요: ").strip()

        if not raw.isdigit():
            print("숫자를 입력해주세요.")
            continue

        num = int(raw)

        if allow_cancel and num == 0:
            print("선택을 취소합니다.")
            return None
        
        if 1 <= num <= len(items):
            return num - 1
        
        print("범위를 벗어났습니다. 다시 선택해주세요.")