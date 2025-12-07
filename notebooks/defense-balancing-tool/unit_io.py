import json
from typing import List
from unit_model import Unit

FILE_PATH = "units.json"

def get_default_units() -> List[Unit]:
    ##프로그램 최초 실행 시 사용할 기본 유닛 목록##
    return [
        # =====================
        # 타워 유닛들
        # =====================
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
            target_type="ground",   # 지상 적만 공격 가능
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
            range=4,                # 장거리
            attack_speed=1.2,
            move_speed=0.0,
            target_type="both",     # 지상 + 공중
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
            range=3,
            attack_speed=0.9,
            move_speed=0.0,
            target_type="ground",   # 기본은 지상만
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
        Unit(
            name="AntiAir Tower",
            level=1,
            hp=90,
            atk=22,
            role="tower",
            cost=130,
            range=5,
            attack_speed=1.0,
            move_speed=0.0,
            target_type="air",      # 공중 전용 타워
            attack_type="ranged",
            hp_per_level=25,
            atk_per_level=6,
        ),

        # =====================
        # 적 유닛들 (지상)
        # =====================
        Unit(
            name="Goblin",
            level=1,
            hp=60,
            atk=8,
            role="ground_enemy",
            cost=40,                # 스폰 코스트나 난이도 기준으로 사용 가능
            range=1,
            attack_speed=1.3,
            move_speed=1.8,
            target_type="tower",    # 타워를 공격
            attack_type="melee",
            hp_per_level=20,
            atk_per_level=3,
        ),
        Unit(
            name="Runner",
            level=1,
            hp=40,
            atk=6,
            role="ground_enemy",
            cost=35,
            range=1,
            attack_speed=1.5,
            move_speed=2.5,         # 매우 빠름
            target_type="tower",
            attack_type="melee",
            hp_per_level=15,
            atk_per_level=2,
        ),
        Unit(
            name="Armored Orc",
            level=1,
            hp=180,
            atk=12,
            role="ground_enemy",
            cost=90,
            range=1,
            attack_speed=0.8,
            move_speed=1.0,
            target_type="tower",
            attack_type="melee",
            hp_per_level=40,
            atk_per_level=4,
        ),
        Unit(
            name="Ogre Boss",
            level=1,
            hp=400,
            atk=20,
            role="boss_enemy",
            cost=200,
            range=1,
            attack_speed=0.6,
            move_speed=0.8,
            target_type="tower",
            attack_type="melee",
            hp_per_level=60,
            atk_per_level=6,
        ),

        # =====================
        # 적 유닛들 (공중 + 원거리)
        # =====================
        Unit(
            name="Wyvern",
            level=1,
            hp=90,
            atk=14,
            role="air_enemy",        # 공중
            cost=110,
            range=1,
            attack_speed=1.0,
            move_speed=2.0,
            target_type="tower",
            attack_type="melee",
            hp_per_level=30,
            atk_per_level=4,
        ),
        Unit(
            name="Dark Shaman",
            level=1,
            hp=80,
            atk=16,
            role="ground_enemy",
            cost=120,
            range=3,                 # 원거리 마법
            attack_speed=0.9,
            move_speed=1.2,
            target_type="tower",
            attack_type="magic",
            hp_per_level=25,
            atk_per_level=5,
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
        return units

    units = [Unit.from_dict(d) for d in data]
    return units