from __future__ import annotations

import argparse
import datetime as dt
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

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


def main():
    ap = argparse.ArgumentParser()

    # 기존 호출 깨질 수 있어서 alias 여러 개 지원
    ap.add_argument("--dataset", "--dataset_path", "--csv", dest="dataset_path", required=True)

    ap.add_argument("--split_mode", choices=["random", "group"], default="group")
    ap.add_argument("--group_key", default="pair_key")
    ap.add_argument("--group_stratified", action="store_true")
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

    ap.add_argument("--tune_threshold", action="store_true")
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

    args = ap.parse_args()

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
