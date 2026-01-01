# Portfolio Visuals — 2025-12-31 Baseline (RF, Recall-tuned)

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
