from __future__ import annotations

import json
import os
from typing import Any, Dict

# perks.json이 없을 때도 프로그램이 죽지 않게 하는 최소 기본값(기존에 쓰던 것들)
_FALLBACK = {
    "shield": {"name": "Shield", "tags": ["all"], "desc": "최대 HP +20%"},
    "rapid": {"name": "Rapid", "tags": ["all"], "desc": "공격속도 +20%"},
    "duelist": {"name": "Duelist", "tags": ["duel"], "desc": "1v1에서 공격력 +15%"},
    "lifesteal": {"name": "LifeSteal", "tags": ["duel", "swarm"], "desc": "공격 시 피해량의 10% 회복"},
    "execute": {"name": "Execute", "tags": ["duel"], "desc": "상대 HP 25% 이하 추가 피해"},
    "cleave": {"name": "Cleave", "tags": ["swarm"], "desc": "1vN에서 주변 적에게 50% 스플래시"},
}

def load_perk_catalog(path: str = "perks.json") -> Dict[str, Dict[str, Any]]:
    """
    perks.json에서 perk 카탈로그를 로드해서 {perk_id: meta} 형태로 반환.
    - meta 예: {"name": "...", "tags": [...], "desc": "..."}
    """
    base_dir = os.path.dirname(__file__)
    abs_path = os.path.join(base_dir, path)

    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception:
        return dict(_FALLBACK)

    # 형태 지원:
    # 1) {"version":1, "perks": {...}}
    # 2) {...} (곧바로 catalog)
    catalog = None
    if isinstance(raw, dict) and isinstance(raw.get("perks"), dict):
        catalog = raw["perks"]
    elif isinstance(raw, dict):
        catalog = raw
    else:
        return dict(_FALLBACK)

    # 최소 검증
    out: Dict[str, Dict[str, Any]] = {}
    for perk_id, meta in catalog.items():
        if not isinstance(perk_id, str) or not perk_id.strip():
            continue
        if not isinstance(meta, dict):
            meta = {}
        out[perk_id] = {
            "name": str(meta.get("name", perk_id)),
            "tags": list(meta.get("tags") or []),
            "desc": str(meta.get("desc", "")),
        }

    return out if out else dict(_FALLBACK)
