# Baseline Eval (20260101)

## Data
- train: `datasets\train_experiments_v1.csv`
- test: `datasets\test_scenarios_v1.csv`
- train rows: 1600
- test rows: 39
- train pos_rate: 0.0638
- test pos_rate: 0.4615
- overlap groups: 0 (dropped train rows=0)

## Split
- split_mode: group (train->val only)
- group_key: pair_key_full
- group_stratified: True (tries=300)
- val_ratio: 0.2
- repeats: 30 (seed_base=42)

## Model
- kind: rf
- class_weight: balanced
- rf_grid: True (candidates=12)
- final_params: {"max_depth": null, "max_features": "sqrt", "min_samples_leaf": 1, "min_samples_split": 10, "n_estimators": 800}
- tune_threshold: True (metric=recall)
- final_model: BEST

### Metrics / TEST (over repeats)
- acc       mean=0.8402 min=0.5641 max=0.9487
- bal_acc   mean=0.8368 min=0.5278 max=0.9444
- f1_1      mean=0.7821 min=0.1053 max=0.9412
- recall_1  mean=0.7926 min=0.0556 max=1.0000
- prec_1    mean=0.8805 min=0.6667 max=1.0000
- ap        mean=0.9585 min=0.9135 max=0.9857
- roc_auc   mean=0.9653 min=0.9365 max=0.9868
- thr       mean=0.1137 min=0.0500 max=0.3100

### Final Model (fit on FULL train)
- thr: 0.1000
- thr_repeats_mean: 0.1137
- thr_repeats_median: 0.1000
- test metrics:
  - acc: 0.9231
  - bal_acc: 0.9286
  - f1_1: 0.9231
  - recall_1: 1.0000
  - prec_1: 0.8571
  - ap: 0.9837
  - roc_auc: 0.9841

## Features
- num_features: 60
- feature_cols: start_distance, defender_count, a_level, a_hp, a_atk, a_cost, a_range, a_attack_speed, a_move_speed, a_hp_per_level, a_atk_per_level, d_level, d_hp, d_atk, d_cost, d_range, d_attack_speed, d_move_speed, d_hp_per_level, d_atk_per_level, a_perk_count, d_perk_count, perk_count_adv, a_has_perk_armor, a_has_perk_cleave, a_has_perk_duelist, a_has_perk_execute, a_has_perk_fury, a_has_perk_haste, a_has_perk_lifesteal ...
