import json
from typing import List
from unit_model import Unit

FILE_PATH = "units.json"

def get_default_units() -> List[Unit]:
    ##프로그램 최초 실행 시 사용할 기본 유닛 목록##
    return [
        Unit(
            name="Knight",
            level=1,
            hp=120,
            atk=15,
            role="tower",
            cost=80,
            range=1,
            attack_speed=1.0,
            move_speed=0.0,
            target_type="ground",
            attack_type="melee",
            hp_per_level=35,
            atk_per_level=4,
        ),
        Unit(
            name="Archer",
            level=1,
            hp=80,
            atk=20,
            role="tower",
            cost=100,
            range=3,
            attack_speed=1.2,
            move_speed=0.0,
            target_type="both",
            attack_type="ranged",
            hp_per_level=25,
            atk_per_level=6,
        ),
        Unit(
            name="Mage",
            level=1,
            hp=70,
            atk=25,
            role="tower",
            cost=120,
            range=2,
            attack_speed=0.9,
            move_speed=0.0,
            target_type="ground",
            attack_type="magic",
            hp_per_level=20,
            atk_per_level=7,
        ),
        Unit(
            name="Tank",
            level=1,
            hp=200,
            atk=10,
            role="tower",
            cost=150,
            range=1,
            attack_speed=0.7,
            move_speed=0.0,
            target_type="ground",
            attack_type="melee",
            hp_per_level=40,
            atk_per_level=3,
        ),
    ]

def save_units_to_file(units: List[Unit], file_path: str = FILE_PATH):
    data = [unit.to_dict() for unit in units]

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_units_from_file(file_path: str = FILE_PATH) -> List[Unit]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("[알림] 저장된 유닛 파일이 없어 기본 유닛을 생성합니다.")
        units = get_default_units()
        save_units_to_file(units, file_path)
        return units
    except json.JSONDecodeError:
        print("[경고] JSON 형식이 깨져있어 파일을 무시하고 기본 유닛으로 다시 생성합니다.")
        units = get_default_units()
        save_units_to_file(units, file_path)
        return []

    units = [Unit.from_dict(d) for d in data]
    return units