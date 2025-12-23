# Baseline Evaluation Report
- generated_at: 2025-12-23T20:03:38
- input: datasets/battle_dataset_scenarios_v1.csv
- rows: 24
- usable_rows: 24
- label_distribution: {1: 12, 0: 12}
- test_ratio: 0.2
- seed: 42
- K(splits): 10

## Summary

| model | acc(mean) | bal_acc(mean) | f1_1(mean) | recall_1(mean) | precision_1(mean) | confusion_sum |
|---|---:|---:|---:|---:|---:|---|
| MAJORITY_SPLIT | 0.3000 | 0.4500 | 0.0800 | 0.2000 | 0.0500 | TN=10 FP=6 FN=22 TP=2 |
| LR | 1.0000 | 0.9500 | 1.0000 | 1.0000 | 1.0000 | TN=16 FP=0 FN=0 TP=24 |
| LR_balanced | 1.0000 | 0.9500 | 1.0000 | 1.0000 | 1.0000 | TN=16 FP=0 FN=0 TP=24 |
| DT_balanced | 0.9500 | 0.9250 | 0.9667 | 0.9500 | 1.0000 | TN=16 FP=0 FN=2 TP=22 |
| RF_balanced_subsample | 1.0000 | 0.9500 | 1.0000 | 1.0000 | 1.0000 | TN=16 FP=0 FN=0 TP=24 |

## Split Mode

- mode: random


## Best Model

- metric: f1_1(mean)
- best: LR
- f1_1_mean: 1.0000

## Top Features (fit on full data)

- kind: lr_coef_abs

| rank | feature | score |
|---:|---|---:|
| 1 | datk | 0.697453 |
| 2 | dhp | 0.585567 |
| 3 | ttk_adv | 0.549572 |
| 4 | d_dps | 0.538010 |
| 5 | d_hp | 0.535753 |
| 6 | d_atk | 0.503020 |
| 7 | dps_adv | 0.478249 |
| 8 | a_ttk_est | 0.388846 |
| 9 | d_ttk_est | 0.316200 |
| 10 | a_atk | 0.296220 |
| 11 | d_move_speed | 0.213694 |
| 12 | a_hp | 0.184882 |

## Threshold Tuning

- (not run)

## RF Grid Search

- (not run)
