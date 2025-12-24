from __future__ import annotations

import argparse
import csv
import random
from collections import Counter
from typing import Any, Dict, List, Tuple

# (1) base(퍼크 제외) - "x를 만드는 순서" 그대로 적어야 함
BASE_FEATURE_NAMES = [
    # meta(3)  <<== x 맨 앞이 이 순서라면, 이름도 이 순서!
    "encounter_is_swarm", "defender_count", "start_distance",

    # base attacker(5)
    "a_hp", "a_atk", "a_range", "a_attack_speed", "a_move_speed",
    # base defender(5)
    "d_hp", "d_atk", "d_range", "d_attack_speed", "d_move_speed",

    # deltas(5)
    "dhp", "datk", "drange", "dattack_speed", "dmove_speed",

    # derived(7)
    "a_dps", "d_dps", "a_ttk_est", "d_ttk_est",
    "dps_adv", "range_adv", "ttk_adv",

    # perk count(3)
    "a_perk_count", "d_perk_count", "perk_count_adv",
]

# (2) row에서 숫자로 읽어올 키들
#  - encounter_is_swarm는 row에 없고 계산값이므로 여기 넣지 않음
BASE_NUM_KEYS = [
    "defender_count",
    "start_distance",

    "a_hp", "a_atk", "a_range", "a_attack_speed", "a_move_speed",
    "d_hp", "d_atk", "d_range", "d_attack_speed", "d_move_speed",

    "a_dps", "d_dps", "a_ttk_est", "d_ttk_est",
    "dps_adv", "range_adv", "ttk_adv",

    "a_perk_count", "d_perk_count",
]

FEATURE_NAMES: list[str] = []
NUM_KEYS: list[str] = []
PERK_IDS: list[str] = []


def rebuild_feature_schema():
    """PERK_IDS가 확정된 뒤, FEATURE_NAMES/NUM_KEYS를 항상 x와 동일하게 재구성."""
    global FEATURE_NAMES, NUM_KEYS
    FEATURE_NAMES = list(BASE_FEATURE_NAMES)
    NUM_KEYS = list(BASE_NUM_KEYS)

    # perk one-hot + advantage
    for pid in PERK_IDS:
        FEATURE_NAMES.extend([f"a_has_perk_{pid}", f"d_has_perk_{pid}", f"perk_adv_{pid}"])
        NUM_KEYS.extend([f"a_has_perk_{pid}", f"d_has_perk_{pid}"])


def detect_perk_ids(rows: list[dict]) -> list[str]:
    """CSV 컬럼에서 a_has_perk_* / d_has_perk_*를 모아 PERK_IDS 결정."""
    ids = set()
    if not rows:
        return []
    for k in rows[0].keys():
        if k.startswith("a_has_perk_"):
            ids.add(k[len("a_has_perk_"):])
        elif k.startswith("d_has_perk_"):
            ids.add(k[len("d_has_perk_"):])
    return sorted(ids)


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

    # encounter_type (categorical) -> 0/1
    enc = str(row.get("encounter_type") or "duel").strip().lower()
    encounter_is_swarm = 1.0 if enc == "swarm" else 0.0

    # meta 먼저 계산
    encounter_type = (row.get("encounter_type") or "").strip().lower()
    encounter_is_swarm = 1.0 if encounter_type == "swarm" else 0.0

    dc_raw = to_float(row.get("defender_count"))
    sd_raw = to_float(row.get("start_distance"))

    # duel 기본 1, swarm도 0/None이면 1로 보정
    if encounter_is_swarm < 0.5:
        defender_count = 1.0
    else:
        defender_count = 1.0 if (dc_raw is None or dc_raw <= 0) else float(dc_raw)

    start_distance = 0.0 if sd_raw is None else float(sd_raw)

    x: list[float] = []
    x.extend([encounter_is_swarm, defender_count, start_distance])
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

    # ===== Perk features =====
    a_pc = to_float(row.get("a_perk_count"))
    d_pc = to_float(row.get("d_perk_count"))
    a_pc = 0.0 if a_pc is None else a_pc
    d_pc = 0.0 if d_pc is None else d_pc

    # count + advantage
    x.extend([a_pc, d_pc, a_pc - d_pc])

    # one-hot + advantage (동적으로 감지된 PERK_IDS 사용)
    for pid in PERK_IDS:
        a_has = to_float(row.get(f"a_has_perk_{pid}"))
        d_has = to_float(row.get(f"d_has_perk_{pid}"))
        a_has = 0.0 if a_has is None else a_has
        d_has = 0.0 if d_has is None else d_has
        x.extend([a_has, d_has, a_has - d_has])


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

