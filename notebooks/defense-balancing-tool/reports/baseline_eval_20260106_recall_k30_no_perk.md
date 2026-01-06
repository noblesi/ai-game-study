# Baseline Eval (20260106)

## Data
- train: `datasets\train_experiments_v1.csv`
- test: `datasets\test_scenarios_v1.csv`
- train rows: 80
- test rows: 39
- train pos_rate: 0.0625
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
- final_params: {"max_depth": null, "max_features": "sqrt", "min_samples_leaf": 1, "min_samples_split": 10, "n_estimators": 400}
- tune_threshold: True (metric=recall)
- final_model: BEST

### Metrics / TEST (over repeats)
- acc       mean=0.5060 min=0.4103 max=0.6667
- bal_acc   mean=0.5258 min=0.4365 max=0.6746
- f1_1      mean=0.5722 min=0.0000 max=0.7083
- recall_1  mean=0.7833 min=0.0000 max=1.0000
- prec_1    mean=0.4733 min=0.0000 max=0.6087
- ap        mean=0.6906 min=0.5850 max=0.8244
- roc_auc   mean=0.6734 min=0.5542 max=0.7976
- thr       mean=0.1970 min=0.0600 max=0.4400

### Final Model (fit on FULL train)
- thr: 0.1650
- thr_repeats_mean: 0.1970
- thr_repeats_median: 0.1650
- test metrics:
  - acc: 0.4872
  - bal_acc: 0.5238
  - f1_1: 0.6429
  - recall_1: 1.0000
  - prec_1: 0.4737
  - ap: 0.6733
  - roc_auc: 0.6429

## Features
- num_features: 27
- feature_cols: start_distance, defender_count, a_level, a_hp, a_atk, a_cost, a_range, a_attack_speed, a_move_speed, a_hp_per_level, a_atk_per_level, d_level, d_hp, d_atk, d_cost, d_range, d_attack_speed, d_move_speed, d_hp_per_level, d_atk_per_level, a_dps, d_dps, a_ttk_est, d_ttk_est, dps_adv, range_adv, ttk_adv
