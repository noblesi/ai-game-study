# Fixed Test Evaluation Report

- generated_at: 2025-12-26T14:13:47
- train: datasets/train_experiments_v1.csv
- test: datasets/test_scenarios_v1.csv
- train_rows: 2820 (usable=2820)
- test_rows: 78 (usable=78)
- group_key: pair_key_full

## Best Model

- best: DT_balanced
- threshold: 0.05

## Metrics

- acc: 1.0000
- bal_acc: 1.0000
- f1_1: 1.0000
- recall_1: 1.0000
- precision_1: 1.0000
- cm: TN=42 FP=0 FN=0 TP=36

## Confusion Matrix

| | pred=0 | pred=1 |
|---|---:|---:|
| true=0 | 42 | 0 |
| true=1 | 0 | 36 |

## Per-scenario predictions

| idx | title | pair_key | type | n | dist | y | pred | p1 | ok |
|---:|---|---|---|---:|---:|---:|---:|---:|:--:|
| 1 | D1: Knight vs Goblin (duel) | Knight__vs__Goblin__duel__x1 | duel | 1 | 5.0 | 1 | 1 | 1.0000 | ✅ |
| 2 | D2: Archer vs Runner (duel) | Archer__vs__Runner__duel__x1 | duel | 1 | 6.0 | 1 | 1 | 1.0000 | ✅ |
| 3 | D3: AntiAir Tower vs Wyvern (duel) | AntiAir Tower__vs__Wyvern__duel__x1 | duel | 1 | 7.0 | 1 | 1 | 1.0000 | ✅ |
| 4 | D4: Mage vs Armored Orc (duel) | Mage__vs__Armored Orc__duel__x1 | duel | 1 | 5.5 | 1 | 1 | 1.0000 | ✅ |
| 5 | D5: Tank vs Ogre Boss (duel) | Tank__vs__Ogre Boss__duel__x1 | duel | 1 | 4.5 | 0 | 0 | 0.0000 | ✅ |
| 6 | D6) Archer vs Runner (close start) | Archer__vs__Runner__duel__x1 | duel | 1 | 3.0 | 1 | 1 | 1.0000 | ✅ |
| 7 | D7) Archer vs Runner (far start) | Archer__vs__Runner__duel__x1 | duel | 1 | 9.0 | 1 | 1 | 1.0000 | ✅ |
| 8 | D8) Archer vs Goblin (mid start) | Archer__vs__Goblin__duel__x1 | duel | 1 | 6.0 | 1 | 1 | 1.0000 | ✅ |
| 9 | D9) Mage vs Runner (mid start) | Mage__vs__Runner__duel__x1 | duel | 1 | 6.0 | 1 | 1 | 1.0000 | ✅ |
| 10 | D10) Mage vs Runner (very far start) | Mage__vs__Runner__duel__x1 | duel | 1 | 10.0 | 1 | 1 | 1.0000 | ✅ |
| 11 | D11) Archer vs Dark Shaman (mid start) | Archer__vs__Dark Shaman__duel__x1 | duel | 1 | 6.0 | 1 | 1 | 1.0000 | ✅ |
| 12 | D12) Mage vs Dark Shaman (mid start) | Mage__vs__Dark Shaman__duel__x1 | duel | 1 | 6.0 | 1 | 1 | 1.0000 | ✅ |
| 13 | D13) Knight vs Dark Shaman (close start) | Knight__vs__Dark Shaman__duel__x1 | duel | 1 | 3.0 | 1 | 1 | 1.0000 | ✅ |
| 14 | D14) AntiAir vs Goblin (target mismatch sanity) | AntiAir Tower__vs__Goblin__duel__x1 | duel | 1 | 6.0 | 0 | 0 | 0.0000 | ✅ |
| 15 | D15) Mage vs Wyvern (target mismatch sanity) | Mage__vs__Wyvern__duel__x1 | duel | 1 | 6.0 | 0 | 0 | 0.0000 | ✅ |
| 16 | D16) AntiAir vs Dark Shaman (target mismatch sanity) | AntiAir Tower__vs__Dark Shaman__duel__x1 | duel | 1 | 6.0 | 0 | 0 | 0.0000 | ✅ |
| 17 | D17) Archer vs Wyvern (both target, far start) | Archer__vs__Wyvern__duel__x1 | duel | 1 | 8.0 | 1 | 1 | 1.0000 | ✅ |
| 18 | D18) Archer(Lv3) vs Runner(Lv3) | Archer__vs__Runner__duel__x1 | duel | 1 | 6.0 | 1 | 1 | 1.0000 | ✅ |
| 19 | D19) Archer(Lv6) vs Runner(Lv6) | Archer__vs__Runner__duel__x1 | duel | 1 | 6.0 | 1 | 1 | 1.0000 | ✅ |
| 20 | D20) Tank(Lv10) vs Ogre Boss(Lv10) | Tank__vs__Ogre Boss__duel__x1 | duel | 1 | 4.0 | 0 | 0 | 0.0000 | ✅ |
| 21 | D21) Mage(Lv10) vs Armored Orc(Lv10) (far start) | Mage__vs__Armored Orc__duel__x1 | duel | 1 | 8.0 | 1 | 1 | 1.0000 | ✅ |
| 22 | D22) AntiAir(Lv6) vs Wyvern(Lv6) (very far start) | AntiAir Tower__vs__Wyvern__duel__x1 | duel | 1 | 10.0 | 1 | 1 | 1.0000 | ✅ |
| 23 | D23) Archer vs Ogre Boss (very far start) | Archer__vs__Ogre Boss__duel__x1 | duel | 1 | 10.0 | 0 | 0 | 0.0000 | ✅ |
| 24 | D24) Mage vs Ogre Boss (far start) | Mage__vs__Ogre Boss__duel__x1 | duel | 1 | 8.0 | 0 | 0 | 0.0000 | ✅ |
| 25 | D25) Tank vs Dark Shaman (ranged enemy check) | Tank__vs__Dark Shaman__duel__x1 | duel | 1 | 7.0 | 1 | 1 | 1.0000 | ✅ |
| 26 | S1: Knight vs Goblin x4 (swarm) | Knight__vs__Goblin x4__swarm__x4 | swarm | 4 | 5.0 | 0 | 0 | 0.0000 | ✅ |
| 27 | S2: AntiAir Tower vs Wyvern x3 (swarm) | AntiAir Tower__vs__Wyvern x3__swarm__x3 | swarm | 3 | 7.0 | 0 | 0 | 0.0000 | ✅ |
| 28 | S3: Mage vs Runner x5 (swarm) | Mage__vs__Runner x5__swarm__x5 | swarm | 5 | 6.0 | 0 | 0 | 0.0000 | ✅ |
| 29 | S4: Archer vs Goblin x6 (swarm) | Archer__vs__Goblin x6__swarm__x6 | swarm | 6 | 7.0 | 0 | 0 | 0.0000 | ✅ |
| 30 | S5: Tank vs Goblin x8 (swarm) | Tank__vs__Goblin x8__swarm__x8 | swarm | 8 | 5.5 | 0 | 0 | 0.0000 | ✅ |
| 31 | S6) Archer vs Goblin Swarm x3 | Archer__vs__Goblin x3__swarm__x3 | swarm | 3 | 7.0 | 0 | 0 | 0.0000 | ✅ |
| 32 | S7) Mage vs Goblin Swarm x5 | Mage__vs__Goblin x5__swarm__x5 | swarm | 5 | 7.0 | 0 | 0 | 0.0000 | ✅ |
| 33 | S8) Knight vs Runner Swarm x4 | Knight__vs__Runner x4__swarm__x4 | swarm | 4 | 6.0 | 0 | 0 | 0.0000 | ✅ |
| 34 | S9) AntiAir vs Wyvern Swarm x3 | AntiAir Tower__vs__Wyvern x3__swarm__x3 | swarm | 3 | 8.0 | 0 | 0 | 0.0000 | ✅ |
| 35 | S10) AntiAir vs Goblin Swarm x4 (target mismatch sanity) | AntiAir Tower__vs__Goblin x4__swarm__x4 | swarm | 4 | 7.0 | 0 | 0 | 0.0000 | ✅ |
| 36 | S11) Archer vs Wyvern Swarm x4 | Archer__vs__Wyvern x4__swarm__x4 | swarm | 4 | 9.0 | 0 | 0 | 0.0000 | ✅ |
| 37 | S12) Mage vs Wyvern Swarm x2 (target mismatch sanity) | Mage__vs__Wyvern x2__swarm__x2 | swarm | 2 | 7.0 | 0 | 0 | 0.0000 | ✅ |
| 38 | S13) Tank vs Dark Shaman Swarm x2 | Tank__vs__Dark Shaman x2__swarm__x2 | swarm | 2 | 8.0 | 0 | 0 | 0.0000 | ✅ |
| 39 | S14) Archer(Lv6) vs Runner(Lv6) Swarm x5 | Archer__vs__Runner x5__swarm__x5 | swarm | 5 | 8.0 | 0 | 0 | 0.0000 | ✅ |
| 40 | D1: Knight vs Goblin (duel) | Knight__vs__Goblin__duel__x1 | duel | 1 | 5.0 | 1 | 1 | 1.0000 | ✅ |
| 41 | D2: Archer vs Runner (duel) | Archer__vs__Runner__duel__x1 | duel | 1 | 6.0 | 1 | 1 | 1.0000 | ✅ |
| 42 | D3: AntiAir Tower vs Wyvern (duel) | AntiAir Tower__vs__Wyvern__duel__x1 | duel | 1 | 7.0 | 1 | 1 | 1.0000 | ✅ |
| 43 | D4: Mage vs Armored Orc (duel) | Mage__vs__Armored Orc__duel__x1 | duel | 1 | 5.5 | 1 | 1 | 1.0000 | ✅ |
| 44 | D5: Tank vs Ogre Boss (duel) | Tank__vs__Ogre Boss__duel__x1 | duel | 1 | 4.5 | 0 | 0 | 0.0000 | ✅ |
| 45 | D6) Archer vs Runner (close start) | Archer__vs__Runner__duel__x1 | duel | 1 | 3.0 | 1 | 1 | 1.0000 | ✅ |
| 46 | D7) Archer vs Runner (far start) | Archer__vs__Runner__duel__x1 | duel | 1 | 9.0 | 1 | 1 | 1.0000 | ✅ |
| 47 | D8) Archer vs Goblin (mid start) | Archer__vs__Goblin__duel__x1 | duel | 1 | 6.0 | 1 | 1 | 1.0000 | ✅ |
| 48 | D9) Mage vs Runner (mid start) | Mage__vs__Runner__duel__x1 | duel | 1 | 6.0 | 1 | 1 | 1.0000 | ✅ |
| 49 | D10) Mage vs Runner (very far start) | Mage__vs__Runner__duel__x1 | duel | 1 | 10.0 | 1 | 1 | 1.0000 | ✅ |
| 50 | D11) Archer vs Dark Shaman (mid start) | Archer__vs__Dark Shaman__duel__x1 | duel | 1 | 6.0 | 1 | 1 | 1.0000 | ✅ |
| 51 | D12) Mage vs Dark Shaman (mid start) | Mage__vs__Dark Shaman__duel__x1 | duel | 1 | 6.0 | 1 | 1 | 1.0000 | ✅ |
| 52 | D13) Knight vs Dark Shaman (close start) | Knight__vs__Dark Shaman__duel__x1 | duel | 1 | 3.0 | 1 | 1 | 1.0000 | ✅ |
| 53 | D14) AntiAir vs Goblin (target mismatch sanity) | AntiAir Tower__vs__Goblin__duel__x1 | duel | 1 | 6.0 | 0 | 0 | 0.0000 | ✅ |
| 54 | D15) Mage vs Wyvern (target mismatch sanity) | Mage__vs__Wyvern__duel__x1 | duel | 1 | 6.0 | 0 | 0 | 0.0000 | ✅ |
| 55 | D16) AntiAir vs Dark Shaman (target mismatch sanity) | AntiAir Tower__vs__Dark Shaman__duel__x1 | duel | 1 | 6.0 | 0 | 0 | 0.0000 | ✅ |
| 56 | D17) Archer vs Wyvern (both target, far start) | Archer__vs__Wyvern__duel__x1 | duel | 1 | 8.0 | 1 | 1 | 1.0000 | ✅ |
| 57 | D18) Archer(Lv3) vs Runner(Lv3) | Archer__vs__Runner__duel__x1 | duel | 1 | 6.0 | 1 | 1 | 1.0000 | ✅ |
| 58 | D19) Archer(Lv6) vs Runner(Lv6) | Archer__vs__Runner__duel__x1 | duel | 1 | 6.0 | 1 | 1 | 1.0000 | ✅ |
| 59 | D20) Tank(Lv10) vs Ogre Boss(Lv10) | Tank__vs__Ogre Boss__duel__x1 | duel | 1 | 4.0 | 0 | 0 | 0.0000 | ✅ |
| 60 | D21) Mage(Lv10) vs Armored Orc(Lv10) (far start) | Mage__vs__Armored Orc__duel__x1 | duel | 1 | 8.0 | 1 | 1 | 1.0000 | ✅ |
| 61 | D22) AntiAir(Lv6) vs Wyvern(Lv6) (very far start) | AntiAir Tower__vs__Wyvern__duel__x1 | duel | 1 | 10.0 | 1 | 1 | 1.0000 | ✅ |
| 62 | D23) Archer vs Ogre Boss (very far start) | Archer__vs__Ogre Boss__duel__x1 | duel | 1 | 10.0 | 0 | 0 | 0.0000 | ✅ |
| 63 | D24) Mage vs Ogre Boss (far start) | Mage__vs__Ogre Boss__duel__x1 | duel | 1 | 8.0 | 0 | 0 | 0.0000 | ✅ |
| 64 | D25) Tank vs Dark Shaman (ranged enemy check) | Tank__vs__Dark Shaman__duel__x1 | duel | 1 | 7.0 | 1 | 1 | 1.0000 | ✅ |
| 65 | S1: Knight vs Goblin x4 (swarm) | Knight__vs__Goblin x4__swarm__x4 | swarm | 4 | 5.0 | 0 | 0 | 0.0000 | ✅ |
| 66 | S2: AntiAir Tower vs Wyvern x3 (swarm) | AntiAir Tower__vs__Wyvern x3__swarm__x3 | swarm | 3 | 7.0 | 0 | 0 | 0.0000 | ✅ |
| 67 | S3: Mage vs Runner x5 (swarm) | Mage__vs__Runner x5__swarm__x5 | swarm | 5 | 6.0 | 0 | 0 | 0.0000 | ✅ |
| 68 | S4: Archer vs Goblin x6 (swarm) | Archer__vs__Goblin x6__swarm__x6 | swarm | 6 | 7.0 | 0 | 0 | 0.0000 | ✅ |
| 69 | S5: Tank vs Goblin x8 (swarm) | Tank__vs__Goblin x8__swarm__x8 | swarm | 8 | 5.5 | 0 | 0 | 0.0000 | ✅ |
| 70 | S6) Archer vs Goblin Swarm x3 | Archer__vs__Goblin x3__swarm__x3 | swarm | 3 | 7.0 | 0 | 0 | 0.0000 | ✅ |
| 71 | S7) Mage vs Goblin Swarm x5 | Mage__vs__Goblin x5__swarm__x5 | swarm | 5 | 7.0 | 0 | 0 | 0.0000 | ✅ |
| 72 | S8) Knight vs Runner Swarm x4 | Knight__vs__Runner x4__swarm__x4 | swarm | 4 | 6.0 | 0 | 0 | 0.0000 | ✅ |
| 73 | S9) AntiAir vs Wyvern Swarm x3 | AntiAir Tower__vs__Wyvern x3__swarm__x3 | swarm | 3 | 8.0 | 0 | 0 | 0.0000 | ✅ |
| 74 | S10) AntiAir vs Goblin Swarm x4 (target mismatch sanity) | AntiAir Tower__vs__Goblin x4__swarm__x4 | swarm | 4 | 7.0 | 0 | 0 | 0.0000 | ✅ |
| 75 | S11) Archer vs Wyvern Swarm x4 | Archer__vs__Wyvern x4__swarm__x4 | swarm | 4 | 9.0 | 0 | 0 | 0.0000 | ✅ |
| 76 | S12) Mage vs Wyvern Swarm x2 (target mismatch sanity) | Mage__vs__Wyvern x2__swarm__x2 | swarm | 2 | 7.0 | 0 | 0 | 0.0000 | ✅ |
| 77 | S13) Tank vs Dark Shaman Swarm x2 | Tank__vs__Dark Shaman x2__swarm__x2 | swarm | 2 | 8.0 | 0 | 0 | 0.0000 | ✅ |
| 78 | S14) Archer(Lv6) vs Runner(Lv6) Swarm x5 | Archer__vs__Runner x5__swarm__x5 | swarm | 5 | 8.0 | 0 | 0 | 0.0000 | ✅ |

## Errors only

- (none)
