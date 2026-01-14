# Baseline Eval (20260114)

## Data
- train: `datasets/train_experiments_v1.csv`
- test: `datasets/test_scenarios_v1.csv`
- train rows: 3200
- test rows: 39
- train pos_rate: 0.0638
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
- acc       mean=0.5667 min=0.5385 max=0.6154
- bal_acc   mean=0.5306 min=0.5000 max=0.5833
- f1_1      mean=0.1107 min=0.0000 max=0.2857
- recall_1  mean=0.0611 min=0.0000 max=0.1667
- prec_1    mean=0.7000 min=0.0000 max=1.0000
- ap        mean=0.9535 min=0.8965 max=0.9889
- roc_auc   mean=0.9626 min=0.9220 max=0.9894
- thr       mean=0.2830 min=0.1600 max=0.4000

### Final Model (fit on FULL train)
- thr: 0.2900
- thr_repeats_mean: 0.2830
- thr_repeats_median: 0.2900
- test metrics:
  - acc: 0.5641
  - bal_acc: 0.5278
  - f1_1: 0.1053
  - recall_1: 0.0556
  - prec_1: 1.0000
  - ap: 0.9587
  - roc_auc: 0.9683

## Features
- num_features: 60
- feature_cols: start_distance, defender_count, a_level, a_hp, a_atk, a_cost, a_range, a_attack_speed, a_move_speed, a_hp_per_level, a_atk_per_level, d_level, d_hp, d_atk, d_cost, d_range, d_attack_speed, d_move_speed, d_hp_per_level, d_atk_per_level, a_perk_count, d_perk_count, perk_count_adv, a_has_perk_armor, a_has_perk_cleave, a_has_perk_duelist, a_has_perk_execute, a_has_perk_fury, a_has_perk_haste, a_has_perk_lifesteal ...
