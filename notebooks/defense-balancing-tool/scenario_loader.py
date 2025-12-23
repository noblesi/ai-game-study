"""Markdown(.md)에 포함된 ```json 시나리오 스펙 블록을 로드하는 유틸.

- battle_scenarios_*.md 파일에 아래 형태의 JSON 코드블록을 넣으면 자동으로 시나리오를 인식한다.

```json
{
  "title": "Knight vs Goblin",
  "attacker_spec": {...},
  "defender_spec": {...},
  "trials": 100,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [5.0, 0.0],
  "verbose_each": false
}
```

- 하나의 md 파일에 JSON 블록이 여러 개 있으면 모두 로드한다.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List


_JSON_BLOCK_RE = re.compile(
    r"```json\s*(?P<json>\{.*?\})\s*```",
    re.DOTALL | re.IGNORECASE,
)



def load_scenarios_from_markdown(path: str | None = None) -> List[Dict]:
    """
    battle_scenarios_*.md 파일에서 ```json ... ``` 블록을 찾아
    시나리오 딕셔너리 목록으로 반환한다.

    v1: attacker_spec / defender_spec 만 있는 구조
    v2: attacker_name / defender_name 로 units.json 을 참조하는 구조
    둘 다 지원한다.
    """
    if path is None:
        md_files = sorted(Path(".").glob("battle_scenarios_*.md"))
        if not md_files:
            return []
    else:
        md_files = [Path(path)]
        if not md_files[0].exists():
            return []

    scenarios: List[Dict] = []

    for p in md_files:
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            continue

        for m in _JSON_BLOCK_RE.finditer(text):
            raw = m.group(1)
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue

            if not isinstance(data, dict):
                continue

            # --- v1: 인라인 스펙 존재 여부 ---
            has_specs = "attacker_spec" in data and "defender_spec" in data

            # --- v2: 이름 참조 존재 여부 ---
            def _has_non_empty_str(key: str) -> bool:
                v = data.get(key)
                return isinstance(v, str) and v.strip() != ""

            has_names = _has_non_empty_str("attacker_name") or _has_non_empty_str("defender_name")

            # 둘 다 없으면 시나리오로 보기 애매하니 스킵
            if not (has_specs or has_names):
                continue

            # 구버전 호환: spec만 있는 경우에도 목록에서 이름을 보여주기 위해 name 채우기
            if has_specs:
                if not _has_non_empty_str("attacker_name"):
                    a_spec = data.get("attacker_spec") or {}
                    if isinstance(a_spec, dict):
                        n = a_spec.get("name")
                        if isinstance(n, str):
                            data["attacker_name"] = n

                if not _has_non_empty_str("defender_name"):
                    d_spec = data.get("defender_spec") or {}
                    if isinstance(d_spec, dict):
                        n = d_spec.get("name")
                        if isinstance(n, str):
                            data["defender_name"] = n

            # 메타정보: 이 시나리오가 어느 파일에서 왔는지
            data["_source"] = str(p)
            scenarios.append(data)

    return scenarios
