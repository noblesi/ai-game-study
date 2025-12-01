from unit_logic import search_units
from unit_model import Unit

def test_search_units():
    units = [
        Unit("Knight", 1, 100, 20),
        Unit("Dark Knight", 5, 200, 50),
        Unit("Archer", 1, 80, 25),
    ]

    result = search_units(units, "Knight")
    assert len(result) == 2
    print("검색 테스트 통과")

if __name__ == "__main__":
    test_search_units()