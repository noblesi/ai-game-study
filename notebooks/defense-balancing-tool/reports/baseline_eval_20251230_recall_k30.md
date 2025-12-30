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
- group_stratified: True (tries=300)
- val_ratio: 0.2
- repeats: 30 (seed_base=42)

## Model
- kind: rf
- class_weight: balanced
- rf_grid: True (candidates=12)
- final_params: {"max_depth": 10, "max_features": "sqrt", "min_samples_leaf": 1, "min_samples_split": 10, "n_estimators": 400}
- tune_threshold: True (metric=recall)
- final_model: BEST

### Metrics / TEST (over repeats)
- acc       mean=0.7342 min=0.5385 max=0.9231
- bal_acc   mean=0.7299 min=0.5000 max=0.9286
- f1_1      mean=0.5933 min=0.0000 max=0.9231
- recall_1  mean=0.6741 min=0.0000 max=1.0000
- prec_1    mean=0.5939 min=0.0000 max=1.0000
- ap        mean=0.9122 min=0.8087 max=0.9616
- roc_auc   mean=0.9399 min=0.8915 max=0.9656
- thr       mean=0.1613 min=0.0500 max=0.4400

### Final Model (fit on FULL train)
- thr: 0.1400
- thr_repeats_mean: 0.1613
- thr_repeats_median: 0.1400
- test metrics:
  - acc: 0.8718
  - bal_acc: 0.8810
  - f1_1: 0.8780
  - recall_1: 1.0000
  - prec_1: 0.7826
  - ap: 0.9800
  - roc_auc: 0.9815

## Features
- num_features: 60
- feature_cols: start_distance, defender_count, a_level, a_hp, a_atk, a_cost, a_range, a_attack_speed, a_move_speed, a_hp_per_level, a_atk_per_level, d_level, d_hp, d_atk, d_cost, d_range, d_attack_speed, d_move_speed, d_hp_per_level, d_atk_per_level, a_perk_count, d_perk_count, perk_count_adv, a_has_perk_armor, a_has_perk_cleave, a_has_perk_duelist, a_has_perk_execute, a_has_perk_fury, a_has_perk_haste, a_has_perk_lifesteal ...
