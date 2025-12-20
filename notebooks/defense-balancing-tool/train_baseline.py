from __future__ import annotations

import argparse
import csv
import random
from collections import Counter
from typing import Any, Dict, List, Tuple

# build_features()의 x 벡터 순서와 반드시 동일해야 함
FEATURE_NAMES = [
    # base attacker(5)
    "a_hp", "a_atk", "a_range", "a_attack_speed", "a_move_speed",
    # base defender(5)
    "d_hp", "d_atk", "d_range", "d_attack_speed", "d_move_speed",
    # deltas(5)
    "dhp", "datk", "drange", "dattack_speed", "dmove_speed",
    # derived(7) - export_dataset.py에서 추가한 컬럼을 x에 넣었다는 가정
    "a_dps", "d_dps", "a_ttk_est", "d_ttk_est",
    "dps_adv", "range_adv", "ttk_adv",
]


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

import os
import datetime
from typing import Optional

def _cm_from_preds(y_true: List[int], y_pred: List[int]) -> List[List[int]]:
    # rows: true(0/1), cols: pred(0/1) => [[TN, FP],[FN, TP]]
    tn = fp = fn = tp = 0
    for yt, yp in zip(y_true, y_pred):
        if yt == 0 and yp == 0:
            tn += 1
        elif yt == 0 and yp == 1:
            fp += 1
        elif yt == 1 and yp == 0:
            fn += 1
        elif yt == 1 and yp == 1:
            tp += 1
    return [[tn, fp], [fn, tp]]

def _metrics_from_cm(cm: List[List[int]]) -> Dict[str, float]:
    tn, fp = cm[0]
    fn, tp = cm[1]
    n = tn + fp + fn + tp

    acc = (tp + tn) / n if n else 0.0

    # label=1 metrics
    precision_1 = tp / (tp + fp) if (tp + fp) else 0.0
    recall_1 = tp / (tp + fn) if (tp + fn) else 0.0
    f1_1 = (2 * precision_1 * recall_1 / (precision_1 + recall_1)) if (precision_1 + recall_1) else 0.0

    # balanced accuracy
    tpr = recall_1
    tnr = tn / (tn + fp) if (tn + fp) else 0.0
    bal_acc = (tpr + tnr) / 2.0

    return {
        "acc": acc,
        "bal_acc": bal_acc,
        "precision_1": precision_1,
        "recall_1": recall_1,
        "f1_1": f1_1,
    }

