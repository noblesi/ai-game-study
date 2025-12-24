# Baseline Evaluation Report
- generated_at: 2025-12-24T17:47:44
- input: datasets/scenarios_v1.csv
- rows: 18
- usable_rows: 18
- label_distribution: {1: 8, 0: 10}
- test_ratio: 0.2
- seed: 42
- K(splits): 10

## Summary

| model | acc(mean) | bal_acc(mean) | f1_1(mean) | recall_1(mean) | precision_1(mean) | confusion_sum |
|---|---:|---:|---:|---:|---:|---|
| MAJORITY_SPLIT | 0.5000 | 0.5000 | 0.0000 | 0.0000 | 0.0000 | TN=20 FP=0 FN=20 TP=0 |
| LR | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | TN=20 FP=0 FN=0 TP=20 |
| LR_balanced | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | TN=20 FP=0 FN=0 TP=20 |
| DT_balanced | 0.9000 | 0.9000 | 0.8667 | 0.9000 | 0.8500 | TN=18 FP=2 FN=2 TP=18 |
| RF_balanced_subsample | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | TN=20 FP=0 FN=0 TP=20 |

## Split Mode

- mode: group
- group_key: pair_key
- n_groups: 9


## Best Model

- metric: f1_1(mean)
- best: LR
- f1_1_mean: 1.0000

## Top Features (fit on full data)

- kind: lr_coef_abs

| rank | feature | score |
|---:|---|---:|
| 1 | dps_adv | 0.544685 |
| 2 | datk | 0.533521 |
| 3 | d_atk | 0.521062 |
| 4 | d_dps | 0.483273 |
| 5 | d_hp | 0.479615 |
| 6 | dhp | 0.478923 |
| 7 | ttk_adv | 0.476337 |
| 8 | a_ttk_est | 0.336322 |
| 9 | d_ttk_est | 0.261181 |
| 10 | dattack_speed | 0.233338 |
| 11 | a_attack_speed | 0.190559 |
| 12 | a_hp | 0.147944 |

## Threshold Tuning

- (not run)

## RF Grid Search

- (not run)
