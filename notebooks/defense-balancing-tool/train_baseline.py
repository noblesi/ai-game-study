from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    confusion_matrix,
    precision_recall_fscore_support,
    roc_auc_score,
)
from sklearn.model_selection import GroupShuffleSplit, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier


def today_yyyymmdd() -> str:
    return dt.datetime.now().strftime("%Y%m%d")


def resolve_label_col(cols: Sequence[str]) -> str:
    for c in [
        "label", "y", "target", "defender_win", "win", "outcome",
        "label_attacker_better", "label_defender_better",
    ]:
        if c in cols:
            return c
    raise ValueError(f"[train_baseline] label column not found. cols={list(cols)[:30]}...")


def resolve_group_col(cols: Sequence[str], want: str) -> str:
    if want in cols:
        return want
    for c in ["pair_key", "group", "matchup_key"]:
        if c in cols:
            return c
    raise ValueError(f"[train_baseline] group column '{want}' not found. cols={list(cols)[:30]}...")


def select_feature_cols(df: pd.DataFrame, label_col: str, group_col: Optional[str],
                        drop_adv: bool, drop_perk: bool) -> List[str]:
    drop = {label_col}
    if group_col:
        drop.add(group_col)

    drop |= {
        "kind","scenario_id","seed","trial","run_id","run_id_short","logged_at","schema_version",
        "engine","spec_source","scenario_title","scenario_source","pair_key_full",
        "attacker_id","defender_id","a_id","d_id","a_name","d_name","encounter_type",
        "record_trials", "trial_index", "trial_outcome", "attacker_pos", "defender_pos"
    }

    result_cols = {
        "trials","wins_attacker","wins_defender","draws","no_result",
        "attacker_win_rate","defender_win_rate","draw_rate","no_result_rate","avg_time",
    }

    feats: List[str] = []
    for c in df.columns:
        if c in drop:
            continue
        if c in result_cols:
            continue

        lc = c.lower()

        # ✅ "label_"로 시작하는 컬럼은 전부 누수 후보 → feature 제외
        # (우리 타겟 컬럼(label_col)만 예외지만, label_col은 이미 drop에 들어가 있어서 여기 안 걸림)
        if lc.startswith("label_"):
            continue

        # (추가 안전장치) 이름에 target/outcome/result가 들어가면 제외
        if any(k in lc for k in ("target", "outcome", "result")):
            continue

        # (특정 누수 컬럼 명시 제거)
        if lc == "label_attacker_better":
            continue

        # (선택) adv/dps/ttk/est 같은 “판정성 강한” 파생 피처 제거
        if drop_adv and (("_adv" in lc) or ("dps" in lc) or ("ttk" in lc) or ("_est" in lc)):
            continue

        # (선택) 퍼크 관련 피처 전체 제거
        if drop_perk and (("has_perk" in lc) or ("perk_" in lc)):
            continue

        if lc.startswith("wins_"):
            continue
        if lc.endswith("_rate"):
            continue
        if lc in ("avg_time", "trials"):
            continue

        if pd.api.types.is_numeric_dtype(df[c]):
            feats.append(c)

    if not feats:
        raise ValueError("[train_baseline] numeric feature columns not found after filtering")

    return feats

def rate(y: np.ndarray) -> float:
    return float(np.mean(y)) if len(y) else float("nan")

@dataclass
class SplitResult:
    train_idx: np.ndarray
    val_idx: np.ndarray
    test_idx: np.ndarray
    test_pos_rate: float
    test_groups: Optional[np.ndarray] = None