def _cm_add(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    return [
        [a[0][0] + b[0][0], a[0][1] + b[0][1]],
        [a[1][0] + b[1][0], a[1][1] + b[1][1]],
    ]

def _summ(vs: List[float]) -> Dict[str, float]:
    if not vs:
        return {"mean": 0.0, "min": 0.0, "max": 0.0}
    return {
        "mean": sum(vs) / len(vs),
        "min": min(vs),
        "max": max(vs),
    }

def _fmt3(x: float) -> str:
    return f"{x:.4f}"

def _fmt_cm(cm: List[List[int]]) -> str:
    tn, fp = cm[0]
    fn, tp = cm[1]
    return f"TN={tn} FP={fp} FN={fn} TP={tp}"

def _default_report_path() -> str:
    ts = datetime.datetime.now().strftime("%Y%m%d")
    return os.path.join("reports", f"baseline_eval_{ts}.md")


def fit_predict_lr(train, test, class_weight=None, seed: int = 0) -> Optional[List[int]]:
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import Pipeline
    except Exception:
        return None

    X_train = [x for x, _ in train]
    y_train = [y for _, y in train]
    X_test = [x for x, _ in test]

    clf = Pipeline([
        ("scaler", StandardScaler()),
        ("lr", LogisticRegression(max_iter=400, class_weight=class_weight)),
    ])
    clf.fit(X_train, y_train)
    return list(map(int, clf.predict(X_test)))


def fit_predict_tree(train, test, model: str, class_weight=None, seed: int = 0) -> Optional[List[int]]:
    """
    model: "dt" | "rf"
    """
    try:
        if model == "dt":
            from sklearn.tree import DecisionTreeClassifier
            clf = DecisionTreeClassifier(class_weight=class_weight, random_state=seed)
        elif model == "rf":
            from sklearn.ensemble import RandomForestClassifier
            clf = RandomForestClassifier(
                n_estimators=200,
                class_weight=class_weight,
                random_state=seed,
                n_jobs=-1,
            )
        else:
            return None
    except Exception:
        return None

    X_train = [x for x, _ in train]
    y_train = [y for _, y in train]
    X_test = [x for x, _ in test]

    clf.fit(X_train, y_train)
    return list(map(int, clf.predict(X_test)))


def write_report_md(
    path: str,
    *,
    input_path: str,
    n_rows: int,
    n_usable: int,
    label_dist: Dict[int, int],
    test_ratio: float,
    seed: int,
    K: int,
    results: Dict[str, Dict[str, Any]],
) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    lines: List[str] = []
    lines.append(f"# Baseline Evaluation Report\n")
    lines.append(f"- generated_at: {datetime.datetime.now().isoformat(timespec='seconds')}\n")
    lines.append(f"- input: {input_path}\n")
    lines.append(f"- rows: {n_rows}\n")
    lines.append(f"- usable_rows: {n_usable}\n")
    lines.append(f"- label_distribution: {label_dist}\n")
    lines.append(f"- test_ratio: {test_ratio}\n")
    lines.append(f"- seed: {seed}\n")
    lines.append(f"- K(splits): {K}\n\n")

    lines.append("## Summary\n\n")
    lines.append("| model | acc(mean) | bal_acc(mean) | f1_1(mean) | recall_1(mean) | precision_1(mean) | confusion_sum |\n")
    lines.append("|---|---:|---:|---:|---:|---:|---|\n")

    for name, pack in results.items():
        s_acc = pack["acc"]
        s_bal = pack["bal_acc"]
        s_f1 = pack["f1_1"]
        s_r = pack["recall_1"]
        s_p = pack["precision_1"]
        cm = pack["cm_sum"]

        lines.append(
            f"| {name} | {_fmt3(s_acc['mean'])} | {_fmt3(s_bal['mean'])} | {_fmt3(s_f1['mean'])} | "
            f"{_fmt3(s_r['mean'])} | {_fmt3(s_p['mean'])} | {_fmt_cm(cm)} |\n"
        )

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)

from typing import Tuple

def pick_best_model(packed: Dict[str, Dict[str, Any]], metric_key: str = "f1_1") -> str:
    """
    packed[name][metric_key]['mean']이 가장 큰 모델을 선택.
    MAJORITY 계열은 제외.
    """
    best_name = ""
    best_score = -1.0
    for name, pck in packed.items():
        if name.startswith("MAJORITY"):
            continue
        score = pck.get(metric_key, {}).get("mean", -1.0)
        if score > best_score:
            best_score = score
            best_name = name
    return best_name


