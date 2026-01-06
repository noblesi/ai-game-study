# Baseline Eval (20260106)

## Data
- train: `datasets/train_experiments_v1.csv`
- test: `datasets/test_scenarios_v1.csv`
- train rows: 80
- test rows: 39
- train pos_rate: 0.0625
- test pos_rate: 0.4615
- overlap groups: 0 (dropped train rows=0)

## Split
- split_mode: group (train->val only)
- group_key: pair_key_full
- group_stratified: True (tries=200)
- val_ratio: 0.2
- repeats: 10 (seed_base=42)

## Model
- kind: rf
- class_weight: balanced
- rf_grid: True (candidates=12)
- final_params: {"max_depth": null, "max_features": "sqrt", "min_samples_leaf": 1, "min_samples_split": 2, "n_estimators": 400}
- tune_threshold: True (metric=f1)
- final_model: BEST

### Metrics / TEST (over repeats)
- acc       mean=0.5410 min=0.4872 max=0.6667
- bal_acc   mean=0.5540 min=0.5000 max=0.6627
- f1_1      mean=0.5139 min=0.0000 max=0.6667
- recall_1  mean=0.7222 min=0.0000 max=1.0000
- prec_1    mean=0.4133 min=0.0000 max=0.6471
- ap        mean=0.7246 min=0.6530 max=0.8657
- roc_auc   mean=0.7610 min=0.6614 max=0.8849
- thr       mean=0.1780 min=0.0800 max=0.3100

### Final Model (fit on FULL train)
- thr: 0.1650
- thr_repeats_mean: 0.1780
- thr_repeats_median: 0.1650
- test metrics:
  - acc: 0.5897
  - bal_acc: 0.5556
  - f1_1: 0.2000
  - recall_1: 0.1111
  - prec_1: 1.0000
  - ap: 0.7417
  - roc_auc: 0.8095

## Features
- num_features: 60
- feature_cols: start_distance, defender_count, a_level, a_hp, a_atk, a_cost, a_range, a_attack_speed, a_move_speed, a_hp_per_level, a_atk_per_level, d_level, d_hp, d_atk, d_cost, d_range, d_attack_speed, d_move_speed, d_hp_per_level, d_atk_per_level, a_perk_count, d_perk_count, perk_count_adv, a_has_perk_armor, a_has_perk_cleave, a_has_perk_duelist, a_has_perk_execute, a_has_perk_fury, a_has_perk_haste, a_has_perk_lifesteal ...
