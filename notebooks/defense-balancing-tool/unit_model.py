from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Unit:
    ##기본스탯##
    name: str
    level: int
    hp: int
    atk: int

    ##디펜스 게임용 확장 스탯##
    role: str = "tower"
    cost: int = 100
    range: int = 1
    attack_speed: float = 1.0
    move_speed: float = 1.0
    target_type: str = "ground"

    ##성장계수(레벨업 시 증가량)##
    hp_per_level: int = 30
    atk_per_level: int = 5
    
    def level_up(self) -> None:
        ##유닛 레벨을 1 올리고, HP/ATK를 함께 증가시킨다##
        self.level += 1
        self.hp += self.hp_per_level
        self.atk += self.atk_per_level

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
            "hp_per_level": self.hp_per_level,
            "atk_per_level": self.atk_per_level,
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
            hp_per_level=data.get("hp_per_level", 30),
            atk_per_level=data.get("atk_per_level", 5),
        )