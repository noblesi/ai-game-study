# Baseline Evaluation Report
- generated_at: 2025-12-28T18:28:29
- input: datasets/battle_dataset_v1.csv
- rows: 120
- usable_rows: 120
- label_distribution: {0: 99, 1: 21}
- test_ratio: 0.2
- seed: 42
- K(splits): 3

## Summary

| model | acc(mean) | bal_acc(mean) | f1_1(mean) | recall_1(mean) | precision_1(mean) | confusion_sum |
|---|---:|---:|---:|---:|---:|---|
| MAJORITY_SPLIT | 0.8333 | 0.5000 | 0.0000 | 0.0000 | 0.0000 | TN=60 FP=0 FN=12 TP=0 |
| LR | 0.8333 | 0.6000 | 0.3016 | 0.2500 | 0.3889 | TN=57 FP=3 FN=9 TP=3 |
| LR_balanced | 0.8194 | 0.6250 | 0.3333 | 0.3333 | 0.3333 | TN=55 FP=5 FN=8 TP=4 |
| DT_balanced | 0.8056 | 0.5500 | 0.2063 | 0.1667 | 0.2778 | TN=56 FP=4 FN=10 TP=2 |
| RF_balanced_subsample | 0.7917 | 0.4750 | 0.0000 | 0.0000 | 0.0000 | TN=57 FP=3 FN=12 TP=0 |

## Split Mode

- mode: group
- group_key: pair_key_full
- n_groups: 120


## Best Model

- metric: f1_1(mean)
- best: LR_balanced
- f1_1_mean: 0.3333

## Top Features (fit on full data)

- kind: lr_coef_abs

| rank | feature | score |
|---:|---|---:|
| 1 | defender_count | 1.391289 |
| 2 | start_distance | 1.109796 |
| 3 | a_dps | 0.979243 |
| 4 | d_ttk_est | 0.863378 |
| 5 | dps_adv | 0.840259 |
| 6 | datk | 0.808707 |
| 7 | d_atk | 0.781425 |
| 8 | d_dps | 0.728673 |
| 9 | d_move_speed | 0.680508 |
| 10 | dmove_speed | 0.622048 |
| 11 | perk_adv_lifesteal | 0.591505 |
| 12 | d_has_perk_lifesteal | 0.582113 |

## Threshold Tuning

- model: LR_balanced
- best_threshold: 0.50
- f1_1: 0.3810
- recall_1: 0.3333
- precision_1: 0.4444
- bal_acc: 0.6250
- cm_sum: TN=55 FP=5 FN=8 TP=4

Top 5 thresholds by f1_1:

| rank | thr | f1_1 | recall_1 | precision_1 | bal_acc |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.50 | 0.3810 | 0.3333 | 0.4444 | 0.6250 |
| 2 | 0.55 | 0.3810 | 0.3333 | 0.4444 | 0.6250 |
| 3 | 0.60 | 0.3810 | 0.3333 | 0.4444 | 0.6250 |
| 4 | 0.10 | 0.3750 | 0.5000 | 0.3000 | 0.6333 |
| 5 | 0.45 | 0.3636 | 0.3333 | 0.4000 | 0.6167 |

## RF Grid Search

- (not run)
