# Baseline Evaluation Report
- generated_at: 2025-12-24T18:18:14
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
| LR | 0.7221 | 0.5471 | 0.2366 | 0.2067 | 0.2892 | TN=659 FP=83 FN=190 TP=51 |
| LR_balanced | 0.6757 | 0.6355 | 0.4554 | 0.5650 | 0.3910 | TN=525 FP=217 FN=102 TP=139 |
| DT_balanced | 0.7883 | 0.6887 | 0.5367 | 0.4930 | 0.6174 | TN=656 FP=86 FN=122 TP=119 |
| RF_balanced_subsample | 0.7734 | 0.6309 | 0.4282 | 0.3521 | 0.5922 | TN=674 FP=68 FN=156 TP=85 |

## Split Mode

- mode: group
- group_key: pair_key
- n_groups: 234


## Best Model

- metric: f1_1(mean)
- best: DT_balanced
- f1_1_mean: 0.5367

## Top Features (fit on full data)

- kind: tree_importance

| rank | feature | score |
|---:|---|---:|
| 1 | d_ttk_est | 0.423604 |
| 2 | a_move_speed | 0.106561 |
| 3 | a_range | 0.088344 |
| 4 | a_atk | 0.079117 |
| 5 | drange | 0.050123 |
| 6 | d_range | 0.048011 |
| 7 | d_attack_speed | 0.046887 |
| 8 | a_dps | 0.042010 |
| 9 | a_attack_speed | 0.032362 |
| 10 | dmove_speed | 0.027212 |
| 11 | dattack_speed | 0.024310 |
| 12 | d_dps | 0.014746 |

## Threshold Tuning

- (not run)

## RF Grid Search

- (not run)