def fit_full_model_and_rank_features(
    model_name: str,
    X: List[List[float]],
    y: List[int],
    feature_names: List[str],
    seed: int,
) -> Tuple[str, List[Tuple[str, float]]]:
    """
    best 모델을 전체 데이터로 재학습하고, feature importance(또는 coef 절대값) Top을 반환.
    return: (kind, [(feature, score), ...])
      kind: "lr_coef_abs" | "tree_importance" | "unsupported"
    """
    # 길이 불일치 방지
    if not X or not feature_names:
        return "unsupported", []
    if len(X[0]) != len(feature_names):
        print(f"[WARN] FEATURE_NAMES length mismatch: x_dim={len(X[0])} names={len(feature_names)}")
        # 그래도 가능한 범위까지만 자르기
        m = min(len(X[0]), len(feature_names))
        feature_names = feature_names[:m]
        X = [row[:m] for row in X]

    # ---- Logistic Regression 계열 ----
    if model_name in ("LR", "LR_balanced"):
        try:
            from sklearn.linear_model import LogisticRegression
            from sklearn.preprocessing import StandardScaler
            from sklearn.pipeline import Pipeline
        except Exception:
            return "unsupported", []

        cw = None if model_name == "LR" else "balanced"

        clf = Pipeline([
            ("scaler", StandardScaler()),
            ("lr", LogisticRegression(max_iter=400, class_weight=cw)),
        ])
        clf.fit(X, y)

        lr = clf.named_steps["lr"]
        coefs = lr.coef_[0]  # shape: (n_features,)
        ranked = sorted(
            [(feature_names[i], abs(float(coefs[i]))) for i in range(len(feature_names))],
            key=lambda t: t[1],
            reverse=True,
        )
        return "lr_coef_abs", ranked

    # ---- Tree 계열 ----
    if model_name in ("DT_balanced", "RF_balanced_subsample"):
        try:
            if model_name == "DT_balanced":
                from sklearn.tree import DecisionTreeClassifier
                clf = DecisionTreeClassifier(class_weight="balanced", random_state=seed)
            else:
                from sklearn.ensemble import RandomForestClassifier
                clf = RandomForestClassifier(
                    n_estimators=200,
                    class_weight="balanced_subsample",
                    random_state=seed,
                    n_jobs=-1,
                )
        except Exception:
            return "unsupported", []

        clf.fit(X, y)
        importances = getattr(clf, "feature_importances_", None)
        if importances is None:
            return "unsupported", []

        ranked = sorted(
            [(feature_names[i], float(importances[i])) for i in range(len(feature_names))],
            key=lambda t: t[1],
            reverse=True,
        )
        return "tree_importance", ranked

    return "unsupported", []



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
    p.add_argument("--report", default="", help="md 리포트 저장 경로(비우면 reports/baseline_eval_YYYYMMDD.md)")
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

    # 모델별 결과 수집 컨테이너
    model_names = [
        "MAJORITY_SPLIT",
        "LR",
        "LR_balanced",
        "DT_balanced",
        "RF_balanced_subsample",
    ]

    results: Dict[str, Dict[str, Any]] = {}
    for name in model_names:
        results[name] = {
            "acc": [],
            "bal_acc": [],
            "precision_1": [],
            "recall_1": [],
            "f1_1": [],
            "cm_sum": [[0, 0], [0, 0]],
            "available": True,
        }

    def _record(name: str, y_true: List[int], y_pred: List[int]) -> None:
        cm = _cm_from_preds(y_true, y_pred)
        m = _metrics_from_cm(cm)
        results[name]["acc"].append(m["acc"])
        results[name]["bal_acc"].append(m["bal_acc"])
        results[name]["precision_1"].append(m["precision_1"])
        results[name]["recall_1"].append(m["recall_1"])
        results[name]["f1_1"].append(m["f1_1"])
        results[name]["cm_sum"] = _cm_add(results[name]["cm_sum"], cm)

    for i in range(K):
        split_seed = args.seed + i
        train, test = split_xy(data, test_ratio=args.test_ratio, seed=split_seed)

        X_test = [x for x, _ in test]
        y_test = [y for _, y in test]

        # ---- MAJORITY baseline (훈련셋 기준) ----
        y_train = [y for _, y in train]
        maj = 1 if y_train.count(1) > y_train.count(0) else 0
        y_pred_maj = [maj] * len(y_test)
        _record("MAJORITY_SPLIT", y_test, y_pred_maj)

        # ---- LogisticRegression ----
        pred = fit_predict_lr(train, test, class_weight=None, seed=split_seed)
        if pred is None:
            results["LR"]["available"] = False
        else:
            _record("LR", y_test, pred)

        pred = fit_predict_lr(train, test, class_weight="balanced", seed=split_seed)
        if pred is None:
            results["LR_balanced"]["available"] = False
        else:
            _record("LR_balanced", y_test, pred)

        # ---- DecisionTree / RandomForest ----
        pred = fit_predict_tree(train, test, model="dt", class_weight="balanced", seed=split_seed)
        if pred is None:
            results["DT_balanced"]["available"] = False
        else:
            _record("DT_balanced", y_test, pred)

        pred = fit_predict_tree(train, test, model="rf", class_weight="balanced_subsample", seed=split_seed)
        if pred is None:
            results["RF_balanced_subsample"]["available"] = False
        else:
            _record("RF_balanced_subsample", y_test, pred)

    # ---- 요약 출력 ----
    packed: Dict[str, Dict[str, Any]] = {}
    for name in model_names:
        if not results[name]["available"]:
            continue

        packed[name] = {
            "acc": _summ(results[name]["acc"]),
            "bal_acc": _summ(results[name]["bal_acc"]),
            "precision_1": _summ(results[name]["precision_1"]),
            "recall_1": _summ(results[name]["recall_1"]),
            "f1_1": _summ(results[name]["f1_1"]),
            "cm_sum": results[name]["cm_sum"],
        }

    # 콘솔 출력(모델별)
    for name, pck in packed.items():
        print(f"[{name}]")
        print(f"- acc      mean={_fmt3(pck['acc']['mean'])} min={_fmt3(pck['acc']['min'])} max={_fmt3(pck['acc']['max'])}")
        print(f"- bal_acc  mean={_fmt3(pck['bal_acc']['mean'])} min={_fmt3(pck['bal_acc']['min'])} max={_fmt3(pck['bal_acc']['max'])}")
        print(f"- f1_1     mean={_fmt3(pck['f1_1']['mean'])} min={_fmt3(pck['f1_1']['min'])} max={_fmt3(pck['f1_1']['max'])}")
        print(f"- recall_1 mean={_fmt3(pck['recall_1']['mean'])} min={_fmt3(pck['recall_1']['min'])} max={_fmt3(pck['recall_1']['max'])}")
        print(f"- prec_1   mean={_fmt3(pck['precision_1']['mean'])} min={_fmt3(pck['precision_1']['min'])} max={_fmt3(pck['precision_1']['max'])}")
        print(f"- cm_sum   {_fmt_cm(pck['cm_sum'])}")
        print()

    # ===== best 모델 선택(F1_1 기준) =====
    best = pick_best_model(packed, metric_key="f1_1")
    if not best:
        print("[WARN] no best model selected.")
    else:
        print(f"[BEST MODEL] by f1_1 mean: {best} (f1_1_mean={packed[best]['f1_1']['mean']:.4f})")

        # 전체 데이터로 재학습 + feature 랭킹
        X_all = [x for x, _ in data]
        y_all = [yy for _, yy in data]

        kind, ranked = fit_full_model_and_rank_features(
            best,
            X_all,
            y_all,
            FEATURE_NAMES,
            seed=args.seed,
        )

        topk = 12
        if ranked:
            print(f"[TOP FEATURES] ({kind}) top {topk}")
            for name, score in ranked[:topk]:
                print(f"- {name}: {score:.6f}")
        else:
            print("[INFO] feature ranking unavailable.")


    # ---- 리포트 저장 ----
    report_path = args.report.strip() or _default_report_path()
    write_report_md(
        report_path,
        input_path=args.input,
        n_rows=len(rows),
        n_usable=len(data),
        label_dist=dict(Counter(ys)),
        test_ratio=args.test_ratio,
        seed=args.seed,
        K=K,
        results=packed,
    )

    # 리포트에 best/top-features append
    try:
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n## Best Model\n\n")
            if best:
                f.write(f"- metric: f1_1(mean)\n")
                f.write(f"- best: {best}\n")
                f.write(f"- f1_1_mean: {packed[best]['f1_1']['mean']:.4f}\n\n")
            else:
                f.write("- best: (none)\n\n")

            f.write("## Top Features (fit on full data)\n\n")
            if best and ranked:
                f.write(f"- kind: {kind}\n\n")
                f.write("| rank | feature | score |\n|---:|---|---:|\n")
                for i, (fname, score) in enumerate(ranked[:12], start=1):
                    f.write(f"| {i} | {fname} | {score:.6f} |\n")
            else:
                f.write("- (unavailable)\n")
        print("[OK] appended best/top-features to report.")
    except Exception as e:
        print(f"[WARN] failed to append report: {e}")


    print(f"[OK] wrote report: {report_path}")


if __name__ == "__main__":
    main()