from __future__ import annotations

import argparse
import csv
import random
from collections import Counter
from typing import Any, Dict, List, Tuple

NUM_KEYS = [
    # base
    "a_hp", "a_atk", "a_range", "a_attack_speed", "a_move_speed",
    "d_hp", "d_atk", "d_range", "d_attack_speed", "d_move_speed",
    # derived (export_dataset.py에서 추가됨)
    "a_dps", "d_dps", "a_ttk_est", "d_ttk_est",
    "dps_adv", "range_adv", "ttk_adv",
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
        # 최소 구현: 누락은 0.0으로 채워서 usable rows를 유지
        vals[k] = 0.0 if v is None else v


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

    # derived features
    x.extend([
        vals["a_dps"], vals["d_dps"], vals["a_ttk_est"], vals["d_ttk_est"],
        vals["dps_adv"], vals["range_adv"], vals["ttk_adv"],
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

def lr_scores(train, test, class_weight=None):
    """
    sklearn LogisticRegression을 학습하고 점수만 반환(출력 X)
    return: (train_acc, test_acc, test_bal_acc) or None
    """
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import Pipeline
        from sklearn.metrics import balanced_accuracy_score
    except Exception:
        return None

    X_train = [x for x, _ in train]
    y_train = [y for _, y in train]
    X_test = [x for x, _ in test]
    y_test = [y for _, y in test]

    clf = Pipeline([
        ("scaler", StandardScaler()),
        ("lr", LogisticRegression(max_iter=400, class_weight=class_weight)),
    ])
    clf.fit(X_train, y_train)

    train_acc = clf.score(X_train, y_train)
    test_acc = clf.score(X_test, y_test)

    y_pred = clf.predict(X_test)
    test_bal = balanced_accuracy_score(y_test, y_pred)

    return train_acc, test_acc, test_bal



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

    # 전체 기준 다수 클래스 baseline(참고용)
    majority = 1 if ys.count(1) > ys.count(0) else 0
    majority_acc_all = sum(1 for y in ys if y == majority) / len(ys)
    print(f"[MAJORITY BASELINE / ALL] always={majority} acc={majority_acc_all:.4f}")

    if len(data) < 10:
        print("[WARN] usable rows too small. Run more scenarios/experiments first.")
        return

    # ===== 반복 평가(운빨 줄이기) =====
    K = 10

    def predict_rule(x: List[float]) -> int:
        # x 구성: [a...5, d...5, deltas...5]
        dhp = x[10]
        datk = x[11]
        drng = x[12]
        score = datk + 0.25 * dhp + 0.5 * drng
        return 1 if score > 0 else 0

    rule_accs = []
    maj_accs = []
    sk_accs = []

    lr_accs = []
    lr_bal_accs = []
    lrb_accs = []
    lrb_bal_accs = []
    
    for i in range(K):
        train, test = split_xy(data, test_ratio=args.test_ratio, seed=args.seed + i)

        # split별 majority baseline(훈련셋 기준) → 테스트셋 평가
        y_train = [y for _, y in train]
        maj = 1 if y_train.count(1) > y_train.count(0) else 0
        maj_acc = sum(1 for _, y in test if y == maj) / len(test)
        maj_accs.append(maj_acc)

        # rule baseline
        rule_acc = sum(1 for x, y in test if predict_rule(x) == y) / len(test)
        rule_accs.append(rule_acc)

        # ---- sklearn LR 점수 수집(출력 없음) ----
        lr = lr_scores(train, test, class_weight=None)
        if lr is not None:
            lr_accs.append(lr[1])       # test_acc
            lr_bal_accs.append(lr[2])   # test_bal_acc

        lrb = lr_scores(train, test, class_weight="balanced")
        if lrb is not None:
            lrb_accs.append(lrb[1])     # test_acc
            lrb_bal_accs.append(lrb[2]) # test_bal_acc

    print("[MAJORITY BASELINE / SPLIT]")
    print(f"- test_acc mean={sum(maj_accs)/K:.4f} min={min(maj_accs):.4f} max={max(maj_accs):.4f}")

    print("[RULE BASELINE / SPLIT]")
    print(f"- test_acc mean={sum(rule_accs)/K:.4f} min={min(rule_accs):.4f} max={max(rule_accs):.4f}")

    if lr_accs:
        n = len(lr_accs)
        print("[SKLEARN LogisticRegression / SPLIT]")
        print(f"- test_acc mean={sum(lr_accs)/n:.4f} min={min(lr_accs):.4f} max={max(lr_accs):.4f}")
        print(f"- test_bal mean={sum(lr_bal_accs)/n:.4f} min={min(lr_bal_accs):.4f} max={max(lr_bal_accs):.4f}")
    else:
        print("[INFO] sklearn LogisticRegression not available (lr_scores returned None).")

    if lrb_accs:
        n = len(lrb_accs)
        print("[SKLEARN LogisticRegression (class_weight=balanced) / SPLIT]")
        print(f"- test_acc mean={sum(lrb_accs)/n:.4f} min={min(lrb_accs):.4f} max={max(lrb_accs):.4f}")
        print(f"- test_bal mean={sum(lrb_bal_accs)/n:.4f} min={min(lrb_bal_accs):.4f} max={max(lrb_bal_accs):.4f}")






if __name__ == "__main__":
    main()