def fit_predict_proba_model(train, test, model_name: str, seed: int = 0):
    """
    model_name: "LR" | "LR_balanced" | "DT_balanced" | "RF_balanced_subsample"
    return: probas for class=1 (List[float]) or None
    """
    try:
        X_train = [x for x, _ in train]
        y_train = [y for _, y in train]
        X_test = [x for x, _ in test]
    except Exception:
        return None

    # LR 계열
    if model_name in ("LR", "LR_balanced"):
        try:
            from sklearn.linear_model import LogisticRegression
            from sklearn.preprocessing import StandardScaler
            from sklearn.pipeline import Pipeline
        except Exception:
            return None

        cw = None if model_name == "LR" else "balanced"
        clf = Pipeline([
            ("scaler", StandardScaler()),
            ("lr", LogisticRegression(max_iter=400, class_weight=cw)),
        ])
        clf.fit(X_train, y_train)
        proba = clf.predict_proba(X_test)[:, 1]
        return [float(p) for p in proba]

    # Tree 계열
    if model_name == "DT_balanced":
        try:
            from sklearn.tree import DecisionTreeClassifier
        except Exception:
            return None
        clf = DecisionTreeClassifier(class_weight="balanced", random_state=seed)
        clf.fit(X_train, y_train)
        proba = clf.predict_proba(X_test)[:, 1]
        return [float(p) for p in proba]

    if model_name == "RF_balanced_subsample":
        try:
            from sklearn.ensemble import RandomForestClassifier
        except Exception:
            return None
        clf = RandomForestClassifier(
            n_estimators=200,
            class_weight="balanced_subsample",
            random_state=seed,
            n_jobs=-1,
        )
        clf.fit(X_train, y_train)
        proba = clf.predict_proba(X_test)[:, 1]
        return [float(p) for p in proba]

    return None


def threshold_sweep_across_splits(
    *,
    model_name: str,
    data: List[Tuple[List[float], int]],
    split_mode: str,
    split_plan,
    K: int,
    seed_base: int,
    test_ratio: float,
    thr_step: float,
):
    """
    모든 split을 돌면서 threshold별 confusion matrix를 누적한 뒤
    f1_1이 최대가 되는 threshold를 선택.
    """
    thresholds = []
    t = thr_step
    while t < 1.0:
        thresholds.append(round(t, 4))
        t += thr_step
    if 0.5 not in thresholds:
        thresholds.append(0.5)
        thresholds.sort()

    cm_by_thr = {thr: [[0, 0], [0, 0]] for thr in thresholds}

    for i in range(K):
        split_seed = seed_base + i

        if split_mode == "group" and split_plan is not None:
            train_idx, test_idx = split_plan[i]
            train = [data[j] for j in train_idx]
            test = [data[j] for j in test_idx]
        else:
            train, test = split_xy(data, test_ratio=test_ratio, seed=split_seed)

        y_test = [y for _, y in test]
        prob = fit_predict_proba_model(train, test, model_name=model_name, seed=split_seed)
        if prob is None:
            return None

        for thr in thresholds:
            y_pred = [1 if p >= thr else 0 for p in prob]
            cm = _cm_from_preds(y_test, y_pred)
            cm_by_thr[thr] = _cm_add(cm_by_thr[thr], cm)

    # threshold별 지표 계산
    scored = []
    for thr, cm_sum in cm_by_thr.items():
        m = _metrics_from_cm(cm_sum)
        scored.append((thr, m, cm_sum))

    # F1_1 최대
    scored.sort(key=lambda x: x[1]["f1_1"], reverse=True)
    return scored  # [(thr, metrics, cm_sum), ...]

def _parse_int_list_csv(s: str) -> List[int]:
    parts = [p.strip() for p in str(s).split(",") if p.strip()]
    out: List[int] = []
    for p in parts:
        out.append(int(p))
    return out


def _parse_max_depth_list_csv(s: str) -> List[int | None]:
    parts = [p.strip() for p in str(s).split(",") if p.strip()]
    out: List[int | None] = []
    for p in parts:
        if p.lower() == "none":
            out.append(None)
        else:
            out.append(int(p))
    return out


def fit_predict_proba_rf(
    train: List[Tuple[List[float], int]],
    test: List[Tuple[List[float], int]],
    *,
    seed: int,
    n_estimators: int,
    max_depth: int | None,
    min_samples_leaf: int,
    class_weight: str = "balanced_subsample",
) -> List[float] | None:
    try:
        from sklearn.ensemble import RandomForestClassifier
    except Exception:
        return None

    X_train = [x for x, _ in train]
    y_train = [y for _, y in train]
    X_test = [x for x, _ in test]

    clf = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_leaf=min_samples_leaf,
        class_weight=class_weight,
        random_state=seed,
        n_jobs=-1,
    )
    clf.fit(X_train, y_train)
    proba = clf.predict_proba(X_test)[:, 1]
    return [float(p) for p in proba]


