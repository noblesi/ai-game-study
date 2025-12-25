from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple


def append_jsonl(path: str, record: dict) -> None:
    """record(dict)를 JSONL 한 줄로 append 저장한다. (디렉터리 자동 생성)"""
    p = Path(path)
    if p.parent and str(p.parent) != ".":
        p.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(record, dict) and "logged_at" not in record:
        record = {**record, "logged_at": datetime.now().isoformat(timespec="seconds")}

    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_jsonl(
    path: str,
    *,
    require_dict: bool = True,
    add_line_key: str | None = None,
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """JSONL 파일을 안전하게 읽어서 (records, errors)를 반환."""
    records: List[Dict[str, Any]] = []
    errors: List[str] = []

    if not os.path.exists(path):
        return records, [f"File not found: {path}"]

    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception as e:
                errors.append(f"{path} L{i}: JSON parse error: {e}")
                continue

            if require_dict and not isinstance(obj, dict):
                errors.append(f"{path} L{i}: not a dict ({type(obj).__name__})")
                continue

            if isinstance(obj, dict):
                if add_line_key:
                    obj[add_line_key] = i
                records.append(obj)
            else:
                records.append({"value": obj, "_line": i})

    return records, errors


def schema_of(r: Dict[str, Any]) -> str:
    v = r.get("schema_version")
    return v if isinstance(v, str) and v.strip() else "legacy"


def short_id(x: Any, n: int = 8) -> str:
    if not isinstance(x, str):
        return "-"
    x = x.strip()
    return x[:n] if x else "-"
