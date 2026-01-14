# Baseline Eval (20260114)

## Data
- train: `datasets\train_experiments_v1.csv`
- test: `datasets\test_scenarios_v1.csv`
- train rows: 3200
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
- final_params: {"max_depth": 16, "max_features": "sqrt", "min_samples_leaf": 1, "min_samples_split": 10, "n_estimators": 800}
- tune_threshold: True (metric=recall)
- final_model: BEST

### Metrics / TEST (over repeats)
- acc       mean=0.6248 min=0.5641 max=0.7949
- bal_acc   mean=0.5974 min=0.5278 max=0.7778
- f1_1      mean=0.3331 min=0.1053 max=0.7805
- recall_1  mean=0.2407 min=0.0556 max=0.8889
- prec_1    mean=0.9090 min=0.6154 max=1.0000
- ap        mean=0.7425 min=0.5937 max=0.9016
- roc_auc   mean=0.7725 min=0.5622 max=0.9021
- thr       mean=0.0930 min=0.0500 max=0.2300

### Final Model (fit on FULL train)
- thr: 0.0700
- thr_repeats_mean: 0.0930
- thr_repeats_median: 0.0700
- test metrics:
  - acc: 0.5641
  - bal_acc: 0.5357
  - f1_1: 0.2609
  - recall_1: 0.1667
  - prec_1: 0.6000
  - ap: 0.7335
  - roc_auc: 0.8042

## Features
- num_features: 42
- feature_cols: start_distance, defender_count, a_level, a_hp, a_atk, a_cost, a_range, a_attack_speed, a_move_speed, a_hp_per_level, a_atk_per_level, d_level, d_hp, d_atk, d_cost, d_range, d_attack_speed, d_move_speed, d_hp_per_level, d_atk_per_level, a_perk_count, d_perk_count, a_has_perk_armor, a_has_perk_cleave, a_has_perk_duelist, a_has_perk_execute, a_has_perk_fury, a_has_perk_haste, a_has_perk_lifesteal, a_has_perk_longshot ...
