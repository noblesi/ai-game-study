# Baseline Evaluation Report
- generated_at: 2025-12-22T21:49:59
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
| 1 | ttk_adv | 0.126880 |
| 2 | dmove_speed | 0.092602 |
| 3 | a_dps | 0.072386 |
| 4 | d_ttk_est | 0.067191 |
| 5 | dps_adv | 0.063607 |
| 6 | dhp | 0.058786 |
| 7 | datk | 0.054503 |
| 8 | a_ttk_est | 0.051106 |
| 9 | a_move_speed | 0.047773 |
| 10 | a_atk | 0.040394 |
| 11 | a_attack_speed | 0.031880 |
| 12 | drange | 0.031251 |

## Threshold Tuning

- model: RF_balanced_subsample
- best_threshold: 0.40
- f1_1: 0.5656
- recall_1: 0.6161
- precision_1: 0.5227
- bal_acc: 0.6871
- cm_sum: TN=395 FP=126 FN=86 TP=138

Top 5 thresholds by f1_1:

| rank | thr | f1_1 | recall_1 | precision_1 | bal_acc |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.40 | 0.5656 | 0.6161 | 0.5227 | 0.6871 |
| 2 | 0.45 | 0.5442 | 0.5357 | 0.5530 | 0.6748 |
| 3 | 0.50 | 0.5351 | 0.4598 | 0.6398 | 0.6742 |
| 4 | 0.35 | 0.5311 | 0.6295 | 0.4593 | 0.6554 |
| 5 | 0.30 | 0.5283 | 0.6875 | 0.4290 | 0.6470 |

## RF Grid Search

- tried_configs: 9
- best_params: n_estimators=200 max_depth=12 min_samples_leaf=2 class_weight=balanced_subsample
- best_threshold: 0.40 f1_1=0.5656 recall_1=0.6161 precision_1=0.5227 bal_acc=0.6871 acc=0.7154
- cm_sum: TN=395 FP=126 FN=86 TP=138

| rank | max_depth | min_samples_leaf | thr | f1_1 | recall_1 | precision_1 | bal_acc | acc |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 12 | 2 | 0.40 | 0.5656 | 0.6161 | 0.5227 | 0.6871 | 0.7154 |
| 2 | None | 2 | 0.40 | 0.5621 | 0.6161 | 0.5169 | 0.6842 | 0.7114 |
| 3 | 8 | 1 | 0.40 | 0.5565 | 0.5938 | 0.5236 | 0.6808 | 0.7154 |
| 4 | 8 | 2 | 0.50 | 0.5536 | 0.4955 | 0.6271 | 0.6844 | 0.7597 |
| 5 | 8 | 4 | 0.45 | 0.5534 | 0.5670 | 0.5404 | 0.6798 | 0.7248 |
| 6 | None | 4 | 0.45 | 0.5511 | 0.5536 | 0.5487 | 0.6789 | 0.7289 |
| 7 | 12 | 4 | 0.45 | 0.5511 | 0.5536 | 0.5487 | 0.6789 | 0.7289 |
| 8 | 12 | 1 | 0.40 | 0.5500 | 0.5893 | 0.5156 | 0.6756 | 0.7101 |
