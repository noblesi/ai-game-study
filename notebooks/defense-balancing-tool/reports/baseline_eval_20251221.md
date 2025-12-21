# Baseline Evaluation Report
- generated_at: 2025-12-21T18:22:59
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
| MAJORITY_SPLIT | 0.6575 | 0.5000 | 0.0000 | 0.0000 | 0.0000 | TN=496 FP=0 FN=258 TP=0 |
| LR | 0.6834 | 0.6475 | 0.4699 | 0.4559 | 0.5598 | TN=417 FP=79 FN=160 TP=98 |
| LR_balanced | 0.6530 | 0.6698 | 0.5573 | 0.7068 | 0.4825 | TN=316 FP=180 FN=81 TP=177 |
| DT_balanced | 0.7198 | 0.7163 | 0.5921 | 0.6666 | 0.5770 | TN=378 FP=118 FN=94 TP=164 |
| RF_balanced_subsample | 0.7613 | 0.7197 | 0.5988 | 0.5640 | 0.6908 | TN=433 FP=63 FN=117 TP=141 |

## Split Mode

- mode: group
- group_key: pair_key
- n_groups: 112


## Best Model

- metric: f1_1(mean)
- best: RF_balanced_subsample
- f1_1_mean: 0.5988

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
