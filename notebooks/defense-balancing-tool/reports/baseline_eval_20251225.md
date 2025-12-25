# Baseline Evaluation Report
- generated_at: 2025-12-25T18:32:33
- input: datasets/battle_dataset_v1.csv
- rows: 438
- usable_rows: 438
- label_distribution: {1: 146, 0: 292}
- test_ratio: 0.2
- seed: 42
- K(splits): 10

## Summary

| model | acc(mean) | bal_acc(mean) | f1_1(mean) | recall_1(mean) | precision_1(mean) | confusion_sum |
|---|---:|---:|---:|---:|---:|---|
| MAJORITY_SPLIT | 0.6805 | 0.5000 | 0.0000 | 0.0000 | 0.0000 | TN=592 FP=0 FN=278 TP=0 |
| LR | 0.7966 | 0.7493 | 0.6581 | 0.6156 | 0.7110 | TN=523 FP=69 FN=108 TP=170 |
| LR_balanced | 0.7460 | 0.7407 | 0.6416 | 0.7235 | 0.5807 | TN=449 FP=143 FN=78 TP=200 |
| DT_balanced | 0.9908 | 0.9934 | 0.9844 | 1.0000 | 0.9699 | TN=584 FP=8 FN=0 TP=278 |
| RF_balanced_subsample | 0.9943 | 0.9958 | 0.9905 | 1.0000 | 0.9814 | TN=587 FP=5 FN=0 TP=278 |

## Split Mode

- mode: random


## Best Model

- metric: f1_1(mean)
- best: RF_balanced_subsample
- f1_1_mean: 0.9905

## Top Features (fit on full data)

- kind: tree_importance

| rank | feature | score |
|---:|---|---:|
| 1 | ttk_adv | 0.137386 |
| 2 | dmove_speed | 0.083176 |
| 3 | dps_adv | 0.073060 |
| 4 | a_ttk_est | 0.070682 |
| 5 | d_ttk_est | 0.067384 |
| 6 | datk | 0.060781 |
| 7 | dhp | 0.059911 |
| 8 | a_dps | 0.055936 |
| 9 | a_move_speed | 0.051830 |
| 10 | d_move_speed | 0.029545 |
| 11 | d_hp | 0.028846 |
| 12 | d_range | 0.028356 |

## Threshold Tuning

- (not run)

## RF Grid Search

- (not run)
