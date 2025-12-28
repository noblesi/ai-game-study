# Fixed Test Evaluation Report

- generated_at: 2025-12-28T18:28:29
- train: datasets/train_experiments_v1.csv
- test: datasets/test_scenarios_v1.csv
- train_rows: 120 (usable=120)
- test_rows: 39 (usable=39)
- group_key: pair_key_full

## Best Model

- best: LR_balanced
- threshold: 0.50

## Metrics

- acc: 0.5641
- bal_acc: 0.5278
- f1_1: 0.1053
- recall_1: 0.0556
- precision_1: 1.0000
- cm: TN=21 FP=0 FN=17 TP=1

## Confusion Matrix

| | pred=0 | pred=1 |
|---|---:|---:|
| true=0 | 21 | 0 |
| true=1 | 17 | 1 |

## Per-scenario predictions

| idx | title | pair_key | type | n | dist | y | pred | p1 | ok |
|---:|---|---|---|---:|---:|---:|---:|---:|:--:|
| 1 | D1: Knight vs Goblin (duel) | Knight__vs__Goblin__duel__x1 | duel | 1 | 5.0 | 1 | 0 | 0.0334 | ❌ |
| 2 | D2: Archer vs Runner (duel) | Archer__vs__Runner__duel__x1 | duel | 1 | 6.0 | 1 | 0 | 0.0043 | ❌ |
| 3 | D3: AntiAir Tower vs Wyvern (duel) | AntiAir Tower__vs__Wyvern__duel__x1 | duel | 1 | 7.0 | 1 | 0 | 0.0043 | ❌ |
| 4 | D4: Mage vs Armored Orc (duel) | Mage__vs__Armored Orc__duel__x1 | duel | 1 | 5.5 | 1 | 0 | 0.0766 | ❌ |
| 5 | D5: Tank vs Ogre Boss (duel) | Tank__vs__Ogre Boss__duel__x1 | duel | 1 | 4.5 | 0 | 0 | 0.1600 | ✅ |
| 6 | D6) Archer vs Runner (close start) | Archer__vs__Runner__duel__x1 | duel | 1 | 3.0 | 1 | 0 | 0.0083 | ❌ |
| 7 | D7) Archer vs Runner (far start) | Archer__vs__Runner__duel__x1 | duel | 1 | 9.0 | 1 | 0 | 0.0022 | ❌ |
| 8 | D8) Archer vs Goblin (mid start) | Archer__vs__Goblin__duel__x1 | duel | 1 | 6.0 | 1 | 0 | 0.0118 | ❌ |
| 9 | D9) Mage vs Runner (mid start) | Mage__vs__Runner__duel__x1 | duel | 1 | 6.0 | 1 | 0 | 0.0037 | ❌ |
| 10 | D10) Mage vs Runner (very far start) | Mage__vs__Runner__duel__x1 | duel | 1 | 10.0 | 1 | 0 | 0.0015 | ❌ |
| 11 | D11) Archer vs Dark Shaman (mid start) | Archer__vs__Dark Shaman__duel__x1 | duel | 1 | 6.0 | 1 | 0 | 0.1332 | ❌ |
| 12 | D12) Mage vs Dark Shaman (mid start) | Mage__vs__Dark Shaman__duel__x1 | duel | 1 | 6.0 | 1 | 0 | 0.1240 | ❌ |
| 13 | D13) Knight vs Dark Shaman (close start) | Knight__vs__Dark Shaman__duel__x1 | duel | 1 | 3.0 | 1 | 0 | 0.3694 | ❌ |
| 14 | D14) AntiAir vs Goblin (target mismatch sanity) | AntiAir Tower__vs__Goblin__duel__x1 | duel | 1 | 6.0 | 0 | 0 | 0.0060 | ✅ |
| 15 | D15) Mage vs Wyvern (target mismatch sanity) | Mage__vs__Wyvern__duel__x1 | duel | 1 | 6.0 | 0 | 0 | 0.0102 | ✅ |
| 16 | D16) AntiAir vs Dark Shaman (target mismatch sanity) | AntiAir Tower__vs__Dark Shaman__duel__x1 | duel | 1 | 6.0 | 0 | 0 | 0.0689 | ✅ |
| 17 | D17) Archer vs Wyvern (both target, far start) | Archer__vs__Wyvern__duel__x1 | duel | 1 | 8.0 | 1 | 0 | 0.0071 | ❌ |
| 18 | D18) Archer(Lv3) vs Runner(Lv3) | Archer__vs__Runner__duel__x1 | duel | 1 | 6.0 | 1 | 0 | 0.0094 | ❌ |
| 19 | D19) Archer(Lv6) vs Runner(Lv6) | Archer__vs__Runner__duel__x1 | duel | 1 | 6.0 | 1 | 0 | 0.0311 | ❌ |
| 20 | D20) Tank(Lv10) vs Ogre Boss(Lv10) | Tank__vs__Ogre Boss__duel__x1 | duel | 1 | 4.0 | 0 | 0 | 0.0676 | ✅ |
| 21 | D21) Mage(Lv10) vs Armored Orc(Lv10) (far start) | Mage__vs__Armored Orc__duel__x1 | duel | 1 | 8.0 | 1 | 1 | 0.5122 | ✅ |
| 22 | D22) AntiAir(Lv6) vs Wyvern(Lv6) (very far start) | AntiAir Tower__vs__Wyvern__duel__x1 | duel | 1 | 10.0 | 1 | 0 | 0.0097 | ❌ |
| 23 | D23) Archer vs Ogre Boss (very far start) | Archer__vs__Ogre Boss__duel__x1 | duel | 1 | 10.0 | 0 | 0 | 0.0378 | ✅ |
| 24 | D24) Mage vs Ogre Boss (far start) | Mage__vs__Ogre Boss__duel__x1 | duel | 1 | 8.0 | 0 | 0 | 0.0521 | ✅ |
| 25 | D25) Tank vs Dark Shaman (ranged enemy check) | Tank__vs__Dark Shaman__duel__x1 | duel | 1 | 7.0 | 1 | 0 | 0.1368 | ❌ |
| 26 | S1: Knight vs Goblin x4 (swarm) | Knight__vs__Goblin x4__swarm__x4 | swarm | 4 | 5.0 | 0 | 0 | 0.0151 | ✅ |
| 27 | S2: AntiAir Tower vs Wyvern x3 (swarm) | AntiAir Tower__vs__Wyvern x3__swarm__x3 | swarm | 3 | 7.0 | 0 | 0 | 0.0022 | ✅ |
| 28 | S3: Mage vs Runner x5 (swarm) | Mage__vs__Runner x5__swarm__x5 | swarm | 5 | 6.0 | 0 | 0 | 0.0040 | ✅ |
| 29 | S4: Archer vs Goblin x6 (swarm) | Archer__vs__Goblin x6__swarm__x6 | swarm | 6 | 7.0 | 0 | 0 | 0.0106 | ✅ |
| 30 | S5: Tank vs Goblin x8 (swarm) | Tank__vs__Goblin x8__swarm__x8 | swarm | 8 | 5.5 | 0 | 0 | 0.0094 | ✅ |
| 31 | S6) Archer vs Goblin Swarm x3 | Archer__vs__Goblin x3__swarm__x3 | swarm | 3 | 7.0 | 0 | 0 | 0.0055 | ✅ |
| 32 | S7) Mage vs Goblin Swarm x5 | Mage__vs__Goblin x5__swarm__x5 | swarm | 5 | 7.0 | 0 | 0 | 0.0082 | ✅ |
| 33 | S8) Knight vs Runner Swarm x4 | Knight__vs__Runner x4__swarm__x4 | swarm | 4 | 6.0 | 0 | 0 | 0.0046 | ✅ |
| 34 | S9) AntiAir vs Wyvern Swarm x3 | AntiAir Tower__vs__Wyvern x3__swarm__x3 | swarm | 3 | 8.0 | 0 | 0 | 0.0017 | ✅ |
| 35 | S10) AntiAir vs Goblin Swarm x4 (target mismatch sanity) | AntiAir Tower__vs__Goblin x4__swarm__x4 | swarm | 4 | 7.0 | 0 | 0 | 0.0030 | ✅ |
| 36 | S11) Archer vs Wyvern Swarm x4 | Archer__vs__Wyvern x4__swarm__x4 | swarm | 4 | 9.0 | 0 | 0 | 0.0034 | ✅ |
| 37 | S12) Mage vs Wyvern Swarm x2 (target mismatch sanity) | Mage__vs__Wyvern x2__swarm__x2 | swarm | 2 | 7.0 | 0 | 0 | 0.0047 | ✅ |
| 38 | S13) Tank vs Dark Shaman Swarm x2 | Tank__vs__Dark Shaman x2__swarm__x2 | swarm | 2 | 8.0 | 0 | 0 | 0.0339 | ✅ |
| 39 | S14) Archer(Lv6) vs Runner(Lv6) Swarm x5 | Archer__vs__Runner x5__swarm__x5 | swarm | 5 | 8.0 | 0 | 0 | 0.0054 | ✅ |

