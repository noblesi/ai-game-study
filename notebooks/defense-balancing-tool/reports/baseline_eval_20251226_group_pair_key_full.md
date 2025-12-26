# Baseline Evaluation Report
- generated_at: 2025-12-26T14:13:47
- input: datasets/battle_dataset_v1.csv
- rows: 2820
- usable_rows: 2820
- label_distribution: {0: 2351, 1: 469}
- test_ratio: 0.2
- seed: 42
- K(splits): 10

## Summary

| model | acc(mean) | bal_acc(mean) | f1_1(mean) | recall_1(mean) | precision_1(mean) | confusion_sum |
|---|---:|---:|---:|---:|---:|---|
| MAJORITY_SPLIT | 0.8311 | 0.5000 | 0.0000 | 0.0000 | 0.0000 | TN=4642 FP=0 FN=944 TP=0 |
| LR | 0.8321 | 0.5963 | 0.3246 | 0.2402 | 0.5087 | TN=4421 FP=221 FN=717 TP=227 |
| LR_balanced | 0.7389 | 0.7515 | 0.4992 | 0.7706 | 0.3700 | TN=3399 FP=1243 FN=216 TP=728 |
| DT_balanced | 0.9720 | 0.9401 | 0.9136 | 0.8923 | 0.9387 | TN=4586 FP=56 FN=100 TP=844 |
| RF_balanced_subsample | 0.9461 | 0.8585 | 0.8170 | 0.7264 | 0.9411 | TN=4599 FP=43 FN=258 TP=686 |

## Split Mode

- mode: group
- group_key: pair_key_full
- n_groups: 2554


## Best Model

- metric: f1_1(mean)
- best: DT_balanced
- f1_1_mean: 0.9136

## Top Features (fit on full data)

- kind: tree_importance

| rank | feature | score |
|---:|---|---:|
| 1 | ttk_adv | 0.336512 |
| 2 | dmove_speed | 0.250669 |
| 3 | d_range | 0.139456 |
| 4 | a_move_speed | 0.085276 |
| 5 | a_range | 0.039337 |
| 6 | d_move_speed | 0.028098 |
| 7 | d_attack_speed | 0.027086 |
| 8 | dps_adv | 0.016218 |
| 9 | start_distance | 0.015931 |
| 10 | d_ttk_est | 0.013620 |
| 11 | range_adv | 0.009748 |
| 12 | a_attack_speed | 0.008521 |

## Threshold Tuning

- model: DT_balanced
- best_threshold: 0.05
- f1_1: 0.9154
- recall_1: 0.8941
- precision_1: 0.9378
- bal_acc: 0.9410
- cm_sum: TN=4586 FP=56 FN=100 TP=844

Top 5 thresholds by f1_1:

| rank | thr | f1_1 | recall_1 | precision_1 | bal_acc |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.05 | 0.9154 | 0.8941 | 0.9378 | 0.9410 |
| 2 | 0.10 | 0.9154 | 0.8941 | 0.9378 | 0.9410 |
| 3 | 0.15 | 0.9154 | 0.8941 | 0.9378 | 0.9410 |
| 4 | 0.20 | 0.9154 | 0.8941 | 0.9378 | 0.9410 |
| 5 | 0.25 | 0.9154 | 0.8941 | 0.9378 | 0.9410 |

## RF Grid Search

- tried_configs: 9
- best_params: n_estimators=200 max_depth=None min_samples_leaf=1 class_weight=balanced_subsample
- best_threshold: 0.40 f1_1=0.8553 recall_1=0.8231 precision_1=0.8900 bal_acc=0.9012 acc=0.9529
- cm_sum: TN=4546 FP=96 FN=167 TP=777

| rank | max_depth | min_samples_leaf | thr | f1_1 | recall_1 | precision_1 | bal_acc | acc |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | None | 1 | 0.40 | 0.8553 | 0.8231 | 0.8900 | 0.9012 | 0.9529 |
| 2 | None | 2 | 0.40 | 0.8534 | 0.8665 | 0.8407 | 0.9166 | 0.9497 |
| 3 | None | 4 | 0.45 | 0.8355 | 0.8771 | 0.7977 | 0.9159 | 0.9416 |
| 4 | 12 | 1 | 0.45 | 0.8328 | 0.8284 | 0.8373 | 0.8978 | 0.9438 |
| 5 | 12 | 2 | 0.45 | 0.8296 | 0.8485 | 0.8116 | 0.9042 | 0.9411 |
| 6 | 12 | 4 | 0.45 | 0.8193 | 0.8814 | 0.7654 | 0.9132 | 0.9343 |
| 7 | 8 | 2 | 0.55 | 0.7815 | 0.8051 | 0.7592 | 0.8766 | 0.9239 |
| 8 | 8 | 4 | 0.55 | 0.7812 | 0.8210 | 0.7452 | 0.8819 | 0.9223 |
