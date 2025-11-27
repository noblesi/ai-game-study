class Unit:
    def __init__(self, name, level, hp, atk):
        self.name = name
        self.level = level
        self.hp = hp
        self.atk = atk
    
    def level_up(self):
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