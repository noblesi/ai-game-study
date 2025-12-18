from __future__ import annotations

import argparse
import csv
import random
from collections import Counter
from typing import Any, Dict, List, Tuple

NUM_KEYS = [
    "a_hp", "a_atk", "a_range", "a_attack_speed", "a_move_speed",
    "d_hp", "d_atk", "d_range", "d_attack_speed", "d_move_speed",
]

def to_float(x: Any) -> float | None:
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).strip()
    if not s:
        return None
    try:
        return float(s)
    except Exception:
        return None


def load_csv(path: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append(row)
    return rows


def build_features(row: Dict[str, Any]) -> Tuple[List[float], int] | None:
    y_raw = row.get("label_attacker_better", "")
    try:
        y = int(float(y_raw))
    except Exception:
        return None
    if y not in (0, 1):
        return None

    vals: Dict[str, float] = {}
    for k in NUM_KEYS:
        v = to_float(row.get(k))
        if v is None:
            # 숫자 피처가 하나라도 없으면 스킵(최소 구현)
            return None
        vals[k] = v

    # 기본 피처 + 차이(deltas)
    x: List[float] = []
    x.extend([vals["a_hp"], vals["a_atk"], vals["a_range"], vals["a_attack_speed"], vals["a_move_speed"]])
    x.extend([vals["d_hp"], vals["d_atk"], vals["d_range"], vals["d_attack_speed"], vals["d_move_speed"]])

    x.extend([
        vals["a_hp"] - vals["d_hp"],
        vals["a_atk"] - vals["d_atk"],
        vals["a_range"] - vals["d_range"],
        vals["a_attack_speed"] - vals["d_attack_speed"],
        vals["a_move_speed"] - vals["d_move_speed"],
    ])

    return x, y


def split_xy(data: List[Tuple[List[float], int]], test_ratio: float, seed: int) -> Tuple[List, List]:
    rnd = random.Random(seed)
    data2 = data[:]
    rnd.shuffle(data2)
    n_test = max(1, int(len(data2) * test_ratio))
    test = data2[:n_test]
    train = data2[n_test:]
    return train, test


def eval_rule_baseline(train: List[Tuple[List[float], int]], test: List[Tuple[List[float], int]]) -> None:
    # 규칙 베이스라인: (ATK 차이) + 0.25*(HP 차이) + 0.5*(Range 차이) > 0 이면 attacker가 더 좋다
    def predict(x: List[float]) -> int:
        # x 구성: [a...5, d...5, deltas...5]
        dhp = x[10]
        datk = x[11]
        drng = x[12]
        score = datk + 0.25 * dhp + 0.5 * drng
        return 1 if score > 0 else 0

    def acc(dataset: List[Tuple[List[float], int]]) -> float:
        c = 0
        for x, y in dataset:
            c += (predict(x) == y)
        return c / max(1, len(dataset))

    print("[RULE BASELINE]")
    print(f"- train_acc: {acc(train):.4f}")
    print(f"- test_acc : {acc(test):.4f}")


def eval_sklearn_if_available(train: List[Tuple[List[float], int]], test: List[Tuple[List[float], int]]) -> bool:
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import Pipeline
    except Exception:
        return False

    X_train = [x for x, _ in train]
    y_train = [y for _, y in train]
    X_test = [x for x, _ in test]
    y_test = [y for _, y in test]

    clf = Pipeline([
        ("scaler", StandardScaler()),
        ("lr", LogisticRegression(max_iter=300)),
    ])
    clf.fit(X_train, y_train)

    train_acc = clf.score(X_train, y_train)
    test_acc = clf.score(X_test, y_test)

    print("[SKLEARN LogisticRegression]")
    print(f"- train_acc: {train_acc:.4f}")
    print(f"- test_acc : {test_acc:.4f}")
    return True


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="datasets/battle_dataset_v1.csv")
    p.add_argument("--test-ratio", type=float, default=0.2)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    rows = load_csv(args.input)
    data: List[Tuple[List[float], int]] = []
    for row in rows:
        item = build_features(row)
        if item is not None:
            data.append(item)

    print(f"[INFO] input rows: {len(rows)}")
    print(f"[INFO] usable rows: {len(data)}")

    ys = [y for _, y in data]
    print(f"[INFO] label distribution: {dict(Counter(ys))}")

    # 다수 클래스(majority)만 찍는 기준선
    majority = 1 if ys.count(1) > ys.count(0) else 0
    majority_acc = sum(1 for y in ys if y == majority) / len(ys)
    print(f"[MAJORITY BASELINE] always={majority} acc={majority_acc:.4f}")


    if len(data) < 10:
        print("[WARN] usable rows too small. Run more scenarios/experiments first.")
        return

    train, test = split_xy(data, test_ratio=args.test_ratio, seed=args.seed)

    used = eval_sklearn_if_available(train, test)
    if not used:
        # 여러 seed로 반복 평가해서 test_acc 변동을 줄임
        accs = []
        for i in range(10):
            train_i, test_i = split_xy(data, test_ratio=args.test_ratio, seed=args.seed + i)

            def predict(x):
                # x 구성: [a...5, d...5, deltas...5]
                dhp = x[10]
                datk = x[11]
                drng = x[12]
                score = datk + 0.25 * dhp + 0.5 * drng
                return 1 if score > 0 else 0

            test_acc = sum(1 for x, y in test_i if predict(x) == y) / len(test_i)
            accs.append(test_acc)

        print("[RULE BASELINE]")
        print(f"- test_acc mean={sum(accs)/len(accs):.4f} min={min(accs):.4f} max={max(accs):.4f}")



if __name__ == "__main__":
    main()