def group_split_once(
    n: int,
    groups: np.ndarray,
    seed: int,
    test_ratio: float,
    val_ratio: float,
    fixed_test_groups: Optional[Sequence[str]] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    idx_all = np.arange(n)

    if fixed_test_groups is None:
        gss = GroupShuffleSplit(n_splits=1, test_size=test_ratio, random_state=seed)
        tr_idx, te_idx = next(gss.split(idx_all, groups=groups))
        test_groups = np.unique(groups[te_idx])
    else:
        fixed = np.array(list(fixed_test_groups))
        te_mask = np.isin(groups, fixed)
        te_idx = idx_all[te_mask]
        tr_idx = idx_all[~te_mask]
        test_groups = np.unique(groups[te_idx])

    # val은 train 내부에서 다시 group split
    denom = max(1e-9, 1.0 - test_ratio)
    val_size_rel = min(0.9, max(0.01, val_ratio / denom))

    gss2 = GroupShuffleSplit(n_splits=1, test_size=val_size_rel, random_state=seed + 1)
    tr2_sub, va_sub = next(gss2.split(tr_idx, groups=groups[tr_idx]))
    tr2_idx = tr_idx[tr2_sub]
    va_idx = tr_idx[va_sub]
    return tr2_idx, va_idx, te_idx, test_groups


def pick_group_split_stratified(
    y: np.ndarray,
    groups: np.ndarray,
    seed: int,
    test_ratio: float,
    val_ratio: float,
    tries: int = 200,
    fixed_test_groups: Optional[Sequence[str]] = None,
) -> SplitResult:
    overall = rate(y)

    if fixed_test_groups is not None:
        tr, va, te, tg = group_split_once(len(y), groups, seed, test_ratio, val_ratio, fixed_test_groups)
        return SplitResult(tr, va, te, test_pos_rate=rate(y[te]), test_groups=tg)

    rng = np.random.RandomState(seed)
    best: Optional[SplitResult] = None
    best_score = float("inf")

    for _ in range(max(1, tries)):
        s = int(rng.randint(0, 2**31 - 1))
        tr, va, te, tg = group_split_once(len(y), groups, s, test_ratio, val_ratio, None)
        tpr = rate(y[te])
        score = abs(tpr - overall)  # test_pos_rate가 전체와 비슷한 split 선호

        best_tg_len = 0 if (best is None or best.test_groups is None) else len(best.test_groups)
        if (score < best_score - 1e-12) or (
            abs(score - best_score) <= 1e-12 and len(tg) > best_tg_len
        ):
            best_score = score
            best = SplitResult(tr, va, te, test_pos_rate=tpr, test_groups=tg)

    assert best is not None
    return best


def random_split_stratified(y: np.ndarray, seed: int, test_ratio: float, val_ratio: float) -> SplitResult:
    idx = np.arange(len(y))
    tr_idx, te_idx = train_test_split(idx, test_size=test_ratio, random_state=seed, stratify=y)

    denom = max(1e-9, 1.0 - test_ratio)
    val_size_rel = min(0.9, max(0.01, val_ratio / denom))
    tr2_idx, va_idx = train_test_split(tr_idx, test_size=val_size_rel, random_state=seed + 1, stratify=y[tr_idx])
    return SplitResult(tr2_idx, va_idx, te_idx, test_pos_rate=rate(y[te_idx]), test_groups=None)


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_score: Optional[np.ndarray] = None) -> Dict[str, float]:
    acc = float(accuracy_score(y_true, y_pred))
    bal_acc = float(balanced_accuracy_score(y_true, y_pred))
    prec, rec, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, pos_label=1, average="binary", zero_division=0
    )

    out: Dict[str, float] = {
        "acc": acc,
        "bal_acc": bal_acc,
        "prec_1": float(prec),
        "recall_1": float(rec),
        "f1_1": float(f1),
    }

    if y_score is not None:
        try:
            out["ap"] = float(average_precision_score(y_true, y_score))
        except Exception:
            out["ap"] = float("nan")
        try:
            out["roc_auc"] = float(roc_auc_score(y_true, y_score))
        except Exception:
            out["roc_auc"] = float("nan")

    return out

def metric_value(m: dict, metric: str) -> float:
    """
    threshold 튜닝/후보선정에 사용할 스칼라 점수 반환.
    args.threshold_metric 값(f1/recall/precision/bal_acc)과
    compute_metrics()의 키(f1_1/recall_1/prec_1/bal_acc)를 매핑한다.
    """
    metric = (metric or "").strip().lower()

    if metric == "f1":
        return float(m.get("f1_1", float("nan")))
    if metric == "recall":
        return float(m.get("recall_1", float("nan")))
    if metric == "precision":
        # compute_metrics가 "prec_1"로 두는 경우가 많음
        if "prec_1" in m:
            return float(m.get("prec_1", float("nan")))
        return float(m.get("precision_1", float("nan")))
    if metric == "bal_acc":
        return float(m.get("bal_acc", float("nan")))

    raise ValueError(f"Unknown metric: {metric}")


def tune_threshold(y_true, y_score, metric, thr_min: float, thr_max: float, thr_steps: int):
    thresholds = np.linspace(thr_min, thr_max, thr_steps)

    best_thr = 0.5
    best_key = -1.0
    best_detail: Dict[str, float] = {"recall_1": -1.0, "prec_1": -1.0}

    for thr in thresholds:
        y_pred = (y_score >= thr).astype(int)
        m = compute_metrics(y_true, y_pred, y_score=y_score)

        key = {
            "f1": m["f1_1"],
            "recall": m["recall_1"],
            "precision": m["prec_1"],
            "bal_acc": m["bal_acc"],
        }[metric]

        # tie-break: recall -> precision
        if (key > best_key + 1e-12) or (
            abs(key - best_key) <= 1e-12 and (m["recall_1"], m["prec_1"]) > (best_detail["recall_1"], best_detail["prec_1"])
        ):
            best_key = key
            best_thr = float(thr)
            best_detail = m

    best_detail = dict(best_detail)
    best_detail["thr"] = best_thr
    best_detail["thr_metric"] = best_key
    return best_thr, best_detail


def summarize(vals: List[float]) -> Dict[str, float]:
    arr = np.array(vals, dtype=float)
    return {
        "mean": float(np.nanmean(arr)),
        "min": float(np.nanmin(arr)),
        "max": float(np.nanmax(arr)),
    }


def fmt_stats(name: str, s: Dict[str, float]) -> str:
    return f"- {name:<9} mean={s['mean']:.4f} min={s['min']:.4f} max={s['max']:.4f}"


def parse_class_weight(s: str):
    s = s.strip().lower()
    if s == "none":
        return None
    if s == "balanced":
        return "balanced"
    # "0:1,1:3" 형태
    out = {}
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        k, v = part.split(":")
        out[int(k.strip())] = float(v.strip())
    return out

