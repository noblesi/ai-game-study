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


_JSON_BLOCK_RE = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)


def load_scenarios_from_markdown(pattern: str = "battle_scenarios_*.md") -> List[Dict[str, Any]]:
    """현재 작업 디렉터리에서 pattern에 매칭되는 md 파일들을 찾아 json 코드블록 시나리오를 로드한다."""
    scenarios: List[Dict[str, Any]] = []

    for p in sorted(Path(".").glob(pattern)):
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # 일부 환경에서 cp949 등으로 저장된 경우가 있을 수 있어 fallback
            text = p.read_text(encoding="utf-8", errors="ignore")

        blocks = _JSON_BLOCK_RE.findall(text)
        if not blocks:
            continue

        for raw in blocks:
            raw = raw.strip()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"시나리오 JSON 파싱 실패: {p} (line {e.lineno}, col {e.colno})"
                ) from e

            # 최소 검증
            if not isinstance(data, dict):
                continue
            if "attacker_spec" not in data or "defender_spec" not in data:
                continue

            data["_source"] = str(p)
            scenarios.append(data)

    return scenarios
