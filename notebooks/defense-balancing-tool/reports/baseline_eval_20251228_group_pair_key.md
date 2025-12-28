# Baseline Evaluation Report
- generated_at: 2025-12-28T20:07:19
- input: datasets/battle_dataset_v1.csv
- rows: 1800
- usable_rows: 1800
- label_distribution: {0: 1503, 1: 297}
- test_ratio: 0.2
- seed: 42
- K(splits): 10

## Summary

| model | acc(mean) | bal_acc(mean) | f1_1(mean) | recall_1(mean) | precision_1(mean) | confusion_sum |
|---|---:|---:|---:|---:|---:|---|
| MAJORITY_SPLIT | 0.8368 | 0.5000 | 0.0000 | 0.0000 | 0.0000 | TN=3043 FP=0 FN=593 TP=0 |
| LR | 0.8483 | 0.6598 | 0.4424 | 0.3800 | 0.5494 | TN=2859 FP=184 FN=368 TP=225 |
| LR_balanced | 0.7843 | 0.7520 | 0.5120 | 0.7041 | 0.4073 | TN=2432 FP=611 FN=176 TP=417 |
| DT_balanced | 0.8360 | 0.7110 | 0.5089 | 0.5238 | 0.5155 | TN=2734 FP=309 FN=286 TP=307 |
| RF_balanced_subsample | 0.8528 | 0.6478 | 0.4239 | 0.3431 | 0.5957 | TN=2898 FP=145 FN=390 TP=203 |

## Split Mode

- mode: group
- group_key: pair_key
- n_groups: 337


## Best Model

- metric: f1_1(mean)
- best: LR_balanced
- f1_1_mean: 0.5120

## Top Features (fit on full data)

- kind: lr_coef_abs

| rank | feature | score |
|---:|---|---:|
| 1 | a_dps | 2.319446 |
| 2 | dps_adv | 1.464612 |
| 3 | datk | 1.405964 |
| 4 | d_atk | 1.308693 |
| 5 | d_dps | 1.139858 |
| 6 | encounter_is_swarm | 0.800064 |
| 7 | a_ttk_est | 0.786855 |
| 8 | ttk_adv | 0.781856 |
| 9 | start_distance | 0.765392 |
| 10 | a_atk | 0.751819 |
| 11 | a_range | 0.606151 |
| 12 | d_attack_speed | 0.597456 |

## Threshold Tuning

- (not run)

## RF Grid Search

- (not run)
