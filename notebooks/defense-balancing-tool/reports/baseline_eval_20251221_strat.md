# Baseline Evaluation Report
- generated_at: 2025-12-21T19:59:03
- input: datasets/battle_dataset_v1.csv
- rows: 367
- usable_rows: 367
- label_distribution: {1: 115, 0: 252}
- test_ratio: 0.2
- seed: 42
- K(splits): 10

## Summary

| model | acc(mean) | bal_acc(mean) | f1_1(mean) | recall_1(mean) | precision_1(mean) | confusion_sum |
|---|---:|---:|---:|---:|---:|---|
| MAJORITY_SPLIT | 0.6994 | 0.5000 | 0.0000 | 0.0000 | 0.0000 | TN=521 FP=0 FN=224 TP=0 |
| LR | 0.6800 | 0.6047 | 0.4246 | 0.4218 | 0.4654 | TN=411 FP=110 FN=128 TP=96 |
| LR_balanced | 0.6358 | 0.6243 | 0.4916 | 0.6029 | 0.4327 | TN=336 FP=185 FN=87 TP=137 |
| DT_balanced | 0.6655 | 0.6137 | 0.4607 | 0.4850 | 0.4505 | TN=387 FP=134 FN=114 TP=110 |
| RF_balanced_subsample | 0.7503 | 0.6659 | 0.5079 | 0.4539 | 0.6396 | TN=458 FP=63 FN=122 TP=102 |

## Split Mode

- mode: group
- group_key: pair_key
- n_groups: 112


## Best Model

- metric: f1_1(mean)
- best: RF_balanced_subsample
- f1_1_mean: 0.5079

## Top Features (fit on full data)

- kind: tree_importance

| rank | feature | score |
|---:|---|---:|
| 1 | ttk_adv | 0.123518 |
| 2 | dmove_speed | 0.090387 |
| 3 | a_dps | 0.068735 |
| 4 | d_ttk_est | 0.067422 |
| 5 | dps_adv | 0.062674 |
| 6 | dhp | 0.061417 |
| 7 | datk | 0.055254 |
| 8 | a_ttk_est | 0.054227 |
| 9 | a_move_speed | 0.048420 |
| 10 | a_atk | 0.040984 |
| 11 | a_attack_speed | 0.031343 |
| 12 | dattack_speed | 0.029861 |
