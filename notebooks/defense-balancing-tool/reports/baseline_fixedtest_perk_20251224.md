# Fixed Test Evaluation Report

- generated_at: 2025-12-24T23:13:21
- train: datasets/experiments_v2.csv
- test: datasets/scenarios_v2.csv
- train_rows: 498 (usable=498)
- test_rows: 78 (usable=12)
- group_key: pair_key
- dropped_overlap_groups: 66

## Best Model

- best: DT_balanced
- threshold: 0.01

## Metrics

- acc: 1.0000
- bal_acc: 0.5000
- f1_1: 0.0000
- recall_1: 0.0000
- precision_1: 0.0000
- cm: TN=12 FP=0 FN=0 TP=0

## Confusion Matrix

| | pred=0 | pred=1 |
|---|---:|---:|
| true=0 | 12 | 0 |
| true=1 | 0 | 0 |

## Per-scenario predictions

| idx | title | pair_key | type | n | dist | y | pred | p1 | ok |
|---:|---|---|---|---:|---:|---:|---:|---:|:--:|
| 1 | S5: Tank vs Goblin x8 (swarm) | Tank__vs__Goblin x8__swarm__x8 | swarm | 8 | 5.5 | 0 | 0 | 0.0000 | ✅ |
| 2 | S8) Knight vs Runner Swarm x4 | Knight__vs__Runner x4__swarm__x4 | swarm | 4 | 6.0 | 0 | 0 | 0.0000 | ✅ |
| 3 | S10) AntiAir vs Goblin Swarm x4 (target mismatch sanity) | AntiAir Tower__vs__Goblin x4__swarm__x4 | swarm | 4 | 7.0 | 0 | 0 | 0.0000 | ✅ |
| 4 | S11) Archer vs Wyvern Swarm x4 | Archer__vs__Wyvern x4__swarm__x4 | swarm | 4 | 9.0 | 0 | 0 | 0.0000 | ✅ |
| 5 | S12) Mage vs Wyvern Swarm x2 (target mismatch sanity) | Mage__vs__Wyvern x2__swarm__x2 | swarm | 2 | 7.0 | 0 | 0 | 0.0000 | ✅ |
| 6 | S13) Tank vs Dark Shaman Swarm x2 | Tank__vs__Dark Shaman x2__swarm__x2 | swarm | 2 | 8.0 | 0 | 0 | 0.0000 | ✅ |
| 7 | S5: Tank vs Goblin x8 (swarm) | Tank__vs__Goblin x8__swarm__x8 | swarm | 8 | 5.5 | 0 | 0 | 0.0000 | ✅ |
| 8 | S8) Knight vs Runner Swarm x4 | Knight__vs__Runner x4__swarm__x4 | swarm | 4 | 6.0 | 0 | 0 | 0.0000 | ✅ |
| 9 | S10) AntiAir vs Goblin Swarm x4 (target mismatch sanity) | AntiAir Tower__vs__Goblin x4__swarm__x4 | swarm | 4 | 7.0 | 0 | 0 | 0.0000 | ✅ |
| 10 | S11) Archer vs Wyvern Swarm x4 | Archer__vs__Wyvern x4__swarm__x4 | swarm | 4 | 9.0 | 0 | 0 | 0.0000 | ✅ |
| 11 | S12) Mage vs Wyvern Swarm x2 (target mismatch sanity) | Mage__vs__Wyvern x2__swarm__x2 | swarm | 2 | 7.0 | 0 | 0 | 0.0000 | ✅ |
| 12 | S13) Tank vs Dark Shaman Swarm x2 | Tank__vs__Dark Shaman x2__swarm__x2 | swarm | 2 | 8.0 | 0 | 0 | 0.0000 | ✅ |

## Errors only

- (none)
