from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    average_precision_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    precision_recall_curve,
    roc_curve,
)


CORE_METRICS = ["recall_1", "prec_1", "f1_1", "bal_acc"]
ALL_METRICS = ["acc", "bal_acc", "f1_1", "recall_1", "prec_1", "ap", "roc_auc"]


def _meta_get_features(meta: dict) -> list[str]:
    # meta 구조가 프로젝트별로 다를 수 있어서 후보 키를 여러 개 둠
    for k in ["feature_cols", "features", "x_cols", "cols"]:
        if k in meta and isinstance(meta[k], list):
            return meta[k]
    raise KeyError("meta에서 feature list를 찾지 못했습니다. (feature_cols/features/x_cols/cols 중 없음)")


def _meta_get_label_col(meta: dict, default: str) -> str:
    for k in ["label_col", "y_col", "target_col", "label"]:
        if k in meta and isinstance(meta[k], str):
            return meta[k]
    return default


def _meta_get_threshold(meta: dict, default: float = 0.5) -> float:
    for k in ["thr", "threshold", "best_thr"]:
        if k in meta:
            try:
                return float(meta[k])
            except Exception:
                pass
    return default


def _rf_feature_importances(model):
    # RandomForestClassifier or Pipeline
    if hasattr(model, "feature_importances_"):
        return model.feature_importances_
    if hasattr(model, "named_steps"):
        for step in model.named_steps.values():
            if hasattr(step, "feature_importances_"):
                return step.feature_importances_
    return None


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray) -> dict:
    return {
        "acc": float(accuracy_score(y_true, y_pred)),
        "bal_acc": float(balanced_accuracy_score(y_true, y_pred)),
        "f1_1": float(f1_score(y_true, y_pred, pos_label=1)),
        "recall_1": float(recall_score(y_true, y_pred, pos_label=1)),
        "prec_1": float(precision_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "ap": float(average_precision_score(y_true, y_proba)),
        "roc_auc": float(roc_auc_score(y_true, y_proba)),
    }


def save_grouped_bar(df: pd.DataFrame, metric_keys: list[str], out_png: Path, title: str):
    labels = df["label"].tolist()
    runs = df["name"].tolist()
    n = len(runs)
    x = np.arange(len(metric_keys))
    width = 0.8 / max(1, n)

    plt.figure()
    for i, (run, lab) in enumerate(zip(runs, labels)):
        vals = [df.loc[df["name"] == run, k].iloc[0] for k in metric_keys]
        plt.bar(x + (i - (n - 1) / 2) * width, vals, width, label=lab)

    plt.xticks(x, metric_keys, rotation=25, ha="right")
    plt.ylim(0.0, 1.05)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=160)
    plt.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="configs/portfolio_runs_20251231.json")
    ap.add_argument("--test", required=True, help="datasets/test_scenarios_v1.csv")
    ap.add_argument("--outdir", default="reports/portfolio_20251231")
    ap.add_argument("--label-col", default="label", help="meta에 없을 때 사용할 label 컬럼명(기본: label)")
    ap.add_argument("--top-errors", type=int, default=15)
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    runs = json.loads(Path(args.config).read_text(encoding="utf-8"))
    test_df = pd.read_csv(args.test, low_memory=False)

    summary_rows = []
    pr_curves = []
    roc_curves = []

    for run in runs:
        name = run["name"]
        label = run.get("label", name)
        model = joblib.load(run["model"])
        meta = json.loads(Path(run["meta"]).read_text(encoding="utf-8"))

        feat_cols = _meta_get_features(meta)
        label_col = _meta_get_label_col(meta, args.label_col)
        thr = _meta_get_threshold(meta, default=0.5)

        X = test_df[feat_cols].to_numpy(dtype=float)
        y_true = test_df[label_col].astype(int).to_numpy()

        y_proba = model.predict_proba(X)[:, 1]
        y_pred = (y_proba >= thr).astype(int)

        # metrics
        metrics = compute_metrics(y_true, y_pred, y_proba)
        row = {"name": name, "label": label, "thr": thr, **metrics}
        summary_rows.append(row)

        # preds csv (포트폴리오 근거)
        preds = test_df.copy()
        preds["_y_true"] = y_true
        preds["_y_proba"] = y_proba
        preds["_y_pred"] = y_pred
        preds.to_csv(outdir / f"preds_{name}.csv", index=False, encoding="utf-8-sig")

        # errors csv (FN/FP)
        fn = preds[(preds["_y_true"] == 1) & (preds["_y_pred"] == 0)].sort_values("_y_proba").head(args.top_errors)
        fp = preds[(preds["_y_true"] == 0) & (preds["_y_pred"] == 1)].sort_values("_y_proba", ascending=False).head(args.top_errors)
        fn.to_csv(outdir / f"errors_{name}_FN_top{args.top_errors}.csv", index=False, encoding="utf-8-sig")
        fp.to_csv(outdir / f"errors_{name}_FP_top{args.top_errors}.csv", index=False, encoding="utf-8-sig")

        # confusion matrix plot
        cm = confusion_matrix(y_true, y_pred)
        disp = ConfusionMatrixDisplay(cm)
        disp.plot()
        plt.title(f"Confusion Matrix - {label} (thr={thr:.3f})")
        plt.tight_layout()
        plt.savefig(outdir / f"confusion_{name}.png", dpi=160)
        plt.close()

        # PR curve data
        prec, rec, _ = precision_recall_curve(y_true, y_proba)
        pr_curves.append((label, rec, prec))

        # ROC curve data
        fpr, tpr, _ = roc_curve(y_true, y_proba)
        roc_curves.append((label, fpr, tpr))

        # feature importance (RF only)
        imps = _rf_feature_importances(model)
        if imps is not None:
            order = np.argsort(imps)[::-1][:20]
            top_feats = [feat_cols[i] for i in order]
            top_vals = imps[order]
            plt.figure()
            plt.barh(top_feats[::-1], top_vals[::-1])
            plt.title(f"Feature Importances Top20 - {label}")
            plt.tight_layout()
            plt.savefig(outdir / f"feature_importance_{name}_top20.png", dpi=160)
            plt.close()

    summary = pd.DataFrame(summary_rows)
    summary.to_csv(outdir / "metrics_summary.csv", index=False, encoding="utf-8-sig")

    # 비교 바차트 (core / all / threshold)
    save_grouped_bar(summary, CORE_METRICS, outdir / "compare_core_metrics.png", "Final Test Metrics (Core)")
    save_grouped_bar(summary, ALL_METRICS, outdir / "compare_all_metrics.png", "Final Test Metrics (All)")

    plt.figure()
    plt.bar(summary["label"].tolist(), summary["thr"].tolist())
    plt.xticks(rotation=25, ha="right")
    plt.title("Threshold by Run")
    plt.tight_layout()
    plt.savefig(outdir / "compare_threshold.png", dpi=160)
    plt.close()

    # PR overlay
    plt.figure()
    for label, rec, prec in pr_curves:
        plt.plot(rec, prec, label=label)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("PR Curves (Overlay)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outdir / "compare_pr_curves.png", dpi=160)
    plt.close()

    # ROC overlay
    plt.figure()
    for label, fpr, tpr in roc_curves:
        plt.plot(fpr, tpr, label=label)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curves (Overlay)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outdir / "compare_roc_curves.png", dpi=160)
    plt.close()

    # README.md 생성 (포트폴리오 붙이기용)
    readme = f"""# Portfolio Visuals — 2025-12-31 Baseline (RF, Recall-tuned)

## What this shows
- Same dataset / same split policy (group split, overlap dropped)
- Same model family (RandomForest, class_weight=balanced)
- Threshold tuned for **recall**
- Ablation study:
  - **Full**: all features
  - **No Perk**: perk features removed
  - **No Adv**: derived/adv features removed (DPS/TTK/adv)

## Key Figures
### Core metric comparison
![](compare_core_metrics.png)

### PR / ROC
![](compare_pr_curves.png)
![](compare_roc_curves.png)

### Confusion matrices
- Full: ![](confusion_full.png)
- No Perk: ![](confusion_no_perk.png)
- No Adv: ![](confusion_no_adv.png)

### Feature importance (Top20)
- Full: ![](feature_importance_full_top20.png)
- No Perk: ![](feature_importance_no_perk_top20.png)
- No Adv: ![](feature_importance_no_adv_top20.png)

## Artifacts
- metrics summary: `metrics_summary.csv`
- per-run predictions: `preds_*.csv`
- error cases: `errors_*_(FN/FP)_topN.csv`
"""
    (outdir / "README.md").write_text(readme, encoding="utf-8")

    print("[OK] Portfolio pack generated:", outdir)


if __name__ == "__main__":
    main()
