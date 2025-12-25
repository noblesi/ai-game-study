from __future__ import annotations

from typing import Sequence, Callable, TypeVar

T = TypeVar("T")


def input_int(prompt: str, allow_negative: bool = False) -> int:
    """정수 입력 공통 처리(빈 값/문자/음수 처리)"""
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

        if (not allow_negative) and value < 0:
            print("음수는 입력할 수 없습니다. 다시 입력해주세요.")
            continue

        return value


def input_non_empty(prompt: str) -> str:
    """빈 문자열을 허용하지 않는 문자열 입력"""
    while True:
        value = input(prompt).strip()
        if not value:
            print("빈 값은 입력할 수 없습니다. 다시 입력해주세요.")
            continue
        return value


def confirm_yes_no(prompt: str) -> bool:
    """y/n 확인 입력"""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("y 또는 n으로 입력해주세요.")


def select_from_list(items: Sequence[T], render: Callable[[T], str]) -> int | None:
    """리스트를 출력하고 번호 선택. 취소 시 None."""
    if not items:
        print("선택할 항목이 없습니다.")
        return None

    for i, item in enumerate(items, start=1):
        print(f"{i}. {render(item)}")

    while True:
        raw = input("번호 선택 (0=취소): ").strip()
        if not raw:
            print("빈 값은 입력할 수 없습니다.")
            continue
        if raw == "0":
            return None
        try:
            idx = int(raw)
        except ValueError:
            print("번호를 입력해주세요.")
            continue
        if 1 <= idx <= len(items):
            return idx - 1
        print("범위를 벗어났습니다.")
