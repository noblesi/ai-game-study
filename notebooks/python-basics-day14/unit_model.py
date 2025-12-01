from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Unit:
    name: str
    level: int
    hp: int
    atk: int
    
    def level_up(self) -> None:
        ##유닛 레벨을 1 올리고, HP/ATK를 함께 증가시킨다##
        self.level += 1
        self.hp += 30
        self.atk += 5

    def to_dict(self) -> dict:
        return{
            "name": self.name,
            "level": self.level,
            "hp": self.hp,
            "atk": self.atk,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Unit":
        return cls(
            name=data["name"],
            level=data["level"],
            hp=data["hp"],
            atk=data["atk"],
        )