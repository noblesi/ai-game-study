# common/perk.py
import json
import random
from pathlib import Path
from typing import Dict, Any, List

PERK_LEVELS = (3, 6, 10)

_FALLBACK = {
    "shield": {"name": "Shield", "tags": ["all"], "desc": "최대 HP +20%"},
    "rapid": {"name": "Rapid", "tags": ["all"], "desc": "공격속도 +20%"},
    "duelist": {"name": "Duelist", "tags": ["duel"], "desc": "1v1에서 공격력 +15%"},
    "lifesteal": {"name": "LifeSteal", "tags": ["duel", "swarm"], "desc": "공격 시 피해량의 10% 회복"},
    "execute": {"name": "Execute", "tags": ["duel"], "desc": "상대 HP 25% 이하 추가 피해"},
    "cleave": {"name": "Cleave", "tags": ["swarm"], "desc": "1vN에서 주변 적에게 50% 스플래시"},
}

def _find_perk_json(path: str) -> Path | None:
    p = Path(path)
    if p.is_absolute():
        return p if p.exists() else None
    
    here = Path(__file__).resolve()
    candidates = [
        here.parent / p,            # common/perks.json
        here.parent.parent / p,     # project_root/perks.json
        Path.cwd() / p,             # 실행 위치 기준
    ]
    for c in candidates:
        if c.exists():
            return c
    return None

def load_perk_catalog(path: str = "perks.json") -> Dict[str, Dict[str, Any]]:
    """
    perks.json에서 perk 카탈로그를 로드해서 {perk_id: meta} 형태로 반환.
    - meta 예: {"name": "...", "tags": [...], "desc": "..."}
    - 형태 지원:
      1) {"version":1, "perks": {...}}
      2) {...} (곧바로 catalog)
    """
    perk_path = _find_perk_json(path)
    if perk_path is None:
        return dict(_FALLBACK)
    
    try:
        raw = json.loads(perk_path.read_text(encoding="utf-8"))
    except Exception:
        return dict(_FALLBACK)
    
    if isinstance(raw, dict) and isinstance(raw.get("perks"), dict):
        catalog = raw["perks"]
    elif isinstance(raw, dict):
        catalog = raw
    else:
        return dict(_FALLBACK)
    
    out: Dict[str, Dict[str, Any]] = {}
    for perk_id, meta in catalog.items():
        if not isinstance(perk_id, str) or not perk_id.strip():
            continue
        if not isinstance(meta, dict):
            meta = {}
        out[perk_id] = {
            "name": str(meta.get("name", perk_id)),
            "tags": list(meta.get("tags" or [])),
            "desc": str(meta.get("desc", "")),
        }
    return out if out else dict(_FALLBACK)

def perk_count_for_level(level: int, perk_levels=PERK_LEVELS) -> int:
    level = int(level)
    return sum(1 for lv in perk_levels if level >= lv)

def set_level_linear(unit, new_level: int, max_level: int = 10, max_perks: int = 3) -> None:
    """
    Unit의 hp/atk가 (base + (level-1)*per_level) 구조라고 가정하고
    레벨을 new_level로 세팅하면서 hp/atk도 같이 재계산.
    """
    try:
        new_level = int(new_level)
    except Exception:
        new_level = 1
    new_level = max(1, min(int(max_level), new_level))

    cur_level = int(getattr(unit, "level", 1) or 1)
    hp = float(getattr(unit, "hp", 0) or 0)
    atk = float(getattr(unit, "atk", 0) or 0)
    hp_pl = float(getattr(unit, "hp_per_level", 0) or 0)
    atk_pl = float(getattr(unit, "atk_per_level", 0) or 0)

    base_hp = hp - (cur_level - 1) * hp_pl
    base_atk = atk - (cur_level - 1) * atk_pl

    setattr(unit, "level", new_level)
    setattr(unit, "hp", int(round(base_hp + (new_level - 1) * hp_pl)))
    setattr(unit, "atk", int(round(base_atk + (new_level - 1) * atk_pl)))

    # 레벨 다운 시 perk 개수도 줄이는 게 안전
    need = min(perk_count_for_level(new_level), max_perks)
    cur = list(getattr(unit, "perks", []) or [])
    if len(cur) > need:
        setattr(unit, "perks", cur[:need])

def eligible_perk_ids(perk_catalog: Dict[str, Any], encounter_type: str) -> List[str]:
    ctx = (encounter_type or "duel").strip().lower()
    out: List[str] = []
    for pid, meta in perk_catalog.items():
        if not isinstance(meta, dict):
            meta = {}
        tags = [str(t).lower() for t in (meta.get("tags") or [])]
        if "all" in tags or ctx in tags:
            out.append(pid)
    return out

def auto_assign_perks(unit, perk_catalog: Dict[str, Any], encounter_type: str, rnd: random.Random,
                      overwrite: bool = False, max_perks: int = 3) -> List[str]:
    """
    unit.level 기준(3/6/10)으로 필요한 perk 개수를 채운다.
    - overwrite=False: 기존 perk 유지 + 부족분만 추가
    - overwrite=True : 기존 perk 초기화 후 다시 채움
    반환: 이번에 새로 추가된 perk_id 리스트
    """
    need = min(perk_count_for_level(getattr(unit, "level", 1)), max_perks)

    if overwrite:
        setattr(unit, "perks", [])
    cur = list(getattr(unit, "perks", []) or [])

    remain = max(0, need - len(cur))
    if remain <= 0:
        return []

    pool = [pid for pid in eligible_perk_ids(perk_catalog, encounter_type) if pid not in cur]
    rnd.shuffle(pool)
    picked = pool[:remain]
    cur.extend(picked)
    setattr(unit, "perks", cur)
    return picked