def resolve_or_make_label(
    df: pd.DataFrame,
    label_col_arg: str,
    drop_ties: bool,
    prefer_existing: bool = True,
) -> Tuple[pd.DataFrame, str]:
    """
    1) label_col_arg가 있으면 그 컬럼 사용
    2) prefer_existing=True면 resolve_label_col()로 기존 라벨 찾기
    3) 없으면 wins_* 또는 *_win_rate로 _label 파생
    """
    label_col = (label_col_arg or "").strip()

    if label_col:
        if label_col not in df.columns:
            raise ValueError(f"[train_baseline] --label_col='{label_col}' not found in csv columns")
        return df, label_col

    if prefer_existing:
        try:
            return df, resolve_label_col(df.columns)  # 네 파일에 이미 있는 함수
        except ValueError:
            pass

    # derive label
    if ("wins_defender" in df.columns) and ("wins_attacker" in df.columns):
        d = df
        if drop_ties:
            d = d[d["wins_defender"] != d["wins_attacker"]].copy()
        d["_label"] = (d["wins_defender"] > d["wins_attacker"]).astype(int)
        return d, "_label"

    if ("defender_win_rate" in df.columns) and ("attacker_win_rate" in df.columns):
        d = df
        if drop_ties:
            d = d[np.abs(d["defender_win_rate"] - d["attacker_win_rate"]) > 1e-12].copy()
        d["_label"] = (d["defender_win_rate"] > d["attacker_win_rate"]).astype(int)
        return d, "_label"

    raise ValueError(
        "[train_baseline] label column not found, and cannot derive label. "
        "Need (wins_defender & wins_attacker) or (defender_win_rate & attacker_win_rate)."
    )


def pick_common_label_col(train_cols: Sequence[str], test_cols: Sequence[str]) -> Optional[str]:
    """train/test에 공통으로 존재하는 label 후보를 우선순위대로 선택"""
    for c in [
        "label", "y", "target", "defender_win", "win", "outcome",
        "label_attacker_better", "label_defender_better",
    ]:
        if (c in train_cols) and (c in test_cols):
            return c
    return None


def build_estimator(
    kind: str,
    seed: int,
    class_weight,
    logreg_C: float,
    logreg_max_iter: int,
    logreg_solver: str,
    rf_params: Optional[Dict[str, object]] = None,
) -> Pipeline:
    """logreg / rf 지원 (저장/로딩 일관성을 위해 Pipeline으로 감쌈)"""
    if kind == "logreg":
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "clf",
                    LogisticRegression(
                        C=logreg_C,
                        class_weight=class_weight,
                        max_iter=logreg_max_iter,
                        solver=logreg_solver,
                    ),
                ),
            ]
        )

    if kind == "rf":
        params = dict(rf_params or {})
        params.setdefault("n_estimators", 600)
        params.setdefault("max_depth", None)
        params.setdefault("min_samples_split", 2)
        params.setdefault("min_samples_leaf", 1)
        params.setdefault("max_features", "sqrt")
        params.setdefault("n_jobs", -1)
        params.setdefault("random_state", seed)

        return Pipeline(
            [
                ("clf", RandomForestClassifier(class_weight=class_weight, **params)),
            ]
        )

    raise ValueError(f"unknown model kind: {kind}")


def rf_grid_candidates() -> List[Dict[str, object]]:
    """프로젝트용 작은 RF grid (너무 커지면 파이프라인이 느려짐)"""
    grid: List[Dict[str, object]] = []
    for n_estimators in [400, 800]:
        for max_depth in [None, 10, 16]:
            for min_split in [2, 10]:
                grid.append(
                    {
                        "n_estimators": n_estimators,
                        "max_depth": max_depth,
                        "min_samples_split": min_split,
                        "min_samples_leaf": 1,
                        "max_features": "sqrt",
                    }
                )
    return grid