def rf_threshold_sweep_across_splits(
    *,
    data: List[Tuple[List[float], int]],
    split_mode: str,
    split_plan,
    K: int,
    seed_base: int,
    test_ratio: float,
    thr_step: float,
    n_estimators: int,
    max_depth: int | None,
    min_samples_leaf: int,
    class_weight: str = "balanced_subsample",
):
    """
    RF에 대해 split별로 predict_proba를 얻고, threshold sweep을 수행해
    f1_1이 최대가 되는 threshold를 반환한다.
    return: scored list [(thr, metrics, cm_sum), ...] or None
    """
    thresholds = []
    t = thr_step
    while t < 1.0:
        thresholds.append(round(t, 4))
        t += thr_step
    if 0.5 not in thresholds:
        thresholds.append(0.5)
        thresholds.sort()

    cm_by_thr = {thr: [[0, 0], [0, 0]] for thr in thresholds}

    for i in range(K):
        split_seed = seed_base + i

        if split_mode == "group" and split_plan is not None:
            train_idx, test_idx = split_plan[i]
            train = [data[j] for j in train_idx]
            test = [data[j] for j in test_idx]
        else:
            train, test = split_xy(data, test_ratio=test_ratio, seed=split_seed)

        y_test = [y for _, y in test]
        prob = fit_predict_proba_rf(
            train,
            test,
            seed=split_seed,
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_leaf=min_samples_leaf,
            class_weight=class_weight,
        )
        if prob is None:
            return None

        for thr in thresholds:
            y_pred = [1 if p >= thr else 0 for p in prob]
            cm = _cm_from_preds(y_test, y_pred)
            cm_by_thr[thr] = _cm_add(cm_by_thr[thr], cm)

    scored = []
    for thr, cm_sum in cm_by_thr.items():
        m = _metrics_from_cm(cm_sum)
        scored.append((thr, m, cm_sum))

    scored.sort(key=lambda x: x[1]["f1_1"], reverse=True)
    return scored


def rf_grid_search_best_by_f1(
    *,
    data: List[Tuple[List[float], int]],
    split_mode: str,
    split_plan,
    K: int,
    seed_base: int,
    test_ratio: float,
    thr_step: float,
    n_estimators: int,
    depths: List[int | None],
    min_leaves: List[int],
    class_weight: str = "balanced_subsample",
):
    """
    RF (max_depth, min_samples_leaf) 미니 그리드를 돌리고,
    각 설정에 대해 threshold sweep(F1 최대)을 수행한 뒤
    가장 좋은 설정을 반환한다.
    return:
      - best_params: dict or None
      - best_tuned: scored list or None
      - rows: list of dict (전체 결과, f1_1 desc 정렬)
    """
    rows: List[Dict[str, Any]] = []
    best_params: Dict[str, Any] | None = None
    best_tuned = None
    best_score = -1.0

    for d in depths:
        for leaf in min_leaves:
            tuned = rf_threshold_sweep_across_splits(
                data=data,
                split_mode=split_mode,
                split_plan=split_plan,
                K=K,
                seed_base=seed_base,
                test_ratio=test_ratio,
                thr_step=thr_step,
                n_estimators=n_estimators,
                max_depth=d,
                min_samples_leaf=leaf,
                class_weight=class_weight,
            )
            if tuned is None or not tuned:
                continue

            thr, m, cm = tuned[0]
            row = {
                "n_estimators": n_estimators,
                "max_depth": d,
                "min_samples_leaf": leaf,
                "thr": thr,
                "acc": m["acc"],
                "bal_acc": m["bal_acc"],
                "f1_1": m["f1_1"],
                "recall_1": m["recall_1"],
                "precision_1": m["precision_1"],
                "cm_sum": cm,
            }
            rows.append(row)

            if m["f1_1"] > best_score:
                best_score = m["f1_1"]
                best_params = {
                    "n_estimators": n_estimators,
                    "max_depth": d,
                    "min_samples_leaf": leaf,
                    "class_weight": class_weight,
                }
                best_tuned = tuned

    rows.sort(key=lambda r: r["f1_1"], reverse=True)
    return best_params, best_tuned, rows


def fit_full_rf_and_rank_features(
    X: List[List[float]],
    y: List[int],
    feature_names: List[str],
    *,
    seed: int,
    rf_params: Dict[str, Any],
) -> Tuple[str, List[Tuple[str, float]]]:
    """RF를 전체 데이터로 재학습 후 feature_importances_로 랭킹."""
    try:
        from sklearn.ensemble import RandomForestClassifier
    except Exception:
        return "unsupported", []

    if not X or not feature_names:
        return "unsupported", []
    if len(X[0]) != len(feature_names):
        m = min(len(X[0]), len(feature_names))
        feature_names = feature_names[:m]
        X = [row[:m] for row in X]

    clf = RandomForestClassifier(
        n_estimators=int(rf_params.get("n_estimators", 200)),
        max_depth=rf_params.get("max_depth", None),
        min_samples_leaf=int(rf_params.get("min_samples_leaf", 1)),
        class_weight=rf_params.get("class_weight", "balanced_subsample"),
        random_state=seed,
        n_jobs=-1,
    )
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

