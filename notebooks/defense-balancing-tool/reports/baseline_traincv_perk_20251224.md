# Baseline Evaluation Report
- generated_at: 2025-12-24T23:13:21
- input: datasets/battle_dataset_v1.csv
- rows: 498
- usable_rows: 498
- label_distribution: {1: 123, 0: 375}
- test_ratio: 0.2
- seed: 42
- K(splits): 10

## Summary

| model | acc(mean) | bal_acc(mean) | f1_1(mean) | recall_1(mean) | precision_1(mean) | confusion_sum |
|---|---:|---:|---:|---:|---:|---|
| MAJORITY_SPLIT | 0.7538 | 0.5000 | 0.0000 | 0.0000 | 0.0000 | TN=742 FP=0 FN=241 TP=0 |
| LR | 0.7339 | 0.5681 | 0.3011 | 0.2443 | 0.4765 | TN=662 FP=80 FN=182 TP=59 |
| LR_balanced | 0.6823 | 0.6501 | 0.4754 | 0.5951 | 0.4072 | TN=524 FP=218 FN=95 TP=146 |
| DT_balanced | 0.7900 | 0.7031 | 0.5569 | 0.5309 | 0.6005 | TN=650 FP=92 FN=114 TP=127 |
| RF_balanced_subsample | 0.7763 | 0.6438 | 0.4553 | 0.3821 | 0.5814 | TN=671 FP=71 FN=150 TP=91 |

## Split Mode

- mode: group
- group_key: pair_key
- n_groups: 234


## Best Model

- metric: f1_1(mean)
- best: DT_balanced
- f1_1_mean: 0.5569

## Top Features (fit on full data)

- kind: tree_importance

| rank | feature | score |
|---:|---|---:|
| 1 | encounter_is_swarm | 0.407766 |
| 2 | dhp | 0.130872 |
| 3 | d_attack_speed | 0.088344 |
| 4 | d_ttk_est | 0.050123 |
| 5 | ttk_adv | 0.047203 |
| 6 | d_range | 0.043668 |
| 7 | range_adv | 0.040801 |
| 8 | a_ttk_est | 0.036735 |
| 9 | dmove_speed | 0.032394 |
| 10 | dps_adv | 0.032362 |
| 11 | datk | 0.032342 |
| 12 | defender_count | 0.030331 |

## Threshold Tuning

- model: DT_balanced
- best_threshold: 0.01
- f1_1: 0.5522
- recall_1: 0.5270
- precision_1: 0.5799
- bal_acc: 0.7015
- cm_sum: TN=650 FP=92 FN=114 TP=127

Top 5 thresholds by f1_1:

| rank | thr | f1_1 | recall_1 | precision_1 | bal_acc |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.01 | 0.5522 | 0.5270 | 0.5799 | 0.7015 |
| 2 | 0.02 | 0.5522 | 0.5270 | 0.5799 | 0.7015 |
| 3 | 0.03 | 0.5522 | 0.5270 | 0.5799 | 0.7015 |
| 4 | 0.04 | 0.5522 | 0.5270 | 0.5799 | 0.7015 |
| 5 | 0.05 | 0.5522 | 0.5270 | 0.5799 | 0.7015 |

## RF Grid Search

- (not run)