def pick_group_val_split_stratified(
    y: np.ndarray,
    groups: np.ndarray,
    seed: int,
    val_ratio: float,
    tries: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """train 내부에서만 group split으로 (train_idx, val_idx) 생성 + val pos_rate를 전체와 비슷하게 맞춤"""
    idx_all = np.arange(len(y))
    overall = float(np.mean(y)) if len(y) else float("nan")

    rng = np.random.RandomState(seed)
    best_tr: Optional[np.ndarray] = None
    best_va: Optional[np.ndarray] = None
    best_score = float("inf")

    for _ in range(max(1, tries)):
        s = int(rng.randint(0, 2**31 - 1))
        gss = GroupShuffleSplit(n_splits=1, test_size=val_ratio, random_state=s)
        tr, va = next(gss.split(idx_all, groups=groups))
        score = abs(float(np.mean(y[va])) - overall)
        if score < best_score - 1e-12:
            best_score = score
            best_tr, best_va = tr, va

    assert best_tr is not None and best_va is not None
    return best_tr, best_va


def pick_random_val_split_stratified(y: np.ndarray, seed: int, val_ratio: float) -> Tuple[np.ndarray, np.ndarray]:
    idx = np.arange(len(y))
    tr, va = train_test_split(idx, test_size=val_ratio, random_state=seed, stratify=y)
    return tr, va


def select_best_candidate_on_val(
    X_tr: np.ndarray,
    y_tr: np.ndarray,
    X_va: np.ndarray,
    y_va: np.ndarray,
    seed: int,
    model_kind: str,
    candidates: List[Dict[str, object]],
    class_weight,
    logreg_C: float,
    logreg_max_iter: int,
    logreg_solver: str,
    tune_thr: bool,
    thr_metric: str,
    thr_min: float,
    thr_max: float,
    thr_steps: int,
    fixed_thr: Optional[float],
) -> Tuple[Dict[str, object], float, Dict[str, float]]:
    """
    후보 파라미터들을 val에서 평가해서 best를 선택하고,
    (옵션) threshold도 val 기준으로 함께 선택한다.
    """
    best_params: Dict[str, object] = {}
    best_thr = 0.5
    best_m: Dict[str, float] = {"f1_1": -1.0, "recall_1": -1.0, "prec_1": -1.0, "bal_acc": -1.0}
    best_key = -1.0

    for params in candidates:
        est = build_estimator(
            kind=model_kind,
            seed=seed,
            class_weight=class_weight,
            logreg_C=logreg_C,
            logreg_max_iter=logreg_max_iter,
            logreg_solver=logreg_solver,
            rf_params=params if model_kind == "rf" else None,
        )
        est.fit(X_tr, y_tr)
        va_score = est.predict_proba(X_va)[:, 1]

        thr = 0.5
        if fixed_thr is not None:
            thr = float(fixed_thr)
        elif tune_thr:
            thr, _ = tune_threshold(  # 네 파일에 이미 있는 함수
                y_va,
                va_score,
                metric=thr_metric,
                thr_min=thr_min,
                thr_max=thr_max,
                thr_steps=thr_steps,
            )

        y_va_pred = (va_score >= thr).astype(int)
        m = compute_metrics(y_va, y_va_pred, y_score=va_score)  # 네 파일에 이미 있는 함수
        key = metric_value(m, thr_metric)  # 네 파일에 이미 있는 함수

        # tie-break: recall -> precision
        if (key > best_key + 1e-12) or (
            abs(key - best_key) <= 1e-12 and (m["recall_1"], m["prec_1"]) > (best_m["recall_1"], best_m["prec_1"])
        ):
            best_key = float(key)
            best_params = dict(params)
            best_thr = float(thr)
            best_m = dict(m)

    return best_params, best_thr, best_m


@dataclass
class RepeatResult:
    test_metrics: Dict[str, float]
    val_metrics: Dict[str, float]
    chosen_thr: float
    model_kind: str
    model_params: Dict[str, object]


def run_train_test_mode(args) -> None:
    """
    --train / --test 모드:
    - test는 고정
    - train에서만 train/val split (repeats=k)
    - (옵션) rf-grid + threshold tuning
    - (옵션) overlap group 제거
    - 최종 모델 fit(full train) 후 저장(save-model/save-meta)
    """
    if not args.train_path or not args.test_path:
        raise ValueError("[train_baseline] train/test mode requires both --train and --test")

    train_df = pd.read_csv(args.train_path, low_memory=False)
    test_df = pd.read_csv(args.test_path, low_memory=False)

    # 1) label 결정 (train/test 공통 label 우선)
    label_arg = (args.label_col or "").strip()
    if label_arg:
        if label_arg not in train_df.columns or label_arg not in test_df.columns:
            raise ValueError(f"[train_baseline] --label_col='{label_arg}' must exist in both train/test CSVs")
        label_col = label_arg
    else:
        common = pick_common_label_col(train_df.columns, test_df.columns)
        if common:
            label_col = common
        else:
            train_df, label_col = resolve_or_make_label(train_df, "", drop_ties=args.drop_ties, prefer_existing=False)
            test_df, test_label = resolve_or_make_label(test_df, "", drop_ties=args.drop_ties, prefer_existing=False)
            if test_label != label_col:
                test_df[label_col] = test_df[test_label].astype(int)
                if test_label in test_df.columns and test_label != label_col:
                    test_df = test_df.drop(columns=[test_label])

    # 2) split mode / group
    split_mode = args.split_mode
    if args.group:
        split_mode = "group"
    if args.random:
        split_mode = "random"

    group_col: Optional[str] = None
    if split_mode == "group":
        group_col = resolve_group_col(train_df.columns, args.group_key)  # 네 파일에 이미 있는 함수
        if group_col not in test_df.columns:
            raise ValueError(f"[train_baseline] test CSV missing group key column: {group_col}")

    # 3) (옵션) overlap group 제거 (train only)
    dropped_overlap = 0
    overlap_groups: Optional[set[str]] = None
    if split_mode == "group" and getattr(args, "drop_overlap_groups", False):
        assert group_col is not None
        tr_groups = set(train_df[group_col].astype(str).tolist())
        te_groups = set(test_df[group_col].astype(str).tolist())
        overlap_groups = tr_groups & te_groups
        if overlap_groups:
            before = len(train_df)
            train_df = train_df[~train_df[group_col].astype(str).isin(overlap_groups)].copy()
            dropped_overlap = before - len(train_df)

    # 4) feature 선택 (train 기준 -> test와 교집합)
    feat_cols_train = select_feature_cols(
        train_df, label_col, group_col, args.drop_adv_features, args.drop_perk_features
    )  # 네 파일에 이미 있는 함수
    feat_cols = [c for c in feat_cols_train if (c in test_df.columns) and pd.api.types.is_numeric_dtype(test_df[c])]
    if not feat_cols:
        raise ValueError("[train_baseline] no common numeric feature columns between train/test")

    needed_train = feat_cols + [label_col] + ([group_col] if group_col else [])
    needed_test = feat_cols + [label_col] + ([group_col] if group_col else [])
    train_df = train_df.dropna(subset=needed_train).reset_index(drop=True)
    test_df = test_df.dropna(subset=needed_test).reset_index(drop=True)

    X_train_full = train_df[feat_cols].to_numpy(dtype=float)
    y_train_full = train_df[label_col].astype(int).to_numpy()
    X_test = test_df[feat_cols].to_numpy(dtype=float)
    y_test = test_df[label_col].astype(int).to_numpy()

    if args.shuffle_labels:
        rng = np.random.RandomState(args.shuffle_seed)
        y_train_full = rng.permutation(y_train_full)
        print(f"[SANITY] labels shuffled (seed={args.shuffle_seed})")

    groups_train = train_df[group_col].astype(str).to_numpy() if group_col else None

    # 5) model candidates
    cw = parse_class_weight(args.class_weight)  # 네 파일에 이미 있는 함수

    model_kind = "logreg"
    candidates: List[Dict[str, object]] = [{}]
    if getattr(args, "rf_grid", False):
        model_kind = "rf"
        candidates = rf_grid_candidates()

    repeats = int(args.k) if args.k is not None else int(args.repeats)
    repeats = max(1, repeats)

    results: List[RepeatResult] = []
    chosen_params_key: List[str] = []

    for i in range(repeats):
        seed = int(args.seed_base + i)

        # train/val split (train 내부에서만)
        if split_mode == "group":
            assert groups_train is not None
            if args.group_stratified:
                tr_idx, va_idx = pick_group_val_split_stratified(
                    y=y_train_full, groups=groups_train, seed=seed, val_ratio=args.val_ratio, tries=args.tries
                )
            else:
                gss = GroupShuffleSplit(n_splits=1, test_size=args.val_ratio, random_state=seed)
                tr_idx, va_idx = next(gss.split(np.arange(len(y_train_full)), groups=groups_train))
        else:
            tr_idx, va_idx = pick_random_val_split_stratified(y_train_full, seed=seed, val_ratio=args.val_ratio)

        X_tr, y_tr = X_train_full[tr_idx], y_train_full[tr_idx]
        X_va, y_va = X_train_full[va_idx], y_train_full[va_idx]

        best_params, thr, val_m = select_best_candidate_on_val(
            X_tr=X_tr, y_tr=y_tr, X_va=X_va, y_va=y_va,
            seed=seed,
            model_kind=model_kind,
            candidates=candidates,
            class_weight=cw,
            logreg_C=args.C,
            logreg_max_iter=args.max_iter,
            logreg_solver=args.solver,
            tune_thr=args.tune_threshold,
            thr_metric=args.threshold_metric,
            thr_min=args.thr_min,
            thr_max=args.thr_max,
            thr_steps=args.thr_steps,
            fixed_thr=args.fixed_thr,
        )

        est = build_estimator(
            kind=model_kind, seed=seed, class_weight=cw,
            logreg_C=args.C, logreg_max_iter=args.max_iter, logreg_solver=args.solver,
            rf_params=best_params if model_kind == "rf" else None,
        )
        est.fit(X_tr, y_tr)

        te_score = est.predict_proba(X_test)[:, 1]
        y_pred = (te_score >= thr).astype(int)
        te_m = compute_metrics(y_test, y_pred, y_score=te_score)
        te_m["thr"] = float(thr)

        results.append(
            RepeatResult(
                test_metrics=te_m,
                val_metrics=val_m,
                chosen_thr=float(thr),
                model_kind=model_kind,
                model_params=dict(best_params),
            )
        )
        chosen_params_key.append(json.dumps(best_params, sort_keys=True, ensure_ascii=False))

    # --- threshold 안정화: repeats에서 선택된 threshold 요약값 사용 ---
    thr_list = [r.chosen_thr for r in results if r.chosen_thr is not None]
    thr_mean = float(np.mean(thr_list)) if thr_list else 0.5
    thr_median = float(np.median(thr_list)) if thr_list else 0.5

    # 6) BEST 파라미터 선택(=mean val metric 최대)
    best_params: Dict[str, object] = {}
    if model_kind == "rf":
        scores_by_key: Dict[str, List[float]] = {}
        for r, k in zip(results, chosen_params_key):
            scores_by_key.setdefault(k, []).append(metric_value(r.val_metrics, args.threshold_metric))
        best_key = max(scores_by_key.items(), key=lambda kv: float(np.nanmean(np.array(kv[1], dtype=float))))[0]
        best_params = json.loads(best_key)

    # 7) 최종 모델(fit on FULL train)
    seed_final = int(args.seed_base)

    # final_model 선택: BEST / LAST
    if args.final_model == "LAST":
        final_params = results[-1].model_params
        if args.fixed_thr is not None:
            final_thr = float(args.fixed_thr)
        elif args.tune_threshold:
            # 마지막 repeat에서 선택된 thr 그대로 사용
            final_thr = float(results[-1].chosen_thr)
        else:
            final_thr = 0.5
    else:
        # BEST: RF면 best_params, logreg면 {}
        final_params = best_params if model_kind == "rf" else {}
        if args.fixed_thr is not None:
            final_thr = float(args.fixed_thr)
        elif args.tune_threshold:
            # 단일 split 재튜닝 대신, repeats 중앙값으로 안정화
            final_thr = thr_median   # 필요하면 thr_mean으로 바꿔도 OK
        else:
            final_thr = 0.5

    final_est = build_estimator(
        kind=model_kind, seed=seed_final, class_weight=cw,
        logreg_C=args.C, logreg_max_iter=args.max_iter, logreg_solver=args.solver,
        rf_params=final_params if model_kind == "rf" else None,
    )
    final_est.fit(X_train_full, y_train_full)

    te_score = final_est.predict_proba(X_test)[:, 1]
    y_pred = (te_score >= final_thr).astype(int)
    final_test_m = compute_metrics(y_test, y_pred, y_score=te_score)
    final_test_m["thr"] = float(final_thr)

    # 8) report 저장
    os.makedirs(args.report_dir, exist_ok=True)
    date = today_yyyymmdd()

    if args.report_name:
        report_name = args.report_name
    else:
        parts = [f"baseline_eval_{date}", "traintest"]
        if split_mode == "group":
            parts.append(f"group_{args.group_key}")
            if args.group_stratified:
                parts.append("strat")
        else:
            parts.append("random")
        if getattr(args, "rf_grid", False):
            parts.append("rfgrid")
        if args.tune_threshold:
            parts.append("thr")
        report_name = "_".join(parts) + ".md"

    report_path = os.path.join(args.report_dir, report_name)

    # repeats 요약
    def summarize(vals: List[float]) -> Dict[str, float]:
        arr = np.array(vals, dtype=float)
        return {"mean": float(np.nanmean(arr)), "min": float(np.nanmin(arr)), "max": float(np.nanmax(arr))}

    def fmt_stats(name: str, s: Dict[str, float]) -> str:
        return f"- {name:<9} mean={s['mean']:.4f} min={s['min']:.4f} max={s['max']:.4f}"

    keys = ["acc", "bal_acc", "f1_1", "recall_1", "prec_1", "ap", "roc_auc", "thr"]
    summary = {k: summarize([r.test_metrics.get(k, float("nan")) for r in results]) for k in keys}

    lines: List[str] = []
    lines.append(f"# Baseline Eval ({date})")
    lines.append("")
    lines.append("## Data")
    lines.append(f"- train: `{args.train_path}`")
    lines.append(f"- test: `{args.test_path}`")
    lines.append(f"- train rows: {len(y_train_full)}")
    lines.append(f"- test rows: {len(y_test)}")
    lines.append(f"- train pos_rate: {float(np.mean(y_train_full)):.4f}")
    lines.append(f"- test pos_rate: {float(np.mean(y_test)):.4f}")
    if overlap_groups is not None:
        lines.append(f"- overlap groups: {len(overlap_groups)} (dropped train rows={dropped_overlap})")
    lines.append("")

    lines.append("## Split")
    lines.append(f"- split_mode: {split_mode} (train->val only)")
    if split_mode == "group":
        lines.append(f"- group_key: {group_col}")
        lines.append(f"- group_stratified: {bool(args.group_stratified)} (tries={args.tries})")
    lines.append(f"- val_ratio: {args.val_ratio}")
    lines.append(f"- repeats: {repeats} (seed_base={args.seed_base})")
    lines.append("")

    lines.append("## Model")
    lines.append(f"- kind: {model_kind}")
    lines.append(f"- class_weight: {args.class_weight}")
    if model_kind == "logreg":
        lines.append(f"- C: {args.C}")
        lines.append(f"- solver: {args.solver}")
    if model_kind == "rf":
        lines.append(f"- rf_grid: {bool(args.rf_grid)} (candidates={len(candidates)})")
        lines.append(f"- final_params: {json.dumps(final_params, ensure_ascii=False)}")
    lines.append(f"- tune_threshold: {bool(args.tune_threshold)} (metric={args.threshold_metric})")
    lines.append(f"- final_model: {args.final_model}")
    lines.append("")

    lines.append("### Metrics / TEST (over repeats)")
    for k in keys:
        lines.append(fmt_stats(k, summary[k]))
    lines.append("")

    lines.append("### Final Model (fit on FULL train)")
    lines.append(f"- thr: {final_thr:.4f}")
    lines.append(f"- thr_repeats_mean: {thr_mean:.4f}")
    lines.append(f"- thr_repeats_median: {thr_median:.4f}")
    lines.append("- test metrics:")
    for k in ["acc", "bal_acc", "f1_1", "recall_1", "prec_1", "ap", "roc_auc"]:
        lines.append(f"  - {k}: {final_test_m.get(k, float('nan')):.4f}")
    lines.append("")

    lines.append("## Features")
    lines.append(f"- num_features: {len(feat_cols)}")
    lines.append(f"- feature_cols: {', '.join(feat_cols[:30])}" + (" ..." if len(feat_cols) > 30 else ""))
    lines.append("")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n".join(lines))
    print(f"\n[OK] report saved: {report_path}")

    # 9) save model/meta
    if args.save_model:
        os.makedirs(os.path.dirname(args.save_model) or ".", exist_ok=True)
        joblib.dump(final_est, args.save_model)
        print(f"[OK] model saved: {args.save_model}")

    if args.save_meta:
        os.makedirs(os.path.dirname(args.save_meta) or ".", exist_ok=True)
        meta = {
            "date": date,
            "train": args.train_path,
            "test": args.test_path,
            "label_col": label_col,
            "group_key": group_col,
            "features": feat_cols,
            "model_kind": model_kind,
            "model_params": final_params,
            "thr": float(final_thr),
            "test_metrics": final_test_m,
        }
        with open(args.save_meta, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        print(f"[OK] meta saved: {args.save_meta}")


def main():
    ap = argparse.ArgumentParser()

    # 기존 호출 깨질 수 있어서 alias 여러 개 지원
    ap.add_argument("--dataset", "--dataset_path", "--csv", dest="dataset_path", default="")
    ap.add_argument("--train", dest="train_path", default="")
    ap.add_argument("--test", dest="test_path", default="")
    ap.add_argument("--k", type=int, default=None)

    ap.add_argument("--split_mode", choices=["random", "group"], default="group")
    ap.add_argument("--group", action="store_true")
    ap.add_argument("--random", action="store_true")
    ap.add_argument("--group_key", "--group-key", default="pair_key")
    ap.add_argument("--group_stratified", "--group-stratified", action="store_true")
    ap.add_argument("--tries", type=int, default=200)

    ap.add_argument("--test_ratio", type=float, default=0.2)
    ap.add_argument("--val_ratio", type=float, default=0.2)

    ap.add_argument("--seed_base", type=int, default=42)
    ap.add_argument("--repeats", type=int, default=20)
    ap.add_argument("--fixed_test", action="store_true")

    ap.add_argument("--model", choices=["majority", "logreg"], default="logreg")
    ap.add_argument("--class_weight", default="balanced")  # balanced / none / "0:1,1:3"
    ap.add_argument("--C", type=float, default=1.0)
    ap.add_argument("--max_iter", type=int, default=2000)
    ap.add_argument("--solver", default="lbfgs")

    ap.add_argument("--tune_threshold", "--tune-threshold", action="store_true")
    ap.add_argument("--threshold_metric", choices=["f1", "recall", "precision", "bal_acc"], default="f1")

    ap.add_argument("--report_dir", default="reports")
    ap.add_argument("--report_name", default="")

    ap.add_argument("--label_col", default="")
    ap.add_argument("--drop_ties", action="store_true")

    ap.add_argument("--shuffle_labels", action="store_true")
    ap.add_argument("--shuffle_seed", type=int, default=123)

    ap.add_argument("--drop_adv_features", action="store_true")
    ap.add_argument("--drop_perk_features", action="store_true")

    ap.add_argument("--thr_min", type=float, default=0.05)
    ap.add_argument("--thr_max", type=float, default=0.95)
    ap.add_argument("--thr_steps", type=int, default=91)

    ap.add_argument("--fixed_thr", type=float, default=None)

    ap.add_argument("--drop-overlap-groups", dest="drop_overlap_groups", action="store_true")
    ap.add_argument("--rf-grid", dest="rf_grid", action="store_true")
    ap.add_argument("--save-model", dest="save_model", default="")
    ap.add_argument("--save-meta", dest="save_meta", default="")
    ap.add_argument("--final-model", dest="final_model", choices=["BEST","LAST"], default="BEST")

    args = ap.parse_args()

    if args.group:  args.split_mode = "group"
    if args.random: args.split_mode = "random"

    if args.train_path or args.test_path:
        run_train_test_mode(args)
        return

    if not args.dataset_path:
        raise ValueError("provide --dataset or --train/--test")

    df = pd.read_csv(args.dataset_path, low_memory=False)

    # 1) label column 결정 (없으면 wins/rate로 파생 생성)
    label_col = args.label_col.strip() if hasattr(args, "label_col") else ""

    if label_col and (label_col not in df.columns):
        raise ValueError(f"[train_baseline] --label_col='{label_col}' not found in csv columns")

    if not label_col:
        try:
            label_col = resolve_label_col(df.columns)
        except ValueError:
            # label이 없다면 자동 파생 생성
            if ("wins_defender" in df.columns) and ("wins_attacker" in df.columns):
                # defender 승수가 attacker 승수보다 많으면 label=1
                if getattr(args, "drop_ties", False):
                    df = df[df["wins_defender"] != df["wins_attacker"]].copy()
                df["_label"] = (df["wins_defender"] > df["wins_attacker"]).astype(int)
                label_col = "_label"
            elif ("defender_win_rate" in df.columns) and ("attacker_win_rate" in df.columns):
                # defender win_rate가 더 크면 label=1
                if getattr(args, "drop_ties", False):
                    df = df[np.abs(df["defender_win_rate"] - df["attacker_win_rate"]) > 1e-12].copy()
                df["_label"] = (df["defender_win_rate"] > df["attacker_win_rate"]).astype(int)
                label_col = "_label"
            else:
                raise ValueError(
                    "[train_baseline] label column not found, and cannot derive label. "
                    "Need (wins_defender & wins_attacker) or (defender_win_rate & attacker_win_rate)."
                )

    # 2) group column / features 결정
    group_col = resolve_group_col(df.columns, args.group_key) if args.split_mode == "group" else None
    feat_cols = select_feature_cols(df, label_col, group_col, args.drop_adv_features, args.drop_perk_features)

    needed = feat_cols + [label_col] + ([group_col] if group_col else [])
    df = df.dropna(subset=needed).reset_index(drop=True)

    X = df[feat_cols].to_numpy(dtype=float)
    y = df[label_col].astype(int).to_numpy()

    if args.shuffle_labels:
        rng = np.random.RandomState(args.shuffle_seed)
        y = rng.permutation(y)
        print(f"[SANITY] labels shuffled (seed={args.shuffle_seed})")

    groups = df[group_col].astype(str).to_numpy() if group_col else None

    dist0 = int(np.sum(y == 0))
    dist1 = int(np.sum(y == 1))
    majority_class = 0 if dist0 >= dist1 else 1

    fixed_test_groups: Optional[np.ndarray] = None
    fixed_test_pos_rate: Optional[float] = None
    if args.split_mode == "group" and args.fixed_test:
        assert groups is not None
        base_split = pick_group_split_stratified(
            y=y,
            groups=groups,
            seed=args.seed_base,
            test_ratio=args.test_ratio,
            val_ratio=args.val_ratio,
            tries=args.tries if args.group_stratified else 1,
        )
        fixed_test_groups = np.unique(groups[base_split.test_idx])
        fixed_test_pos_rate = base_split.test_pos_rate

    metrics_runs: List[Dict[str, float]] = []
    test_pos_rates: List[float] = []
    thr_list: List[float] = []
    cm_sum = np.zeros((2, 2), dtype=int)

    for i in range(args.repeats):
        seed = args.seed_base + i

        if args.split_mode == "random":
            split = random_split_stratified(y, seed, args.test_ratio, args.val_ratio)
        else:
            assert groups is not None
            split = pick_group_split_stratified(
                y=y,
                groups=groups,
                seed=seed,
                test_ratio=args.test_ratio,
                val_ratio=args.val_ratio,
                tries=args.tries if args.group_stratified else 1,
                fixed_test_groups=fixed_test_groups,
            )

        test_pos_rates.append(split.test_pos_rate)

        X_tr, y_tr = X[split.train_idx], y[split.train_idx]
        X_va, y_va = X[split.val_idx], y[split.val_idx]
        X_te, y_te = X[split.test_idx], y[split.test_idx]

        if args.model == "majority":
            y_pred = np.full_like(y_te, majority_class)
            cm_sum += confusion_matrix(y_te, y_pred, labels=[0, 1])
            metrics_runs.append(compute_metrics(y_te, y_pred))
            continue

        cw = parse_class_weight(args.class_weight)

        pipe = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "clf",
                    LogisticRegression(
                        C=args.C,
                        class_weight=cw,
                        max_iter=args.max_iter,
                        solver=args.solver,
                    ),
                ),
            ]
        )
        pipe.fit(X_tr, y_tr)

        thr = 0.5
        va_score = pipe.predict_proba(X_va)[:, 1]

        if args.fixed_thr is not None:
            thr = float(args.fixed_thr)
        elif args.tune_threshold:
            thr, _ = tune_threshold(
                y_va, va_score,
                metric=args.threshold_metric,
                thr_min=args.thr_min,
                thr_max=args.thr_max,
                thr_steps=args.thr_steps,
            )
        thr_list.append(float(thr))

        te_score = pipe.predict_proba(X_te)[:, 1]
        y_pred = (te_score >= thr).astype(int)

        cm_sum += confusion_matrix(y_te, y_pred, labels=[0, 1])
        m = compute_metrics(y_te, y_pred, y_score=te_score)
        m["thr"] = float(thr)
        metrics_runs.append(m)

    keys = ["acc", "bal_acc", "f1_1", "recall_1", "prec_1"]
    if args.model != "majority":
        keys += ["ap", "roc_auc", "thr"]

    summary = {k: summarize([m.get(k, float("nan")) for m in metrics_runs]) for k in keys}
    tpr_stats = summarize(test_pos_rates)

    os.makedirs(args.report_dir, exist_ok=True)

    date = today_yyyymmdd()
    if args.report_name:
        report_name = args.report_name
    else:
        parts = [f"baseline_eval_{date}"]
        if args.split_mode == "group":
            parts.append(f"group_{args.group_key}")
            if args.group_stratified:
                parts.append("strat")
            if args.fixed_test:
                parts.append("fixedtest")
        else:
            parts.append("random")

        if args.model == "logreg" and args.tune_threshold:
            parts.append("thr")

        report_name = "_".join(parts) + ".md"

    report_path = os.path.join(args.report_dir, report_name)

    lines: List[str] = []
    lines.append(f"# Baseline Eval ({date})")
    lines.append("")
    lines.append("## Data")
    lines.append(f"- dataset: `{args.dataset_path}`")
    lines.append(f"- rows: {len(y)}")
    lines.append(f"- label distribution: {{0: {dist0}, 1: {dist1}}}")
    lines.append("")
    lines.append("## Split")
    lines.append(f"- split_mode: {args.split_mode}")
    if args.split_mode == "group":
        lines.append(f"- group_key: {group_col}")
        lines.append(f"- group_stratified: {bool(args.group_stratified)} (tries={args.tries})")
        lines.append(f"- fixed_test: {bool(args.fixed_test)}")
        if fixed_test_groups is not None:
            lines.append(f"- fixed_test_groups: {len(fixed_test_groups)}")
            lines.append(f"- fixed_test_pos_rate: {fixed_test_pos_rate:.4f}")
    lines.append(f"- test_ratio: {args.test_ratio}")
    lines.append(f"- val_ratio: {args.val_ratio}")
    lines.append(f"- repeats: {args.repeats} (seed_base={args.seed_base})")
    lines.append("")
    lines.append("### test_pos_rate (label=1) / SPLIT")
    lines.append(f"- mean={tpr_stats['mean']:.4f} min={tpr_stats['min']:.4f} max={tpr_stats['max']:.4f}")
    lines.append("")

    lines.append("## Majority Baseline (always=majority)")
    majority_all = compute_metrics(y, np.full_like(y, majority_class))
    lines.append(f"- majority_class: {majority_class}")
    lines.append(
        f"- acc(all): {majority_all['acc']:.4f}  bal_acc(all): {majority_all['bal_acc']:.4f}  f1_1(all): {majority_all['f1_1']:.4f}"
    )
    lines.append("")

    lines.append(f"## Model: {args.model}")
    if args.model == "logreg":
        lines.append(f"- class_weight: {args.class_weight}")
        lines.append(f"- C: {args.C}")
        lines.append(f"- tune_threshold: {bool(args.tune_threshold)} (metric={args.threshold_metric})")
        if thr_list:
            thr_stats = summarize(thr_list)
            lines.append(f"- threshold stats: mean={thr_stats['mean']:.3f} min={thr_stats['min']:.3f} max={thr_stats['max']:.3f}")
    lines.append("")

    lines.append("### Metrics / TEST")
    for k in keys:
        lines.append(fmt_stats(k, summary[k]))
    lines.append("")
    lines.append("### Confusion Matrix (sum over repeats)")
    lines.append(f"- TN={cm_sum[0,0]} FP={cm_sum[0,1]} FN={cm_sum[1,0]} TP={cm_sum[1,1]}")
    lines.append("")
    lines.append("## Features")
    lines.append(f"- num_features: {len(feat_cols)}")
    lines.append(f"- feature_cols: {', '.join(feat_cols[:30])}" + (" ..." if len(feat_cols) > 30 else ""))
    lines.append("")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n".join(lines))
    print(f"\n[OK] report saved: {report_path}")


if __name__ == "__main__":
    main()