def write_fixed_test_report_md(
    path: str,
    *,
    train_path: str,
    test_path: str,
    n_train_rows: int,
    n_train_usable: int,
    n_test_rows: int,
    n_test_usable: int,
    group_key: str,
    dropped_overlap: int,
    best_model: str,
    threshold: float,
    results: Dict[str, Any],
    details: List[Dict[str, Any]] | None = None
) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    lines: List[str] = []
    lines.append(f"# Fixed Test Evaluation Report\n\n")
    lines.append(f"- generated_at: {datetime.datetime.now().isoformat(timespec='seconds')}\n")
    lines.append(f"- train: {train_path}\n")
    lines.append(f"- test: {test_path}\n")
    lines.append(f"- train_rows: {n_train_rows} (usable={n_train_usable})\n")
    lines.append(f"- test_rows: {n_test_rows} (usable={n_test_usable})\n")
    lines.append(f"- group_key: {group_key}\n")
    if dropped_overlap:
        lines.append(f"- dropped_overlap_groups: {dropped_overlap}\n")
    lines.append("\n")

    lines.append("## Best Model\n\n")
    lines.append(f"- best: {best_model}\n")
    lines.append(f"- threshold: {threshold:.2f}\n\n")

    lines.append("## Metrics\n\n")
    m = results["metrics"]
    cm = results["cm"]
    lines.append(f"- acc: {m['acc']:.4f}\n")
    lines.append(f"- bal_acc: {m['bal_acc']:.4f}\n")
    lines.append(f"- f1_1: {m['f1_1']:.4f}\n")
    lines.append(f"- recall_1: {m['recall_1']:.4f}\n")
    lines.append(f"- precision_1: {m['precision_1']:.4f}\n")
    lines.append(f"- cm: {_fmt_cm(cm)}\n\n")

    lines.append("## Confusion Matrix\n\n")
    lines.append("| | pred=0 | pred=1 |\n")
    lines.append("|---|---:|---:|\n")
    lines.append(f"| true=0 | {cm[0][0]} | {cm[0][1]} |\n")
    lines.append(f"| true=1 | {cm[1][0]} | {cm[1][1]} |\n")

    if details:
        lines.append("\n## Per-scenario predictions\n\n")
        lines.append("| idx | title | pair_key | type | n | dist | y | pred | p1 | ok |\n")
        lines.append("|---:|---|---|---|---:|---:|---:|---:|---:|:--:|\n")
        for i, d in enumerate(details, start=1):
            title = str(d.get("scenario_title","")).replace("|","/")
            pair_key = str(d.get("pair_key","")).replace("|","/")
            et = d.get("encounter_type","")
            n = d.get("defender_count","")
            dist = d.get("start_distance","")
            y = d.get("y_true","")
            pred = d.get("y_pred","")
            p1 = d.get("proba_1", None)
            p1s = "" if p1 is None else f"{p1:.4f}"
            ok = "✅" if d.get("ok") else "❌"
            lines.append(f"| {i} | {title} | {pair_key} | {et} | {n} | {dist} | {y} | {pred} | {p1s} | {ok} |\n")

        wrong = [d for d in details if not d.get("ok")]
        lines.append("\n## Errors only\n\n")
        if not wrong:
            lines.append("- (none)\n")
        else:
            for d in wrong:
                lines.append(f"- {d.get('scenario_title')} / pair={d.get('pair_key')} y={d.get('y_true')} pred={d.get('y_pred')} p1={d.get('proba_1')}\n")

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
    p = argparse.ArgumentParser(allow_abbrev=False)
    p.add_argument("--input", default="datasets/battle_dataset_v1.csv")
    p.add_argument("--train", default="", help="학습(train) CSV 경로. 지정 시 --input 대신 사용")
    p.add_argument("--test", default="", help="고정 테스트(test) CSV 경로. 지정 시 train 전체로 학습 후 test 평가를 추가로 수행")
    p.add_argument("--report-test", default="", help="고정 테스트 평가 리포트 저장 경로")
    p.add_argument("--drop-overlap-groups", action="store_true",
                   help="train/test 간 group_key가 겹치는 test row 제거(누수 방지)")
    p.add_argument("--k", type=int, default=10, help="반복 split 횟수 K (default=10)")
    p.add_argument("--test-ratio", type=float, default=0.2)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--report", default="", help="md 리포트 저장 경로(비우면 reports/baseline_eval_YYYYMMDD.md)")
    p.add_argument("--group", action="store_true", help="GroupShuffleSplit로 (attacker,defender) 조합 단위 분할")
    p.add_argument("--group-key", default="pair_key", help="그룹 분할에 사용할 CSV 컬럼명 (default: pair_key)")
    p.add_argument("--group-stratified", action="store_true", 
                   help="그룹 단위로 split하되(조합 분리), 그룹 라벨(다수결) 기준으로 stratified sampling 적용")
    p.add_argument("--tune-threshold", action="store_true", help="best 모델에 대해 threshold sweep으로 F1_1 최대 threshold 찾기")
    p.add_argument("--thr-step", type=float, default=0.05, help="threshold sweep step (default=0.05)")

    p.add_argument("--rf-grid", action="store_true",
                   help="RF 미니 그리드 탐색(max_depth/min_samples_leaf) + threshold 재튜닝(=F1 최대)")
    p.add_argument("--rf-depths", default="None,8,12",
                   help="RF max_depth 후보(콤마). 예: None,8,12")
    p.add_argument("--rf-min-leaves", default="1,2,4",
                   help="RF min_samples_leaf 후보(콤마). 예: 1,2,4")
    p.add_argument("--rf-estimators", type=int, default=200,
                   help="RF n_estimators (default=200)")
    p.add_argument("--rf-topn", type=int, default=8,
                   help="리포트에 남길 RF grid 상위 N개 (default=8)")

    args = p.parse_args()

    train_path = (args.train.strip() if isinstance(args.train, str) else "") or args.input
    rows = load_csv(args.input)
    PERK_IDS = detect_perk_ids(rows)
    rebuild_feature_schema()
    # ===== perk 컬럼 자동 감지 + FEATURE_NAMES 확장 =====
    global FEATURE_NAMES, NUM_KEYS

    header_keys = list(rows[0].keys()) if rows else []
    perk_ids = []
    for k in header_keys:
        if k.startswith("a_has_perk_"):
            perk_ids.append(k[len("a_has_perk_"):])
    PERK_IDS = sorted(set(perk_ids))

    extra_feature_names = [
        "encounter_is_swarm", "defender_count","start_distance",
        "a_perk_count", "d_perk_count", "perk_count_adv"]
    for pid in PERK_IDS:
        extra_feature_names += [
            f"a_has_perk_{pid}", f"d_has_perk_{pid}", f"perk_adv_{pid}"
        ]

    FEATURE_NAMES = list(BASE_FEATURE_NAMES) + extra_feature_names
    # NUM_KEYS는 기존 BASE_NUM_KEYS 그대로 둬도 되고,
    # 필요하면 perk_count를 여기에도 포함 가능(현재 build_features가 직접 읽어서 필수는 아님)
    NUM_KEYS = list(BASE_NUM_KEYS)

    data: List[Tuple[List[float], int]] = []
    groups: List[str] = []
    for idx, row in enumerate(rows):
        item = build_features(row)
        if item is None:
            continue

        # group key 수집(없으면 a_name/d_name으로 fallback)
        g = row.get(args.group_key)
        if not isinstance(g, str) or not g.strip():
            a = row.get("a_name")
            d = row.get("d_name")
            if isinstance(a, str) and isinstance(d, str) and a.strip() and d.strip():
                g = f"{a.strip()}__vs__{d.strip()}"
            else:
                # 마지막 fallback: 행 단위(그룹 분할 의미는 약해지지만 크래시 방지)
                g = f"row_{idx}"

        data.append(item)
        groups.append(g)

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
    K = int(args.k)

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

    # ===== split 계획 수립 =====
    split_mode = "random"
    n_groups = 0
    split_plan = None

    if args.group:
        try:
            from sklearn.model_selection import GroupShuffleSplit
        except Exception:
            print("[WARN] sklearn not available. fallback to random split.")
            args.group = False
        else:
            split_mode = "group"
            n_groups = len(set(groups))
            print(f"[INFO] split mode: GROUP key={args.group_key} groups={n_groups}")

            X_all = [x for x, _ in data]
            y_all = [y for _, y in data]

            if args.group_stratified:
                # ---- 그룹 단위 + 라벨 비율 완화(그룹 라벨 다수결로 stratify) ----
                from sklearn.model_selection import StratifiedShuffleSplit

                # group -> indices
                group_to_indices: Dict[str, List[int]] = {}
                for idx, g in enumerate(groups):
                    group_to_indices.setdefault(g, []).append(idx)

                uniq_groups = list(group_to_indices.keys())

                # 그룹 라벨: 그룹 내 y 다수결(동률이면 1)
                group_labels: List[int] = []
                for g in uniq_groups:
                    ys_g = [y_all[i] for i in group_to_indices[g]]
                    ones = sum(ys_g)
                    zeros = len(ys_g) - ones
                    group_labels.append(1 if ones >= zeros else 0)

                sss = StratifiedShuffleSplit(
                    n_splits=K, test_size=args.test_ratio, random_state=args.seed
                )

                split_plan = []
                for train_g_idx, test_g_idx in sss.split(uniq_groups, group_labels):
                    train_groups = [uniq_groups[i] for i in train_g_idx]
                    test_groups = [uniq_groups[i] for i in test_g_idx]

                    train_idx = [i for g in train_groups for i in group_to_indices[g]]
                    test_idx = [i for g in test_groups for i in group_to_indices[g]]
                    split_plan.append((train_idx, test_idx))

                print("[INFO] group-stratified: enabled")
            else:
                gss = GroupShuffleSplit(n_splits=K, test_size=args.test_ratio, random_state=args.seed)
                split_plan = list(gss.split(X_all, y_all, groups))


    if split_mode == "random":
        print(f"[INFO] split mode: RANDOM seed_base={args.seed} test_ratio={args.test_ratio}")

    test_pos_rates: List[float] = []

    for i in range(K):
        split_seed = args.seed + i

        if split_mode == "group" and split_plan is not None:
            train_idx, test_idx = split_plan[i]
            train = [data[j] for j in train_idx]
            test = [data[j] for j in test_idx]
        else:
            train, test = split_xy(data, test_ratio=args.test_ratio, seed=split_seed)

        X_test = [x for x, _ in test]
        y_test = [y for _, y in test]

        # test 라벨(1) 비율 기록(분포 흔들림 체크)
        if len(y_test) > 0:
            test_pos_rates.append(sum(y_test) / len(y_test))

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

    if test_pos_rates:
        s = _summ(test_pos_rates)
        print("[INFO] test_pos_rate (label=1) / SPLIT")
        print(f"- mean={_fmt3(s['mean'])} min={_fmt3(s['min'])} max={_fmt3(s['max'])}")
        print()

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

    kind = "unsupported"
    ranked: List[Tuple[str, float]] = []

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

    # ===== Threshold 튜닝(확률 기반) =====
    tuned = None
    if args.tune_threshold and best:
        # predict_proba 지원 모델만
        if best in ("LR", "LR_balanced", "DT_balanced", "RF_balanced_subsample"):
            tuned = threshold_sweep_across_splits(
                model_name=best,
                data=data,
                split_mode=split_mode,
                split_plan=split_plan,
                K=K,
                seed_base=args.seed,
                test_ratio=args.test_ratio,
                thr_step=args.thr_step,
            )
            if tuned is None:
                print("[WARN] threshold tuning skipped (predict_proba not available).")
            else:
                thr, m, cm = tuned[0]
                print(f"[BEST THRESHOLD] model={best} thr={thr:.2f} f1_1={m['f1_1']:.4f} "
                      f"recall_1={m['recall_1']:.4f} prec_1={m['precision_1']:.4f} bal_acc={m['bal_acc']:.4f}")
                print(f"- cm_sum {_fmt_cm(cm)}")
        else:
            print("[INFO] threshold tuning not supported for this best model.")



    # ===== RF 미니 그리드 탐색 + threshold 재튜닝(선택) =====
    rf_grid_params: Dict[str, Any] | None = None
    rf_grid_best_row: Dict[str, Any] | None = None
    rf_grid_rows: List[Dict[str, Any]] | None = None

    if args.rf_grid:
        try:
            depths = _parse_max_depth_list_csv(args.rf_depths)
            leaves = _parse_int_list_csv(args.rf_min_leaves)
        except Exception as e:
            print(f"[WARN] rf-grid parse failed: {e}")
        else:
            rf_grid_params, rf_grid_best_tuned, rf_grid_rows = rf_grid_search_best_by_f1(
                data=data,
                split_mode=split_mode,
                split_plan=split_plan,
                K=K,
                seed_base=args.seed,
                test_ratio=args.test_ratio,
                thr_step=args.thr_step,
                n_estimators=args.rf_estimators,
                depths=depths,
                min_leaves=leaves,
                class_weight="balanced_subsample",
            )

            if rf_grid_rows:
                rf_grid_best_row = rf_grid_rows[0]
                print("[RF GRID]")
                print(f"- tried: {len(rf_grid_rows)} configs")
                print(f"- best_params: n_estimators={rf_grid_best_row['n_estimators']} "
                      f"max_depth={rf_grid_best_row['max_depth']} "
                      f"min_samples_leaf={rf_grid_best_row['min_samples_leaf']}")
                print(f"- best_threshold: {rf_grid_best_row['thr']:.2f} "
                      f"f1_1={rf_grid_best_row['f1_1']:.4f} "
                      f"recall_1={rf_grid_best_row['recall_1']:.4f} "
                      f"prec_1={rf_grid_best_row['precision_1']:.4f} "
                      f"bal_acc={rf_grid_best_row['bal_acc']:.4f}")
                print(f"- cm_sum {_fmt_cm(rf_grid_best_row['cm_sum'])}")

                # 기존 기준(best/tuned) 대비 개선되면 best/tuned/feature ranking을 갱신
                ref_f1 = -1.0
                if tuned and isinstance(tuned, list) and tuned:
                    ref_f1 = float(tuned[0][1].get("f1_1", -1.0))
                elif best and best in packed:
                    ref_f1 = float(packed[best]["f1_1"]["mean"])

                if rf_grid_best_row["f1_1"] > ref_f1:
                    best = "RF_balanced_subsample"
                    tuned = rf_grid_best_tuned  # threshold ranking (Top5 출력/리포트용)

                    # 전체 데이터로 RF(선택된 파라미터) 재학습 후 feature 랭킹 갱신
                    X_all2 = [x for x, _ in data]
                    y_all2 = [yy for _, yy in data]
                    if rf_grid_params:
                        kind, ranked = fit_full_rf_and_rank_features(
                            X_all2,
                            y_all2,
                            FEATURE_NAMES,
                            seed=args.seed,
                            rf_params=rf_grid_params,
                        )
                        if ranked:
                            print(f"[TOP FEATURES] (tree_importance) top 12 (RF tuned)")
                            for name, score in ranked[:12]:
                                print(f"- {name}: {score:.6f}")
            else:
                print("[WARN] RF grid search produced no results (sklearn missing?).")

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
            f.write("\n## Split Mode\n\n")
            f.write(f"- mode: {split_mode}\n")
            if split_mode == "group":
                f.write(f"- group_key: {args.group_key}\n")
                f.write(f"- n_groups: {n_groups}\n")
            f.write("\n")

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

            f.write("\n## Threshold Tuning\n\n")
            if tuned:
                thr, m, cm = tuned[0]
                f.write(f"- model: {best}\n")
                f.write(f"- best_threshold: {thr:.2f}\n")
                f.write(f"- f1_1: {m['f1_1']:.4f}\n")
                f.write(f"- recall_1: {m['recall_1']:.4f}\n")
                f.write(f"- precision_1: {m['precision_1']:.4f}\n")
                f.write(f"- bal_acc: {m['bal_acc']:.4f}\n")
                f.write(f"- cm_sum: {_fmt_cm(cm)}\n\n")

                f.write("Top 5 thresholds by f1_1:\n\n")
                f.write("| rank | thr | f1_1 | recall_1 | precision_1 | bal_acc |\n|---:|---:|---:|---:|---:|---:|\n")
                for i, (t, mm, _) in enumerate(tuned[:5], start=1):
                    f.write(f"| {i} | {t:.2f} | {mm['f1_1']:.4f} | {mm['recall_1']:.4f} | {mm['precision_1']:.4f} | {mm['bal_acc']:.4f} |\n")
            else:
                f.write("- (not run)\n")

            f.write("\n## RF Grid Search\n\n")
            if rf_grid_rows:
                f.write(f"- tried_configs: {len(rf_grid_rows)}\n")
                if rf_grid_params:
                    f.write(
                        f"- best_params: n_estimators={rf_grid_params.get('n_estimators')} "
                        f"max_depth={rf_grid_params.get('max_depth')} "
                        f"min_samples_leaf={rf_grid_params.get('min_samples_leaf')} "
                        f"class_weight={rf_grid_params.get('class_weight')}\n"
                    )
                if rf_grid_best_row:
                    f.write(
                        f"- best_threshold: {rf_grid_best_row['thr']:.2f} "
                        f"f1_1={rf_grid_best_row['f1_1']:.4f} "
                        f"recall_1={rf_grid_best_row['recall_1']:.4f} "
                        f"precision_1={rf_grid_best_row['precision_1']:.4f} "
                        f"bal_acc={rf_grid_best_row['bal_acc']:.4f} "
                        f"acc={rf_grid_best_row['acc']:.4f}\n"
                    )
                    f.write(f"- cm_sum: {_fmt_cm(rf_grid_best_row['cm_sum'])}\n\n")

                f.write("| rank | max_depth | min_samples_leaf | thr | f1_1 | recall_1 | precision_1 | bal_acc | acc |\n")
                f.write("|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n")
                topn = max(1, int(args.rf_topn))
                for i, row in enumerate(rf_grid_rows[:topn], start=1):
                    md = "None" if row["max_depth"] is None else str(row["max_depth"])
                    f.write(
                        f"| {i} | {md} | {row['min_samples_leaf']} | {row['thr']:.2f} | "
                        f"{row['f1_1']:.4f} | {row['recall_1']:.4f} | {row['precision_1']:.4f} | "
                        f"{row['bal_acc']:.4f} | {row['acc']:.4f} |\n"
                    )
            else:
                f.write("- (not run)\n")

                
        print("[OK] appended best/top-features to report.")
    except Exception as e:
        print(f"[WARN] failed to append report: {e}")


    print(f"[OK] wrote report: {report_path}")

    # ===== Fixed Test Evaluation (optional) =====
    if isinstance(args.test, str) and args.test.strip():
        test_path = args.test.strip()
        test_rows = load_csv(test_path)

        test_data: List[Tuple[List[float], int]] = []
        test_groups: List[str] = []
        test_rows_kept: List[Dict[str, Any]] = []

        for idx, row in enumerate(test_rows):
            item = build_features(row)
            if item is None:
                continue

            g = row.get(args.group_key)
            if not isinstance(g, str) or not g.strip():
                a = row.get("a_name")
                d = row.get("d_name")
                if isinstance(a, str) and isinstance(d, str) and a.strip() and d.strip():
                    g = f"{a.strip()}__vs__{d.strip()}"
                else:
                    g = f"row_{idx}"

            test_data.append(item)
            test_groups.append(g)
            test_rows_kept.append(row)

        dropped = 0
        if args.drop_overlap_groups and args.group:
            train_group_set = set(groups)
            keep_idx = [i for i, g in enumerate(test_groups) if g not in train_group_set]
            dropped = len(test_groups) - len(keep_idx)
            if dropped > 0:
                test_data = [test_data[i] for i in keep_idx]
                test_groups = [test_groups[i] for i in keep_idx]
                test_rows_kept = [test_rows_kept[i] for i in keep_idx]

        print(f"[INFO] fixed test: {test_path}")
        print(f"[INFO] test rows: {len(test_rows)}")
        print(f"[INFO] usable test rows: {len(test_data)}")
        if dropped:
            print(f"[INFO] dropped overlap groups: {dropped}")

        if len(test_data) == 0:
            print("[WARN] fixed test usable rows is 0 (after filtering). skip fixed test eval.")
        elif not best:
            print("[WARN] best model is empty. skip fixed test eval.")
        else:
            # threshold 우선순위: 튠 결과(tuned) -> rf_grid_best_row -> default(0.5)
            thr = 0.5
            if tuned and isinstance(tuned, list) and tuned:
                try:
                    thr = float(tuned[0][0])
                except Exception:
                    thr = 0.5
            elif rf_grid_best_row and isinstance(rf_grid_best_row, dict) and "thr" in rf_grid_best_row:
                try:
                    thr = float(rf_grid_best_row["thr"])
                except Exception:
                    thr = 0.5

            y_true = [y for _, y in test_data]
            preds: Optional[List[int]] = None

            if best.startswith("MAJORITY"):
                maj = 1 if ys.count(1) > ys.count(0) else 0
                preds = [maj] * len(test_data)
                thr = 0.5
            else:
                # proba 기반 threshold가 가능하면 사용
                probas = fit_predict_proba_model(data, test_data, best, seed=args.seed)
                if probas is not None:
                    preds = [1 if p >= thr else 0 for p in probas]
                else:
                    # fallback (함수들은 기존 파일에 이미 있어야 함)
                    if best == "LR":
                        preds = fit_predict_lr(data, test_data, class_weight=None, seed=args.seed)
                    elif best == "LR_balanced":
                        preds = fit_predict_lr(data, test_data, class_weight="balanced", seed=args.seed)
                    elif best == "DT_balanced":
                        preds = fit_predict_tree(data, test_data, model="dt", class_weight="balanced", seed=args.seed)
                    elif best == "RF_balanced_subsample":
                        preds = fit_predict_tree(data, test_data, model="rf", class_weight="balanced_subsample", seed=args.seed)

            if preds is None:
                print("[WARN] fixed test eval skipped (sklearn missing?).")
            else:
                details: List[Dict[str, Any]] = []
                for i, row in enumerate(test_rows_kept):
                    details.append({
                        "scenario_title": row.get("scenario_title", ""),
                        "pair_key": row.get("pair_key", ""),
                        "encounter_type": row.get("encounter_type", ""),
                        "defender_count": row.get("defender_count", ""),
                        "start_distance": row.get("start_distance", ""),
                        "y_true": y_true[i],
                        "y_pred": preds[i],
                        "proba_1": (round(probas[i], 4) if probas is not None else None),
                        "ok": (y_true[i] == preds[i]),
                    })
                
                cm = _cm_from_preds(y_true, preds)
                m = _metrics_from_cm(cm)

                print("[FIXED_TEST]")
                print(f"- model   : {best}")
                print(f"- thr     : {thr:.2f}")
                print(f"- acc     : {m['acc']:.4f}")
                print(f"- bal_acc : {m['bal_acc']:.4f}")
                print(f"- f1_1    : {m['f1_1']:.4f}")
                print(f"- recall_1: {m['recall_1']:.4f}")
                print(f"- prec_1  : {m['precision_1']:.4f}")
                print(f"- cm      : {_fmt_cm(cm)}")

                report_test_path = (
                    args.report_test.strip()
                    if isinstance(args.report_test, str) and args.report_test.strip()
                    else report_path.replace(".md", "_fixedtest.md")
                )

                write_fixed_test_report_md(
                    report_test_path,
                    train_path=train_path,
                    test_path=test_path,
                    n_train_rows=len(rows),
                    n_train_usable=len(data),
                    n_test_rows=len(test_rows),
                    n_test_usable=len(test_data),
                    group_key=args.group_key,
                    dropped_overlap=dropped,
                    best_model=best,
                    threshold=thr,
                    results={"metrics": m, "cm": cm},
                    details=details,
                )
                print(f"[OK] wrote fixed-test report: {report_test_path}")

    
if __name__ == "__main__":
    main()