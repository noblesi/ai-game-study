from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class Unit:
    """
    디펜스/전투 시뮬레이션에서 사용하는 공통 유닛 데이터 모델.

    - 기본 전투 스탯: name, level, hp, atk
    - 디펜스/밸런스/AI 실험용 확장 스탯:
      role, cost, range, attack_speed, move_speed, target_type, attack_type
    - 성장 계수: hp_per_level, atk_per_level

    전투 시뮬레이션 함수(simulate_duel, simulate_duel_2d)와
    자동 실험 메뉴(auto_battle_experiment_menu)는
    이 클래스를 입력으로 받아서,
    결과를 일관된 dict 포맷으로 반환하도록 맞춰져 있다.
    """


    # 기본스탯
    name: str
    level: int
    hp: int
    atk: int

    # 디펜스 게임용 확장 스탯
    role: str = "tower"
    cost: int = 100
    range: int = 1
    attack_speed: float = 1.0
    move_speed: float = 1.0
    target_type: str = "ground"
    attack_type: str = "melee"

    # 성장계수(레벨업 시 증가량)
    hp_per_level: int = 30
    atk_per_level: int = 5

    # Perk(레벨 보상)
    # - 3/6/10레벨에 1개씩 선택(최대 3개)
    # - 실제 선택/검증 로직은 unit_logic.py가 담당
    perks: List[str] = field(default_factory=list)
    
    def level_up(self, max_level: int = 10) -> bool:
        """유닛 레벨을 1 올리고, HP/ATK를 함께 증가.

        - 기본 룰: max_level=10
        - 레벨업 불가면 False 반환
        """
        if self.level >= max_level:
            return False
        self.level += 1
        self.hp += self.hp_per_level
        self.atk += self.atk_per_level
        return True

    def to_dict(self) -> dict:
        return{
            "name": self.name,
            "level": self.level,
            "hp": self.hp,
            "atk": self.atk,
            "role": self.role,
            "cost": self.cost,
            "range": self.range,
            "attack_speed": self.attack_speed,
            "move_speed": self.move_speed,
            "target_type": self.target_type,
            "attack_type": self.attack_type,
            "hp_per_level": self.hp_per_level,
            "atk_per_level": self.atk_per_level,
            "perks": list(self.perks) if self.perks else [],
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Unit":
        return cls(
            name=data["name"],
            level=data["level"],
            hp=data["hp"],
            atk=data["atk"],
            role=data.get("role", "tower"),
            cost=data.get("cost", 100),
            range=data.get("range", 1),
            attack_speed=data.get("attack_speed", 1.0),
            move_speed=data.get("move_speed", 1.0),
            target_type=data.get("target_type", "ground"),
            attack_type=data.get("attack_type", "melee"),
            hp_per_level=data.get("hp_per_level", 30),
            atk_per_level=data.get("atk_per_level", 5),
            perks=list(data.get("perks") or []),
        )