# Fixed Test Evaluation Report

- generated_at: 2025-12-28T20:07:19
- train: datasets/train_experiments_v1.csv
- test: datasets/test_scenarios_v1.csv
- train_rows: 1800 (usable=1800)
- test_rows: 39 (usable=12)
- group_key: pair_key
- dropped_overlap_groups: 27

## Best Model

- best: LR_balanced
- threshold: 0.10

## Metrics

- acc: 0.7500
- bal_acc: 0.8333
- f1_1: 0.6667
- recall_1: 1.0000
- precision_1: 0.5000
- cm: TN=6 FP=3 FN=0 TP=3

## Confusion Matrix

| | pred=0 | pred=1 |
|---|---:|---:|
| true=0 | 6 | 3 |
| true=1 | 0 | 3 |

## Per-scenario predictions

| idx | title | pair_key | type | n | dist | y | pred | p1 | ok |
|---:|---|---|---|---:|---:|---:|---:|---:|:--:|
| 1 | D4: Mage vs Armored Orc (duel) | Mage__vs__Armored Orc__duel__x1 | duel | 1 | 5.5 | 1 | 1 | 0.1939 | ✅ |
| 2 | D12) Mage vs Dark Shaman (mid start) | Mage__vs__Dark Shaman__duel__x1 | duel | 1 | 6.0 | 1 | 1 | 0.3143 | ✅ |
| 3 | D21) Mage(Lv10) vs Armored Orc(Lv10) (far start) | Mage__vs__Armored Orc__duel__x1 | duel | 1 | 8.0 | 1 | 1 | 0.9432 | ✅ |
| 4 | S1: Knight vs Goblin x4 (swarm) | Knight__vs__Goblin x4__swarm__x4 | swarm | 4 | 5.0 | 0 | 1 | 0.1678 | ❌ |
| 5 | S4: Archer vs Goblin x6 (swarm) | Archer__vs__Goblin x6__swarm__x6 | swarm | 6 | 7.0 | 0 | 0 | 0.0309 | ✅ |
| 6 | S7) Mage vs Goblin Swarm x5 | Mage__vs__Goblin x5__swarm__x5 | swarm | 5 | 7.0 | 0 | 0 | 0.0759 | ✅ |
| 7 | S8) Knight vs Runner Swarm x4 | Knight__vs__Runner x4__swarm__x4 | swarm | 4 | 6.0 | 0 | 1 | 0.1755 | ❌ |
| 8 | S10) AntiAir vs Goblin Swarm x4 (target mismatch sanity) | AntiAir Tower__vs__Goblin x4__swarm__x4 | swarm | 4 | 7.0 | 0 | 0 | 0.0152 | ✅ |
| 9 | S11) Archer vs Wyvern Swarm x4 | Archer__vs__Wyvern x4__swarm__x4 | swarm | 4 | 9.0 | 0 | 0 | 0.0067 | ✅ |
| 10 | S12) Mage vs Wyvern Swarm x2 (target mismatch sanity) | Mage__vs__Wyvern x2__swarm__x2 | swarm | 2 | 7.0 | 0 | 0 | 0.0236 | ✅ |
| 11 | S13) Tank vs Dark Shaman Swarm x2 | Tank__vs__Dark Shaman x2__swarm__x2 | swarm | 2 | 8.0 | 0 | 0 | 0.0546 | ✅ |
| 12 | S14) Archer(Lv6) vs Runner(Lv6) Swarm x5 | Archer__vs__Runner x5__swarm__x5 | swarm | 5 | 8.0 | 0 | 1 | 0.3292 | ❌ |

## Errors only

- S1: Knight vs Goblin x4 (swarm) / pair=Knight__vs__Goblin x4__swarm__x4 y=0 pred=1 p1=0.1678
- S8) Knight vs Runner Swarm x4 / pair=Knight__vs__Runner x4__swarm__x4 y=0 pred=1 p1=0.1755
- S14) Archer(Lv6) vs Runner(Lv6) Swarm x5 / pair=Archer__vs__Runner x5__swarm__x5 y=0 pred=1 p1=0.3292
