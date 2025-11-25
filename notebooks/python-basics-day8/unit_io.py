import json

def save_units_to_file(units, filename="units.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(units, f, ensure_ascii=False, indent=2)
        print(f"\n유닛정보를 '{filename}' 파일에 저장했습니다.\n")
    except Exception as e:
        print(f"\n유닛 정보를 저장하는 중 오류가 발생했브니다: {e}\n")

    

def load_units_from_file(filename="units.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                print("[경고] 저장된 데이터 형식이 올바르지 않습니다. 새 유닛 리스트로 시작합니다.")
                return []
            print(f"[알림]'{filename}' 파일에서 유닛 정보를 불러왔습니다.\n")
        return data
    except FileNotFoundError:
        print(f"[알림] '{filename}' 파일이 없어 새 유닛 리스트를 사용합니다.\n")
        return []
    except json.JSONDecodeError:
        print(f"[경고] '{filename}' 파일을 읽는 중 오류가 발생했습니다. 새 유닛 리스트를 사용합니다.\n")
        return []
