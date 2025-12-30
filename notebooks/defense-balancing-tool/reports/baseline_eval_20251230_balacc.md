# Baseline Eval (20251230)

## Data
- train: `datasets/train_experiments_v1.csv`
- test: `datasets/test_scenarios_v1.csv`
- train rows: 1200
- test rows: 39
- train pos_rate: 0.0567
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
- tune_threshold: True (metric=bal_acc)
- final_model: BEST

### Metrics / TEST (over repeats)
- acc       mean=0.7692 min=0.5385 max=0.9231
- bal_acc   mean=0.7567 min=0.5000 max=0.9286
- f1_1      mean=0.5734 min=0.0000 max=0.9231
- recall_1  mean=0.5944 min=0.0000 max=1.0000
- prec_1    mean=0.6173 min=0.0000 max=1.0000
- ap        mean=0.8927 min=0.8103 max=0.9507
- roc_auc   mean=0.9247 min=0.8571 max=0.9643
- thr       mean=0.1940 min=0.0900 max=0.4400

### Final Model (fit on FULL train)
- thr: 0.1500
- thr_repeats_mean: 0.1940
- thr_repeats_median: 0.1500
- test metrics:
  - acc: 0.6923
  - bal_acc: 0.6706
  - f1_1: 0.5385
  - recall_1: 0.3889
  - prec_1: 0.8750
  - ap: 0.9197
  - roc_auc: 0.9484

## Features
- num_features: 60
- feature_cols: start_distance, defender_count, a_level, a_hp, a_atk, a_cost, a_range, a_attack_speed, a_move_speed, a_hp_per_level, a_atk_per_level, d_level, d_hp, d_atk, d_cost, d_range, d_attack_speed, d_move_speed, d_hp_per_level, d_atk_per_level, a_perk_count, d_perk_count, perk_count_adv, a_has_perk_armor, a_has_perk_cleave, a_has_perk_duelist, a_has_perk_execute, a_has_perk_fury, a_has_perk_haste, a_has_perk_lifesteal ...
