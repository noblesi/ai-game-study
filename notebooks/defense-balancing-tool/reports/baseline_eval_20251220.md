# Baseline Evaluation Report
- generated_at: 2025-12-20T19:47:13
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
| MAJORITY_SPLIT | 0.6959 | 0.5000 | 0.0000 | 0.0000 | 0.0000 | TN=508 FP=0 FN=222 TP=0 |
| LR | 0.7329 | 0.6655 | 0.5301 | 0.4930 | 0.5959 | TN=426 FP=82 FN=113 TP=109 |
| LR_balanced | 0.6616 | 0.6687 | 0.5534 | 0.6921 | 0.4636 | TN=329 FP=179 FN=68 TP=154 |
| DT_balanced | 0.9986 | 0.9991 | 0.9976 | 1.0000 | 0.9952 | TN=507 FP=1 FN=0 TP=222 |
| RF_balanced_subsample | 0.9945 | 0.9939 | 0.9921 | 0.9897 | 0.9952 | TN=507 FP=1 FN=3 TP=219 |

## Best Model

- metric: f1_1(mean)
- best: DT_balanced
- f1_1_mean: 0.9976

## Top Features (fit on full data)

- kind: tree_importance

| rank | feature | score |
|---:|---|---:|
| 1 | ttk_adv | 0.254596 |
| 2 | d_ttk_est | 0.184094 |
| 3 | a_move_speed | 0.122569 |
| 4 | datk | 0.106957 |
| 5 | a_dps | 0.090796 |
| 6 | dmove_speed | 0.079173 |
| 7 | drange | 0.068869 |
| 8 | a_ttk_est | 0.066928 |
| 9 | range_adv | 0.025069 |
| 10 | dhp | 0.000949 |
| 11 | d_move_speed | 0.000000 |
| 12 | d_range | 0.000000 |
