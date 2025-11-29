import json
from typing import List
from unit_model import Unit

FILE_PATH = "units.json"

def save_units_to_file(units: List[Unit], file_path: str = FILE_PATH):
    data = [unit.to_dict() for unit in units]

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_units_from_file(file_path: str = FILE_PATH) -> List[Unit]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("[알림] 저장된 유닛 파일이 없어 새로 시작합니다.")
        return []
    except json.JSONDecodeError:
        print("[경고] JSON 형식이 깨져있어 파일을 무시하고 새로 시작합니다.")
        return []
    
    units = [Unit.from_dict(d) for d in data]
    return units