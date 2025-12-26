# Baseline Evaluation Report
- generated_at: 2025-12-26T12:37:13
- input: datasets/battle_dataset_v1.csv
- rows: 498
- usable_rows: 498
- label_distribution: {1: 156, 0: 342}
- test_ratio: 0.2
- seed: 42
- K(splits): 10

## Summary

| model | acc(mean) | bal_acc(mean) | f1_1(mean) | recall_1(mean) | precision_1(mean) | confusion_sum |
|---|---:|---:|---:|---:|---:|---|
| MAJORITY_SPLIT | 0.6648 | 0.5000 | 0.0000 | 0.0000 | 0.0000 | TN=674 FP=0 FN=342 TP=0 |
| LR | 0.7124 | 0.6594 | 0.5301 | 0.5027 | 0.5710 | TN=549 FP=125 FN=167 TP=175 |
| LR_balanced | 0.7068 | 0.7111 | 0.6175 | 0.7317 | 0.5473 | TN=463 FP=211 FN=88 TP=254 |
| DT_balanced | 0.6995 | 0.6470 | 0.4991 | 0.4743 | 0.5584 | TN=553 FP=121 FN=188 TP=154 |
| RF_balanced_subsample | 0.7305 | 0.6577 | 0.5137 | 0.4435 | 0.6849 | TN=587 FP=87 FN=189 TP=153 |

## Split Mode

- mode: group
- group_key: pair_key
- n_groups: 150


## Best Model

- metric: f1_1(mean)
- best: LR_balanced
- f1_1_mean: 0.6175

## Top Features (fit on full data)

- kind: lr_coef_abs

| rank | feature | score |
|---:|---|---:|
| 1 | dps_adv | 1.906548 |
| 2 | a_dps | 1.613662 |
| 3 | dhp | 1.379818 |
| 4 | d_dps | 1.365794 |
| 5 | d_hp | 1.293664 |
| 6 | d_atk | 1.133477 |
| 7 | datk | 0.979563 |
| 8 | a_atk | 0.773905 |
| 9 | a_ttk_est | 0.734007 |
| 10 | encounter_is_swarm | 0.671356 |
| 11 | d_has_perk_lifesteal | 0.640603 |
| 12 | a_has_perk_longshot | 0.640377 |

## Threshold Tuning

- model: LR_balanced
- best_threshold: 0.50
- f1_1: 0.6295
- recall_1: 0.7427
- precision_1: 0.5462
- bal_acc: 0.7148
- cm_sum: TN=463 FP=211 FN=88 TP=254

Top 5 thresholds by f1_1:

| rank | thr | f1_1 | recall_1 | precision_1 | bal_acc |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.50 | 0.6295 | 0.7427 | 0.5462 | 0.7148 |
| 2 | 0.45 | 0.6190 | 0.7719 | 0.5166 | 0.7027 |
| 3 | 0.55 | 0.6096 | 0.6871 | 0.5478 | 0.6997 |
| 4 | 0.40 | 0.6054 | 0.7895 | 0.4909 | 0.6870 |
| 5 | 0.30 | 0.6052 | 0.8918 | 0.4580 | 0.6781 |

## RF Grid Search

- (not run)