## Errors only

- D1: Knight vs Goblin (duel) / pair=Knight__vs__Goblin__duel__x1 y=1 pred=0 p1=0.0334
- D2: Archer vs Runner (duel) / pair=Archer__vs__Runner__duel__x1 y=1 pred=0 p1=0.0043
- D3: AntiAir Tower vs Wyvern (duel) / pair=AntiAir Tower__vs__Wyvern__duel__x1 y=1 pred=0 p1=0.0043
- D4: Mage vs Armored Orc (duel) / pair=Mage__vs__Armored Orc__duel__x1 y=1 pred=0 p1=0.0766
- D6) Archer vs Runner (close start) / pair=Archer__vs__Runner__duel__x1 y=1 pred=0 p1=0.0083
- D7) Archer vs Runner (far start) / pair=Archer__vs__Runner__duel__x1 y=1 pred=0 p1=0.0022
- D8) Archer vs Goblin (mid start) / pair=Archer__vs__Goblin__duel__x1 y=1 pred=0 p1=0.0118
- D9) Mage vs Runner (mid start) / pair=Mage__vs__Runner__duel__x1 y=1 pred=0 p1=0.0037
- D10) Mage vs Runner (very far start) / pair=Mage__vs__Runner__duel__x1 y=1 pred=0 p1=0.0015
- D11) Archer vs Dark Shaman (mid start) / pair=Archer__vs__Dark Shaman__duel__x1 y=1 pred=0 p1=0.1332
- D12) Mage vs Dark Shaman (mid start) / pair=Mage__vs__Dark Shaman__duel__x1 y=1 pred=0 p1=0.124
- D13) Knight vs Dark Shaman (close start) / pair=Knight__vs__Dark Shaman__duel__x1 y=1 pred=0 p1=0.3694
- D17) Archer vs Wyvern (both target, far start) / pair=Archer__vs__Wyvern__duel__x1 y=1 pred=0 p1=0.0071
- D18) Archer(Lv3) vs Runner(Lv3) / pair=Archer__vs__Runner__duel__x1 y=1 pred=0 p1=0.0094
- D19) Archer(Lv6) vs Runner(Lv6) / pair=Archer__vs__Runner__duel__x1 y=1 pred=0 p1=0.0311
- D22) AntiAir(Lv6) vs Wyvern(Lv6) (very far start) / pair=AntiAir Tower__vs__Wyvern__duel__x1 y=1 pred=0 p1=0.0097
- D25) Tank vs Dark Shaman (ranged enemy check) / pair=Tank__vs__Dark Shaman__duel__x1 y=1 pred=0 p1=0.1368
