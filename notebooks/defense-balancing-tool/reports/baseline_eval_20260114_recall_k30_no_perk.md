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
- acc       mean=0.8556 min=0.5897 max=0.9231
- bal_acc   mean=0.8574 min=0.5556 max=0.9286
- f1_1      mean=0.8182 min=0.2000 max=0.9231
- recall_1  mean=0.8815 min=0.1111 max=1.0000
- prec_1    mean=0.8422 min=0.7200 max=1.0000
- ap        mean=0.9710 min=0.9106 max=0.9881
- roc_auc   mean=0.9758 min=0.9365 max=0.9894
- thr       mean=0.1010 min=0.0500 max=0.2900

### Final Model (fit on FULL train)
- thr: 0.0900
- thr_repeats_mean: 0.1010
- thr_repeats_median: 0.0900
- test metrics:
  - acc: 0.8974
  - bal_acc: 0.9008
  - f1_1: 0.8947
  - recall_1: 0.9444
  - prec_1: 0.8500
  - ap: 0.9835
  - roc_auc: 0.9841

## Features
- num_features: 27
- feature_cols: start_distance, defender_count, a_level, a_hp, a_atk, a_cost, a_range, a_attack_speed, a_move_speed, a_hp_per_level, a_atk_per_level, d_level, d_hp, d_atk, d_cost, d_range, d_attack_speed, d_move_speed, d_hp_per_level, d_atk_per_level, a_dps, d_dps, a_ttk_est, d_ttk_est, dps_adv, range_adv, ttk_adv
