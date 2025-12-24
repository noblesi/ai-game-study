# Baseline Evaluation Report
- generated_at: 2025-12-24T21:44:49
- input: datasets/battle_dataset_v1.csv
- rows: 498
- usable_rows: 498
- label_distribution: {1: 123, 0: 375}
- test_ratio: 0.2
- seed: 42
- K(splits): 10

## Summary

| model | acc(mean) | bal_acc(mean) | f1_1(mean) | recall_1(mean) | precision_1(mean) | confusion_sum |
|---|---:|---:|---:|---:|---:|---|
| MAJORITY_SPLIT | 0.7538 | 0.5000 | 0.0000 | 0.0000 | 0.0000 | TN=742 FP=0 FN=241 TP=0 |
| LR | 0.7339 | 0.5681 | 0.3011 | 0.2443 | 0.4765 | TN=662 FP=80 FN=182 TP=59 |
| LR_balanced | 0.6823 | 0.6501 | 0.4754 | 0.5951 | 0.4072 | TN=524 FP=218 FN=95 TP=146 |
| DT_balanced | 0.7903 | 0.7016 | 0.5527 | 0.5245 | 0.5993 | TN=652 FP=90 FN=116 TP=125 |
| RF_balanced_subsample | 0.7793 | 0.6389 | 0.4432 | 0.3641 | 0.6174 | TN=677 FP=65 FN=153 TP=88 |

## Split Mode

- mode: group
- group_key: pair_key
- n_groups: 234


## Best Model

- metric: f1_1(mean)
- best: DT_balanced
- f1_1_mean: 0.5527

## Top Features (fit on full data)

- kind: tree_importance

| rank | feature | score |
|---:|---|---:|
| 1 | ttk_adv | 0.360662 |
| 2 | d_range | 0.106561 |
| 3 | d_hp | 0.088344 |
| 4 | a_move_speed | 0.079117 |
| 5 | d_ttk_est | 0.074455 |
| 6 | datk | 0.056606 |
| 7 | a_dps | 0.050123 |
| 8 | a_ttk_est | 0.043354 |
| 9 | dps_adv | 0.035524 |
| 10 | d_atk | 0.032362 |
| 11 | d_move_speed | 0.031870 |
| 12 | d_dps | 0.024782 |

## Threshold Tuning

- model: DT_balanced
- best_threshold: 0.02
- f1_1: 0.5482
- recall_1: 0.5187
- precision_1: 0.5814
- bal_acc: 0.6987
- cm_sum: TN=652 FP=90 FN=116 TP=125

Top 5 thresholds by f1_1:

| rank | thr | f1_1 | recall_1 | precision_1 | bal_acc |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.02 | 0.5482 | 0.5187 | 0.5814 | 0.6987 |
| 2 | 0.04 | 0.5482 | 0.5187 | 0.5814 | 0.6987 |
| 3 | 0.06 | 0.5482 | 0.5187 | 0.5814 | 0.6987 |
| 4 | 0.08 | 0.5482 | 0.5187 | 0.5814 | 0.6987 |
| 5 | 0.10 | 0.5482 | 0.5187 | 0.5814 | 0.6987 |

## RF Grid Search

- (not run)
