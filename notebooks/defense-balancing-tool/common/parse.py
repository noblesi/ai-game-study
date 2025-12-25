from __future__ import annotations

import math
from typing import Any


def to_float(x: Any) -> float | None:
    """값을 안전하게 float으로 변환. 실패/빈값/NaN이면 None."""
    if x is None:
        return None
    if isinstance(x, (int, float)):
        v = float(x)
        return None if math.isnan(v) else v

    s = str(x).strip()
    if not s:
        return None

    try:
        v = float(s)
    except Exception:
        return None

    return None if math.isnan(v) else v


def safe_div(num: float | None, den: float | None) -> float | None:
    """0/None 안전 나눗셈."""
    if num is None or den is None:
        return None
    if den == 0:
        return None
    return num / den
