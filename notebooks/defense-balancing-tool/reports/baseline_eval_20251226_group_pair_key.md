# Baseline Evaluation Report
- generated_at: 2025-12-26T14:50:16
- input: datasets/battle_dataset_v1.csv
- rows: 2268
- usable_rows: 2268
- label_distribution: {0: 1901, 1: 367}
- test_ratio: 0.2
- seed: 42
- K(splits): 10

## Summary

| model | acc(mean) | bal_acc(mean) | f1_1(mean) | recall_1(mean) | precision_1(mean) | confusion_sum |
|---|---:|---:|---:|---:|---:|---|
| MAJORITY_SPLIT | 0.8427 | 0.5000 | 0.0000 | 0.0000 | 0.0000 | TN=3772 FP=0 FN=706 TP=0 |
| LR | 0.8309 | 0.5327 | 0.1529 | 0.0983 | 0.3659 | TN=3647 FP=125 FN=634 TP=72 |
| LR_balanced | 0.7306 | 0.7244 | 0.4542 | 0.7156 | 0.3359 | TN=2761 FP=1011 FN=197 TP=509 |
| DT_balanced | 0.9403 | 0.8884 | 0.8091 | 0.8123 | 0.8199 | TN=3636 FP=136 FN=135 TP=571 |
| RF_balanced_subsample | 0.8916 | 0.7102 | 0.5599 | 0.4454 | 0.8037 | TN=3677 FP=95 FN=391 TP=315 |

## Split Mode

- mode: group
- group_key: pair_key
- n_groups: 352


## Best Model

- metric: f1_1(mean)
- best: DT_balanced
- f1_1_mean: 0.8091

## Top Features (fit on full data)

- kind: tree_importance

| rank | feature | score |
|---:|---|---:|
| 1 | ttk_adv | 0.311752 |
| 2 | d_range | 0.155265 |
| 3 | a_move_speed | 0.125891 |
| 4 | dmove_speed | 0.107195 |
| 5 | d_move_speed | 0.087862 |
| 6 | range_adv | 0.036690 |
| 7 | dps_adv | 0.033706 |
| 8 | a_range | 0.033354 |
| 9 | a_ttk_est | 0.019285 |
| 10 | dattack_speed | 0.017541 |
| 11 | d_ttk_est | 0.012929 |
| 12 | dhp | 0.012322 |

## Threshold Tuning

- model: DT_balanced
- best_threshold: 0.95
- f1_1: 0.8117
- recall_1: 0.8088
- precision_1: 0.8146
- bal_acc: 0.8872
- cm_sum: TN=3642 FP=130 FN=135 TP=571

Top 5 thresholds by f1_1:

| rank | thr | f1_1 | recall_1 | precision_1 | bal_acc |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.95 | 0.8117 | 0.8088 | 0.8146 | 0.8872 |
| 2 | 0.05 | 0.8082 | 0.8088 | 0.8076 | 0.8864 |
| 3 | 0.10 | 0.8082 | 0.8088 | 0.8076 | 0.8864 |
| 4 | 0.15 | 0.8082 | 0.8088 | 0.8076 | 0.8864 |
| 5 | 0.20 | 0.8082 | 0.8088 | 0.8076 | 0.8864 |

## RF Grid Search

- tried_configs: 9
- best_params: n_estimators=200 max_depth=None min_samples_leaf=1 class_weight=balanced_subsample
- best_threshold: 0.30 f1_1=0.6960 recall_1=0.7620 precision_1=0.6405 bal_acc=0.8410 acc=0.8950
- cm_sum: TN=3470 FP=302 FN=168 TP=538

| rank | max_depth | min_samples_leaf | thr | f1_1 | recall_1 | precision_1 | bal_acc | acc |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | None | 1 | 0.30 | 0.6960 | 0.7620 | 0.6405 | 0.8410 | 0.8950 |
| 2 | None | 2 | 0.35 | 0.6894 | 0.7592 | 0.6313 | 0.8381 | 0.8921 |
| 3 | 12 | 2 | 0.40 | 0.6853 | 0.7450 | 0.6345 | 0.8324 | 0.8921 |
| 4 | None | 4 | 0.40 | 0.6830 | 0.7691 | 0.6143 | 0.8394 | 0.8874 |
| 5 | 12 | 4 | 0.45 | 0.6784 | 0.7365 | 0.6288 | 0.8276 | 0.8899 |
| 6 | 12 | 1 | 0.35 | 0.6777 | 0.7507 | 0.6177 | 0.8319 | 0.8874 |
| 7 | 8 | 4 | 0.45 | 0.6522 | 0.7861 | 0.5572 | 0.8346 | 0.8678 |
| 8 | 8 | 1 | 0.45 | 0.6512 | 0.7564 | 0.5717 | 0.8252 | 0.8723 |
