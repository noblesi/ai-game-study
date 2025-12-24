# Baseline Evaluation Report
- generated_at: 2025-12-24T17:48:58
- input: datasets/experiments_v1.csv
- rows: 360
- usable_rows: 360
- label_distribution: {0: 250, 1: 110}
- test_ratio: 0.2
- seed: 42
- K(splits): 10

## Summary

| model | acc(mean) | bal_acc(mean) | f1_1(mean) | recall_1(mean) | precision_1(mean) | confusion_sum |
|---|---:|---:|---:|---:|---:|---|
| MAJORITY_SPLIT | 0.6905 | 0.5000 | 0.0000 | 0.0000 | 0.0000 | TN=493 FP=0 FN=221 TP=0 |
| LR | 0.7048 | 0.6186 | 0.4381 | 0.3927 | 0.5770 | TN=416 FP=77 FN=134 TP=87 |
| LR_balanced | 0.6180 | 0.6025 | 0.4753 | 0.5615 | 0.4199 | TN=317 FP=176 FN=97 TP=124 |
| DT_balanced | 0.7353 | 0.6909 | 0.5552 | 0.5739 | 0.5547 | TN=398 FP=95 FN=94 TP=127 |
| RF_balanced_subsample | 0.7779 | 0.6786 | 0.5266 | 0.4181 | 0.7526 | TN=463 FP=30 FN=129 TP=92 |

## Split Mode

- mode: group
- group_key: pair_key
- n_groups: 110


## Best Model

- metric: f1_1(mean)
- best: DT_balanced
- f1_1_mean: 0.5552

## Top Features (fit on full data)

- kind: tree_importance

| rank | feature | score |
|---:|---|---:|
| 1 | ttk_adv | 0.284844 |
| 2 | d_ttk_est | 0.197812 |
| 3 | a_move_speed | 0.099229 |
| 4 | datk | 0.089126 |
| 5 | a_dps | 0.087221 |
| 6 | dmove_speed | 0.080878 |
| 7 | drange | 0.072314 |
| 8 | a_ttk_est | 0.062750 |
| 9 | dattack_speed | 0.024916 |
| 10 | d_dps | 0.000910 |
| 11 | a_attack_speed | 0.000000 |
| 12 | a_hp | 0.000000 |

## Threshold Tuning

- (not run)

## RF Grid Search

- (not run)
