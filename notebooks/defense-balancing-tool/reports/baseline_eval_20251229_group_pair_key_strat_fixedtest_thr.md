# Baseline Eval (20251229)

## Data
- dataset: `datasets/battle_trials_v1.csv`
- rows: 14270
- label distribution: {0: 12010, 1: 2260}

## Split
- split_mode: group
- group_key: pair_key
- group_stratified: True (tries=300)
- fixed_test: True
- fixed_test_groups: 31
- fixed_test_pos_rate: 0.1581
- test_ratio: 0.2
- val_ratio: 0.2
- repeats: 20 (seed_base=42)

### test_pos_rate (label=1) / SPLIT
- mean=0.1581 min=0.1581 max=0.1581

## Majority Baseline (always=majority)
- majority_class: 0
- acc(all): 0.8416  bal_acc(all): 0.5000  f1_1(all): 0.0000

## Model: logreg
- class_weight: balanced
- C: 1.0
- tune_threshold: True (metric=recall)
- threshold stats: mean=0.234 min=0.050 max=0.880

### Metrics / TEST
- acc       mean=0.8533 min=0.7574 max=0.9559
- bal_acc   mean=0.8751 min=0.7035 max=0.9585
- f1_1      mean=0.6725 min=0.5429 max=0.8605
- recall_1  mean=0.9070 min=0.4419 max=1.0000
- prec_1    mean=0.5594 min=0.3905 max=0.8605
- ap        mean=0.8104 min=0.5901 max=0.9619
- roc_auc   mean=0.9571 min=0.9043 max=0.9913
- thr       mean=0.2340 min=0.0500 max=0.8800

### Confusion Matrix (sum over repeats)
- TN=38620 FP=7180 FN=800 TP=7800

## Features
- num_features: 60
- feature_cols: start_distance, defender_count, a_level, a_hp, a_atk, a_cost, a_range, a_attack_speed, a_move_speed, a_hp_per_level, a_atk_per_level, d_level, d_hp, d_atk, d_cost, d_range, d_attack_speed, d_move_speed, d_hp_per_level, d_atk_per_level, a_perk_count, d_perk_count, perk_count_adv, a_has_perk_armor, a_has_perk_cleave, a_has_perk_duelist, a_has_perk_execute, a_has_perk_fury, a_has_perk_haste, a_has_perk_lifesteal ...
