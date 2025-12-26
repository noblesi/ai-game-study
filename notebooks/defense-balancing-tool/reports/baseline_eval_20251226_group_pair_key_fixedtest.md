# Fixed Test Evaluation Report

- generated_at: 2025-12-26T14:50:16
- train: datasets/train_experiments_train_by_pair.csv
- test: datasets/holdout_by_pair.csv
- train_rows: 2268 (usable=2268)
- test_rows: 552 (usable=552)
- group_key: pair_key

## Best Model

- best: DT_balanced
- threshold: 0.95

## Metrics

- acc: 0.9130
- bal_acc: 0.8822
- f1_1: 0.7798
- recall_1: 0.8333
- precision_1: 0.7328
- cm: TN=419 FP=31 FN=17 TP=85

## Confusion Matrix

| | pred=0 | pred=1 |
|---|---:|---:|
| true=0 | 419 | 31 |
| true=1 | 17 | 85 |

## Per-scenario predictions

| idx | title | pair_key | type | n | dist | y | pred | p1 | ok |
|---:|---|---|---|---:|---:|---:|---:|---:|:--:|
| 1 |  | Wyvern__vs__Mage x8__swarm__x8 | swarm | 8 | 10.59359441092269 | 1 | 1 | 1.0000 | ✅ |
| 2 |  | Wyvern__vs__Mage x8__swarm__x8 | swarm | 8 | 11.540668887969726 | 1 | 1 | 1.0000 | ✅ |
| 3 |  | Wyvern__vs__Mage x8__swarm__x8 | swarm | 8 | 16.105726603028177 | 1 | 1 | 1.0000 | ✅ |
| 4 |  | Wyvern__vs__Mage x8__swarm__x8 | swarm | 8 | 7.817157991120579 | 0 | 1 | 1.0000 | ❌ |
| 5 |  | Wyvern__vs__Mage x8__swarm__x8 | swarm | 8 | 3.72496167283235 | 0 | 0 | 0.0000 | ✅ |
| 6 |  | Wyvern__vs__Mage x8__swarm__x8 | swarm | 8 | 10.435715871920978 | 1 | 1 | 1.0000 | ✅ |
| 7 |  | Armored Orc__vs__Runner__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 8 |  | Armored Orc__vs__Runner__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 9 |  | Armored Orc__vs__Runner__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 10 |  | Armored Orc__vs__Runner__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 11 |  | Armored Orc__vs__Runner__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 12 |  | Armored Orc__vs__Runner__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 13 |  | Armored Orc__vs__Runner__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 14 |  | Armored Orc__vs__Runner__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 15 |  | Armored Orc__vs__Runner__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 16 |  | Armored Orc__vs__Runner__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 17 |  | Armored Orc__vs__Runner__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 18 |  | Ogre Boss__vs__Dark Shaman x3__swarm__x3 | swarm | 3 | 7.618785143439653 | 0 | 0 | 0.0000 | ✅ |
| 19 |  | Ogre Boss__vs__Dark Shaman x3__swarm__x3 | swarm | 3 | 8.93273885327248 | 0 | 0 | 0.0000 | ✅ |
| 20 |  | Ogre Boss__vs__Dark Shaman x3__swarm__x3 | swarm | 3 | 6.12137493820054 | 0 | 0 | 0.0000 | ✅ |
| 21 |  | Ogre Boss__vs__Dark Shaman x3__swarm__x3 | swarm | 3 | 4.7299567190204215 | 0 | 0 | 0.0000 | ✅ |
| 22 |  | Runner__vs__Mage x5__swarm__x5 | swarm | 5 | 5.0 | 0 | 0 | 0.0000 | ✅ |
| 23 |  | Runner__vs__Mage x5__swarm__x5 | swarm | 5 | 12.931733942370048 | 0 | 0 | 0.0000 | ✅ |
| 24 |  | Runner__vs__Mage x5__swarm__x5 | swarm | 5 | 13.69419072963402 | 0 | 0 | 0.0000 | ✅ |
| 25 |  | Runner__vs__Mage x5__swarm__x5 | swarm | 5 | 10.554802075730716 | 0 | 0 | 0.0000 | ✅ |
| 26 |  | Goblin__vs__Runner x8__swarm__x8 | swarm | 8 | 6.354914692089346 | 0 | 0 | 0.0000 | ✅ |
| 27 |  | Goblin__vs__Runner x8__swarm__x8 | swarm | 8 | 2.259112086257232 | 0 | 0 | 0.0000 | ✅ |
| 28 |  | Goblin__vs__Runner x8__swarm__x8 | swarm | 8 | 16.605148115774753 | 0 | 0 | 0.0000 | ✅ |
| 29 |  | Goblin__vs__Runner x8__swarm__x8 | swarm | 8 | 13.746866172419093 | 0 | 0 | 0.0000 | ✅ |
| 30 |  | Goblin__vs__Runner x8__swarm__x8 | swarm | 8 | 8.6724609948762 | 0 | 0 | 0.0000 | ✅ |
| 31 |  | Goblin__vs__Runner x8__swarm__x8 | swarm | 8 | 10.07374718239871 | 0 | 0 | 0.0000 | ✅ |
| 32 |  | Runner__vs__Goblin__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 33 |  | Runner__vs__Goblin__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 34 |  | Runner__vs__Goblin__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 35 |  | Runner__vs__Goblin__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 36 |  | Runner__vs__Goblin__duel__x1 | duel | 1 | 5.0 | 0 | 0 | 0.0000 | ✅ |
| 37 |  | Runner__vs__Goblin__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 38 |  | Runner__vs__Goblin__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 39 |  | Runner__vs__Goblin__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 40 |  | Runner__vs__Goblin__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 41 |  | Runner__vs__Goblin__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 42 |  | Runner__vs__Goblin__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 43 |  | Runner__vs__Goblin__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 44 |  | Runner__vs__Goblin__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 45 |  | Goblin__vs__Runner x5__swarm__x5 | swarm | 5 | 12.796323870114087 | 0 | 0 | 0.0000 | ✅ |
| 46 |  | Goblin__vs__Runner x5__swarm__x5 | swarm | 5 | 5.309922736972592 | 0 | 0 | 0.0000 | ✅ |
| 47 |  | Goblin__vs__Runner x5__swarm__x5 | swarm | 5 | 12.143310369403915 | 0 | 0 | 0.0000 | ✅ |
| 48 |  | Goblin__vs__Runner x5__swarm__x5 | swarm | 5 | 2.97633535000665 | 0 | 0 | 0.0000 | ✅ |
| 49 |  | Goblin__vs__Runner x5__swarm__x5 | swarm | 5 | 8.246017308044696 | 0 | 0 | 0.0000 | ✅ |
| 50 |  | Mage__vs__AntiAir Tower x8__swarm__x8 | swarm | 8 | 12.969802846974499 | 0 | 0 | 0.0000 | ✅ |
| 51 |  | Mage__vs__AntiAir Tower x8__swarm__x8 | swarm | 8 | 12.659091381598147 | 0 | 0 | 0.0000 | ✅ |
| 52 |  | Mage__vs__AntiAir Tower x8__swarm__x8 | swarm | 8 | 12.952782169206168 | 0 | 0 | 0.0000 | ✅ |
| 53 |  | Archer__vs__Dark Shaman x3__swarm__x3 | swarm | 3 | 11.457556780629668 | 0 | 0 | 0.0000 | ✅ |
| 54 |  | Archer__vs__Dark Shaman x3__swarm__x3 | swarm | 3 | 7.238579524134991 | 0 | 0 | 0.0000 | ✅ |
| 55 |  | Archer__vs__Dark Shaman x3__swarm__x3 | swarm | 3 | 12.19356240055976 | 0 | 0 | 0.0000 | ✅ |
| 56 |  | Archer__vs__Dark Shaman x3__swarm__x3 | swarm | 3 | 10.627902695058891 | 0 | 0 | 0.0000 | ✅ |
| 57 |  | Archer__vs__Dark Shaman x3__swarm__x3 | swarm | 3 | 7.372833705890338 | 0 | 0 | 0.0000 | ✅ |
| 58 |  | Archer__vs__Dark Shaman x3__swarm__x3 | swarm | 3 | 7.515561280128781 | 0 | 0 | 0.0000 | ✅ |
| 59 |  | AntiAir Tower__vs__Goblin x3__swarm__x3 | swarm | 3 | 4.5957849674372175 | 0 | 0 | 0.0000 | ✅ |
| 60 |  | AntiAir Tower__vs__Goblin x3__swarm__x3 | swarm | 3 | 12.547410623616464 | 0 | 0 | 0.0000 | ✅ |
| 61 |  | AntiAir Tower__vs__Goblin x3__swarm__x3 | swarm | 3 | 7.572530183501185 | 0 | 0 | 0.0000 | ✅ |
| 62 |  | AntiAir Tower__vs__Goblin x3__swarm__x3 | swarm | 3 | 10.427992298346018 | 0 | 0 | 0.0000 | ✅ |
| 63 |  | AntiAir Tower__vs__Goblin x3__swarm__x3 | swarm | 3 | 3.465938971330426 | 0 | 0 | 0.0000 | ✅ |
| 64 |  | AntiAir Tower__vs__Goblin x3__swarm__x3 | swarm | 3 | 2.7461654847182584 | 0 | 0 | 0.0000 | ✅ |
| 65 |  | Goblin__vs__Archer__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 66 |  | Goblin__vs__Archer__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 67 |  | Goblin__vs__Archer__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 68 |  | Goblin__vs__Archer__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 69 |  | Goblin__vs__Archer__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 70 |  | Goblin__vs__Archer__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 71 |  | Goblin__vs__Archer__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 72 |  | Goblin__vs__Archer__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 73 |  | Goblin__vs__Archer__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 74 |  | Goblin__vs__Archer__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 75 |  | Knight__vs__Dark Shaman__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 76 |  | Knight__vs__Dark Shaman__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 77 |  | Knight__vs__Dark Shaman__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 78 |  | Knight__vs__Dark Shaman__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 79 |  | Knight__vs__Dark Shaman__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 80 |  | Knight__vs__Dark Shaman__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 81 |  | Knight__vs__Dark Shaman__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 82 |  | Knight__vs__Dark Shaman__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 83 |  | Knight__vs__Dark Shaman__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 84 |  | Knight__vs__Dark Shaman__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 85 |  | Knight__vs__Dark Shaman__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 86 |  | Knight__vs__Dark Shaman__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 87 |  | Armored Orc__vs__Tank x5__swarm__x5 | swarm | 5 | 11.636172282448854 | 0 | 0 | 0.0000 | ✅ |
| 88 |  | Armored Orc__vs__Tank x5__swarm__x5 | swarm | 5 | 14.743987135121246 | 0 | 0 | 0.0000 | ✅ |
| 89 |  | Armored Orc__vs__Tank x5__swarm__x5 | swarm | 5 | 6.623197448117615 | 0 | 0 | 0.0000 | ✅ |
| 90 |  | Armored Orc__vs__Tank x5__swarm__x5 | swarm | 5 | 3.63274133936497 | 0 | 0 | 0.0000 | ✅ |
| 91 |  | Armored Orc__vs__Tank x5__swarm__x5 | swarm | 5 | 8.58279352847375 | 0 | 0 | 0.0000 | ✅ |
| 92 |  | Armored Orc__vs__Tank x5__swarm__x5 | swarm | 5 | 5.588830207840064 | 0 | 0 | 0.0000 | ✅ |
| 93 |  | Goblin__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 11.800860867737782 | 0 | 0 | 0.0000 | ✅ |
| 94 |  | Goblin__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 8.002216240941983 | 0 | 0 | 0.0000 | ✅ |
| 95 |  | Goblin__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 5.711072716065519 | 0 | 0 | 0.0000 | ✅ |
| 96 |  | Goblin__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 3.657650213182392 | 0 | 0 | 0.0000 | ✅ |
| 97 |  | Goblin__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 4.229340807695653 | 0 | 0 | 0.0000 | ✅ |
| 98 |  | Ogre Boss__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 99 |  | Ogre Boss__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 100 |  | Ogre Boss__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 101 |  | Ogre Boss__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 102 |  | Ogre Boss__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 0 | 0.0000 | ❌ |
| 103 |  | Ogre Boss__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 104 |  | Ogre Boss__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 105 |  | Ogre Boss__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 106 |  | Ogre Boss__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 107 |  | Ogre Boss__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 0 | 0.0000 | ❌ |
| 108 |  | Ogre Boss__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 109 |  | Tank__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 110 |  | Tank__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 111 |  | Tank__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 112 |  | Tank__vs__Wyvern__duel__x1 | duel | 1 | 5.0 | 0 | 0 | 0.0000 | ✅ |
| 113 |  | Tank__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 114 |  | Tank__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 115 |  | Tank__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 116 |  | Tank__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 117 |  | Tank__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 118 |  | Tank__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 119 |  | Tank__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 120 |  | Tank__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 121 |  | Dark Shaman__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 122 |  | Dark Shaman__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 123 |  | Dark Shaman__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 124 |  | Dark Shaman__vs__AntiAir Tower__duel__x1 | duel | 1 | 5.0 | 1 | 1 | 1.0000 | ✅ |
| 125 |  | Dark Shaman__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 0 | 0.0000 | ❌ |
| 126 |  | Dark Shaman__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 127 |  | Dark Shaman__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 128 |  | Dark Shaman__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 129 |  | Dark Shaman__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 130 |  | Dark Shaman__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 131 |  | Dark Shaman__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 132 |  | Archer__vs__Knight__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 133 |  | Archer__vs__Knight__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 134 |  | Archer__vs__Knight__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 135 |  | Archer__vs__Knight__duel__x1 | duel | 1 |  | 1 | 0 | 0.0000 | ❌ |
| 136 |  | Archer__vs__Knight__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 137 |  | Archer__vs__Knight__duel__x1 | duel | 1 |  | 1 | 0 | 0.0000 | ❌ |
| 138 |  | Archer__vs__Knight__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 139 |  | Archer__vs__Knight__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 140 |  | Archer__vs__Knight__duel__x1 | duel | 1 |  | 1 | 0 | 0.0000 | ❌ |
| 141 |  | Archer__vs__Knight__duel__x1 | duel | 1 |  | 1 | 0 | 0.0000 | ❌ |
| 142 |  | Archer__vs__Runner x8__swarm__x8 | swarm | 8 | 3.498104543053737 | 1 | 1 | 1.0000 | ✅ |
| 143 |  | Archer__vs__Runner x8__swarm__x8 | swarm | 8 | 16.007904630186832 | 1 | 0 | 0.0000 | ❌ |
| 144 |  | Archer__vs__Runner x8__swarm__x8 | swarm | 8 | 8.74219744599957 | 0 | 0 | 0.0000 | ✅ |
| 145 |  | Archer__vs__Runner x8__swarm__x8 | swarm | 8 | 7.1413313426689875 | 0 | 0 | 0.0000 | ✅ |
| 146 |  | Archer__vs__Runner x8__swarm__x8 | swarm | 8 | 3.87858024385028 | 0 | 0 | 0.0000 | ✅ |
| 147 |  | Archer__vs__Runner x8__swarm__x8 | swarm | 8 | 9.583537828729378 | 0 | 0 | 0.0000 | ✅ |
| 148 |  | Archer__vs__Runner x8__swarm__x8 | swarm | 8 | 12.766587519326242 | 0 | 0 | 0.0000 | ✅ |
| 149 |  | Dark Shaman__vs__Archer x5__swarm__x5 | swarm | 5 | 8.538621123350065 | 0 | 0 | 0.0000 | ✅ |
| 150 |  | Dark Shaman__vs__Archer x5__swarm__x5 | swarm | 5 | 9.0771023220339 | 0 | 0 | 0.0000 | ✅ |
| 151 |  | Dark Shaman__vs__Archer x5__swarm__x5 | swarm | 5 | 6.1914755923274845 | 0 | 0 | 0.0000 | ✅ |
| 152 |  | Dark Shaman__vs__Archer x5__swarm__x5 | swarm | 5 | 4.293040888343876 | 0 | 0 | 0.0000 | ✅ |
| 153 |  | Dark Shaman__vs__Archer x5__swarm__x5 | swarm | 5 | 15.577527890983557 | 0 | 0 | 0.0000 | ✅ |
| 154 |  | Armored Orc__vs__Tank x8__swarm__x8 | swarm | 8 | 12.279215234351204 | 0 | 0 | 0.0000 | ✅ |
| 155 |  | Armored Orc__vs__Tank x8__swarm__x8 | swarm | 8 | 13.016023201107966 | 0 | 0 | 0.0000 | ✅ |
| 156 |  | Armored Orc__vs__Tank x8__swarm__x8 | swarm | 8 | 15.489376880150658 | 0 | 0 | 0.0000 | ✅ |
| 157 |  | Armored Orc__vs__Tank x8__swarm__x8 | swarm | 8 | 12.509338400050966 | 0 | 0 | 0.0000 | ✅ |
| 158 |  | Armored Orc__vs__Tank x8__swarm__x8 | swarm | 8 | 13.819656176346074 | 0 | 0 | 0.0000 | ✅ |
| 159 |  | Armored Orc__vs__Tank x8__swarm__x8 | swarm | 8 | 9.385705276512391 | 0 | 0 | 0.0000 | ✅ |
| 160 |  | Tank__vs__Mage x8__swarm__x8 | swarm | 8 | 5.0 | 0 | 0 | 0.0000 | ✅ |
| 161 |  | Tank__vs__Mage x8__swarm__x8 | swarm | 8 | 4.763150089832751 | 0 | 0 | 0.0000 | ✅ |
| 162 |  | Tank__vs__Mage x8__swarm__x8 | swarm | 8 | 4.889579373643277 | 0 | 0 | 0.0000 | ✅ |
| 163 |  | Tank__vs__Mage x8__swarm__x8 | swarm | 8 | 15.094125558398057 | 0 | 0 | 0.0000 | ✅ |
| 164 |  | Tank__vs__Mage x8__swarm__x8 | swarm | 8 | 1.4299874589171653 | 0 | 0 | 0.0000 | ✅ |
| 165 |  | Tank__vs__Mage x8__swarm__x8 | swarm | 8 | 14.11908473152757 | 0 | 0 | 0.0000 | ✅ |
| 166 |  | Armored Orc__vs__Archer__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 167 |  | Armored Orc__vs__Archer__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 168 |  | Armored Orc__vs__Archer__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 169 |  | Armored Orc__vs__Archer__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 170 |  | Armored Orc__vs__Archer__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 171 |  | Armored Orc__vs__Archer__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 172 |  | Armored Orc__vs__Archer__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 173 |  | Armored Orc__vs__Archer__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 174 |  | Armored Orc__vs__Archer__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 175 |  | Mage__vs__Armored Orc x8__swarm__x8 | swarm | 8 | 11.826165559037564 | 0 | 0 | 0.0000 | ✅ |
| 176 |  | Mage__vs__Armored Orc x8__swarm__x8 | swarm | 8 | 15.07657157424564 | 0 | 0 | 0.0000 | ✅ |
| 177 |  | Mage__vs__Armored Orc x8__swarm__x8 | swarm | 8 | 10.906876383787814 | 0 | 0 | 0.0000 | ✅ |
| 178 |  | Mage__vs__Armored Orc x8__swarm__x8 | swarm | 8 | 6.405149401108299 | 0 | 0 | 0.0000 | ✅ |
| 179 |  | Mage__vs__Armored Orc x8__swarm__x8 | swarm | 8 | 10.417080781362428 | 0 | 0 | 0.0000 | ✅ |
| 180 |  | Wyvern__vs__Tank__duel__x1 | duel | 1 |  | 1 | 0 | 0.0000 | ❌ |
| 181 |  | Wyvern__vs__Tank__duel__x1 | duel | 1 |  | 1 | 0 | 0.0000 | ❌ |
| 182 |  | Wyvern__vs__Tank__duel__x1 | duel | 1 |  | 1 | 0 | 0.0000 | ❌ |
| 183 |  | Wyvern__vs__Tank__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 184 |  | Wyvern__vs__Tank__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 185 |  | Wyvern__vs__Tank__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 186 |  | Wyvern__vs__Tank__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 187 |  | Wyvern__vs__Tank__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 188 |  | Wyvern__vs__Tank__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 189 |  | Wyvern__vs__Tank__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 190 |  | Tank__vs__Runner x8__swarm__x8 | swarm | 8 | 10.306231938736373 | 0 | 0 | 0.0000 | ✅ |
| 191 |  | Tank__vs__Runner x8__swarm__x8 | swarm | 8 | 6.181837736919462 | 0 | 0 | 0.0000 | ✅ |
| 192 |  | Tank__vs__Runner x8__swarm__x8 | swarm | 8 | 6.185963808167295 | 0 | 0 | 0.0000 | ✅ |
| 193 |  | Tank__vs__Runner x8__swarm__x8 | swarm | 8 | 11.379062860064934 | 0 | 0 | 0.0000 | ✅ |
| 194 |  | Knight__vs__AntiAir Tower x3__swarm__x3 | swarm | 3 | 12.4989321658261 | 0 | 0 | 0.0000 | ✅ |
| 195 |  | Knight__vs__AntiAir Tower x3__swarm__x3 | swarm | 3 | 8.716992574093844 | 0 | 0 | 0.0000 | ✅ |
| 196 |  | Knight__vs__AntiAir Tower x3__swarm__x3 | swarm | 3 | 10.132454511700693 | 0 | 0 | 0.0000 | ✅ |
| 197 |  | Knight__vs__AntiAir Tower x3__swarm__x3 | swarm | 3 | 7.589106130802731 | 0 | 0 | 0.0000 | ✅ |
| 198 |  | Knight__vs__AntiAir Tower x3__swarm__x3 | swarm | 3 | 5.8875657896488125 | 0 | 0 | 0.0000 | ✅ |
| 199 |  | Knight__vs__AntiAir Tower x3__swarm__x3 | swarm | 3 | 2.3641880098484815 | 0 | 0 | 0.0000 | ✅ |
| 200 |  | Knight__vs__Tank x8__swarm__x8 | swarm | 8 | 5.075138541336146 | 0 | 0 | 0.0000 | ✅ |
| 201 |  | Knight__vs__Tank x8__swarm__x8 | swarm | 8 | 6.634412088288245 | 0 | 0 | 0.0000 | ✅ |
| 202 |  | Knight__vs__Tank x8__swarm__x8 | swarm | 8 | 9.87846423618291 | 0 | 0 | 0.0000 | ✅ |
| 203 |  | Knight__vs__Tank x8__swarm__x8 | swarm | 8 | 8.376110211532563 | 0 | 0 | 0.0000 | ✅ |
| 204 |  | Wyvern__vs__Mage__duel__x1 | duel | 1 |  | 1 | 0 | 0.0000 | ❌ |
| 205 |  | Wyvern__vs__Mage__duel__x1 | duel | 1 |  | 1 | 0 | 0.0000 | ❌ |
| 206 |  | Wyvern__vs__Mage__duel__x1 | duel | 1 |  | 1 | 0 | 0.0000 | ❌ |
| 207 |  | Wyvern__vs__Mage__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 208 |  | Wyvern__vs__Mage__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 209 |  | Wyvern__vs__Mage__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 210 |  | Wyvern__vs__Mage__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 211 |  | Wyvern__vs__Mage__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 212 |  | Wyvern__vs__Mage__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 213 |  | Wyvern__vs__Mage__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 214 |  | Wyvern__vs__Mage__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 215 |  | AntiAir Tower__vs__Tank__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 216 |  | AntiAir Tower__vs__Tank__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 217 |  | AntiAir Tower__vs__Tank__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 218 |  | AntiAir Tower__vs__Tank__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 219 |  | AntiAir Tower__vs__Tank__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 220 |  | AntiAir Tower__vs__Tank__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 221 |  | AntiAir Tower__vs__Tank__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 222 |  | AntiAir Tower__vs__Tank__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 223 |  | AntiAir Tower__vs__Tank__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 224 |  | AntiAir Tower__vs__Tank__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 225 |  | AntiAir Tower__vs__Tank__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 226 |  | Ogre Boss__vs__Knight x8__swarm__x8 | swarm | 8 | 5.0 | 0 | 0 | 0.0000 | ✅ |
| 227 |  | Ogre Boss__vs__Knight x8__swarm__x8 | swarm | 8 | 10.552976201203238 | 0 | 0 | 0.0000 | ✅ |
| 228 |  | Ogre Boss__vs__Knight x8__swarm__x8 | swarm | 8 | 6.899880025117176 | 0 | 0 | 0.0000 | ✅ |
| 229 |  | Ogre Boss__vs__Knight x8__swarm__x8 | swarm | 8 | 5.8611813398871915 | 0 | 0 | 0.0000 | ✅ |
| 230 |  | Ogre Boss__vs__Knight x8__swarm__x8 | swarm | 8 | 13.88618160218913 | 0 | 0 | 0.0000 | ✅ |
| 231 |  | Ogre Boss__vs__Knight x8__swarm__x8 | swarm | 8 | 0.807345403180059 | 0 | 0 | 0.0000 | ✅ |
| 232 |  | Dark Shaman__vs__Wyvern x8__swarm__x8 | swarm | 8 | 6.061513906601075 | 0 | 0 | 0.0000 | ✅ |
| 233 |  | Dark Shaman__vs__Wyvern x8__swarm__x8 | swarm | 8 | 11.30255290807071 | 0 | 0 | 0.0000 | ✅ |
| 234 |  | Dark Shaman__vs__Wyvern x8__swarm__x8 | swarm | 8 | 8.088393634136354 | 0 | 0 | 0.0000 | ✅ |
| 235 |  | Dark Shaman__vs__Wyvern x8__swarm__x8 | swarm | 8 | 12.702124469070723 | 0 | 0 | 0.0000 | ✅ |
| 236 |  | Dark Shaman__vs__Wyvern x8__swarm__x8 | swarm | 8 | 10.61047546742362 | 0 | 0 | 0.0000 | ✅ |
| 237 |  | Mage__vs__Goblin__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 238 |  | Mage__vs__Goblin__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 239 |  | Mage__vs__Goblin__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 240 |  | Mage__vs__Goblin__duel__x1 | duel | 1 | 5.0 | 1 | 1 | 1.0000 | ✅ |
| 241 |  | Mage__vs__Goblin__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 242 |  | Mage__vs__Goblin__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 243 |  | Mage__vs__Goblin__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 244 |  | Mage__vs__Goblin__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 245 |  | Runner__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 246 |  | Runner__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 247 |  | Runner__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 248 |  | Runner__vs__AntiAir Tower__duel__x1 | duel | 1 | 5.0 | 1 | 1 | 1.0000 | ✅ |
| 249 |  | Runner__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 250 |  | Runner__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 251 |  | Runner__vs__AntiAir Tower__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 252 |  | Knight__vs__Runner x3__swarm__x3 | swarm | 3 | 9.593554589680155 | 0 | 0 | 0.0000 | ✅ |
| 253 |  | Knight__vs__Runner x3__swarm__x3 | swarm | 3 | 6.686320173042595 | 0 | 0 | 0.0000 | ✅ |
| 254 |  | Knight__vs__Runner x3__swarm__x3 | swarm | 3 | 12.66816445769684 | 0 | 0 | 0.0000 | ✅ |
| 255 |  | Knight__vs__Runner x3__swarm__x3 | swarm | 3 | 10.707463689417933 | 0 | 0 | 0.0000 | ✅ |
| 256 |  | Knight__vs__Runner x3__swarm__x3 | swarm | 3 | 2.6876688263481996 | 0 | 0 | 0.0000 | ✅ |
| 257 |  | AntiAir Tower__vs__Tank x3__swarm__x3 | swarm | 3 | 8.274083317090767 | 0 | 0 | 0.0000 | ✅ |
| 258 |  | AntiAir Tower__vs__Tank x3__swarm__x3 | swarm | 3 | 12.12513213871364 | 0 | 0 | 0.0000 | ✅ |
| 259 |  | AntiAir Tower__vs__Tank x3__swarm__x3 | swarm | 3 | 2.9656505428933224 | 0 | 1 | 1.0000 | ❌ |
| 260 |  | AntiAir Tower__vs__Tank x3__swarm__x3 | swarm | 3 | 9.331070937625833 | 0 | 0 | 0.0000 | ✅ |
| 261 |  | AntiAir Tower__vs__Tank x3__swarm__x3 | swarm | 3 | 2.5523002897210003 | 0 | 0 | 0.0000 | ✅ |
| 262 |  | Archer__vs__AntiAir Tower x3__swarm__x3 | swarm | 3 | 6.055055270611423 | 0 | 0 | 0.0000 | ✅ |
| 263 |  | Archer__vs__AntiAir Tower x3__swarm__x3 | swarm | 3 | 13.24313639395764 | 0 | 0 | 0.0000 | ✅ |
| 264 |  | Archer__vs__AntiAir Tower x3__swarm__x3 | swarm | 3 | 7.897414976913819 | 0 | 0 | 0.0000 | ✅ |
| 265 |  | Archer__vs__AntiAir Tower x3__swarm__x3 | swarm | 3 | 9.192732771781545 | 0 | 0 | 0.0000 | ✅ |
| 266 |  | Archer__vs__AntiAir Tower x3__swarm__x3 | swarm | 3 | 9.676043277612667 | 0 | 0 | 0.0000 | ✅ |
| 267 |  | Archer__vs__AntiAir Tower x3__swarm__x3 | swarm | 3 | 7.585848762048304 | 0 | 0 | 0.0000 | ✅ |
| 268 |  | Armored Orc__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 5.113389930964699 | 0 | 0 | 0.0000 | ✅ |
| 269 |  | Armored Orc__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 5.743162750331592 | 0 | 0 | 0.0000 | ✅ |
| 270 |  | Armored Orc__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 12.518473716745627 | 0 | 0 | 0.0000 | ✅ |
| 271 |  | Armored Orc__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 6.780860189202519 | 0 | 0 | 0.0000 | ✅ |
| 272 |  | Armored Orc__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 3.7248382710545624 | 0 | 0 | 0.0000 | ✅ |
| 273 |  | Armored Orc__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 1.2607121970526713 | 0 | 0 | 0.0000 | ✅ |
| 274 |  | Armored Orc__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 4.324251449527752 | 0 | 0 | 0.0000 | ✅ |
| 275 |  | Armored Orc__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 9.44621423177252 | 0 | 0 | 0.0000 | ✅ |
| 276 |  | Dark Shaman__vs__Goblin x8__swarm__x8 | swarm | 8 | 8.104949156132115 | 0 | 0 | 0.0000 | ✅ |
| 277 |  | Dark Shaman__vs__Goblin x8__swarm__x8 | swarm | 8 | 7.514861737979812 | 0 | 0 | 0.0000 | ✅ |
| 278 |  | Dark Shaman__vs__Goblin x8__swarm__x8 | swarm | 8 | 7.88882564322613 | 0 | 0 | 0.0000 | ✅ |
| 279 |  | AntiAir Tower__vs__Mage x3__swarm__x3 | swarm | 3 | 5.0 | 0 | 0 | 0.0000 | ✅ |
| 280 |  | AntiAir Tower__vs__Mage x3__swarm__x3 | swarm | 3 | 6.809392693208437 | 0 | 0 | 0.0000 | ✅ |
| 281 |  | AntiAir Tower__vs__Mage x3__swarm__x3 | swarm | 3 | 1.8521842432943587 | 0 | 0 | 0.0000 | ✅ |
| 282 |  | AntiAir Tower__vs__Mage x3__swarm__x3 | swarm | 3 | 10.256232560030142 | 0 | 0 | 0.0000 | ✅ |
| 283 |  | AntiAir Tower__vs__Mage x3__swarm__x3 | swarm | 3 | 11.11706295077913 | 0 | 0 | 0.0000 | ✅ |
| 284 |  | AntiAir Tower__vs__Mage x3__swarm__x3 | swarm | 3 | 16.288345618450116 | 0 | 0 | 0.0000 | ✅ |
| 285 |  | AntiAir Tower__vs__Mage x3__swarm__x3 | swarm | 3 | 8.799834812732774 | 0 | 0 | 0.0000 | ✅ |
| 286 |  | Wyvern__vs__Runner x5__swarm__x5 | swarm | 5 | 2.992607710038018 | 0 | 0 | 0.0000 | ✅ |
| 287 |  | Wyvern__vs__Runner x5__swarm__x5 | swarm | 5 | 3.1156236984405448 | 0 | 0 | 0.0000 | ✅ |
| 288 |  | Wyvern__vs__Runner x5__swarm__x5 | swarm | 5 | 13.423147328582857 | 0 | 0 | 0.0000 | ✅ |
| 289 |  | Wyvern__vs__Runner x5__swarm__x5 | swarm | 5 | 11.21505671650059 | 0 | 0 | 0.0000 | ✅ |
| 290 |  | Wyvern__vs__Runner x5__swarm__x5 | swarm | 5 | 12.8931482016279 | 0 | 0 | 0.0000 | ✅ |
| 291 |  | Armored Orc__vs__Knight__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 292 |  | Armored Orc__vs__Knight__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 293 |  | Armored Orc__vs__Knight__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 294 |  | Armored Orc__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 295 |  | Armored Orc__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 296 |  | Armored Orc__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 297 |  | Armored Orc__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 298 |  | Armored Orc__vs__Knight__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 299 |  | Armored Orc__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 300 |  | Armored Orc__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 301 |  | Armored Orc__vs__Knight__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 302 |  | Archer__vs__Mage x3__swarm__x3 | swarm | 3 | 13.238199005733753 | 0 | 0 | 0.0000 | ✅ |
| 303 |  | Archer__vs__Mage x3__swarm__x3 | swarm | 3 | 10.362484016376758 | 0 | 0 | 0.0000 | ✅ |
| 304 |  | Archer__vs__Mage x3__swarm__x3 | swarm | 3 | 12.871696681922664 | 0 | 0 | 0.0000 | ✅ |
| 305 |  | Archer__vs__Mage x3__swarm__x3 | swarm | 3 | 8.967231123966968 | 0 | 0 | 0.0000 | ✅ |
| 306 |  | Archer__vs__Knight x3__swarm__x3 | swarm | 3 | 5.0 | 0 | 0 | 0.0000 | ✅ |
| 307 |  | Archer__vs__Knight x3__swarm__x3 | swarm | 3 | 11.650815989501652 | 0 | 0 | 0.0000 | ✅ |
| 308 |  | Archer__vs__Knight x3__swarm__x3 | swarm | 3 | 5.274509505393979 | 0 | 0 | 0.0000 | ✅ |
| 309 |  | Archer__vs__Knight x3__swarm__x3 | swarm | 3 | 5.218025721427933 | 0 | 0 | 0.0000 | ✅ |
| 310 |  | Archer__vs__Knight x3__swarm__x3 | swarm | 3 | 11.921601137635921 | 0 | 0 | 0.0000 | ✅ |
| 311 |  | Archer__vs__Knight x3__swarm__x3 | swarm | 3 | 2.256072116839372 | 1 | 0 | 0.0000 | ❌ |
| 312 |  | Archer__vs__Knight x3__swarm__x3 | swarm | 3 | 9.148398310092944 | 0 | 0 | 0.0000 | ✅ |
| 313 |  | Dark Shaman__vs__Knight x3__swarm__x3 | swarm | 3 | 9.833952124240493 | 0 | 0 | 0.0000 | ✅ |
| 314 |  | Dark Shaman__vs__Knight x3__swarm__x3 | swarm | 3 | 6.128665621109864 | 0 | 0 | 0.0000 | ✅ |
| 315 |  | Dark Shaman__vs__Knight x3__swarm__x3 | swarm | 3 | 14.841742010030178 | 0 | 0 | 0.0000 | ✅ |
| 316 |  | Runner__vs__Dark Shaman x5__swarm__x5 | swarm | 5 | 8.784540227025632 | 0 | 0 | 0.0000 | ✅ |
| 317 |  | Runner__vs__Dark Shaman x5__swarm__x5 | swarm | 5 | 9.905511154321594 | 0 | 0 | 0.0000 | ✅ |
| 318 |  | Runner__vs__Dark Shaman x5__swarm__x5 | swarm | 5 | 2.348321596699029 | 0 | 0 | 0.0000 | ✅ |
| 319 |  | Runner__vs__Dark Shaman x5__swarm__x5 | swarm | 5 | 2.0695373398743966 | 0 | 0 | 0.0000 | ✅ |
| 320 |  | Runner__vs__Dark Shaman x5__swarm__x5 | swarm | 5 | 4.813571959657357 | 0 | 0 | 0.0000 | ✅ |
| 321 |  | Ogre Boss__vs__Knight x5__swarm__x5 | swarm | 5 | 15.874333974093046 | 0 | 0 | 0.0000 | ✅ |
| 322 |  | Ogre Boss__vs__Knight x5__swarm__x5 | swarm | 5 | 8.834323490378079 | 0 | 0 | 0.0000 | ✅ |
| 323 |  | Ogre Boss__vs__Knight x5__swarm__x5 | swarm | 5 | 4.141093743565397 | 0 | 0 | 0.0000 | ✅ |
| 324 |  | Armored Orc__vs__Knight x8__swarm__x8 | swarm | 8 | 12.623502901658387 | 0 | 0 | 0.0000 | ✅ |
| 325 |  | Armored Orc__vs__Knight x8__swarm__x8 | swarm | 8 | 8.277980615296327 | 0 | 0 | 0.0000 | ✅ |
| 326 |  | Armored Orc__vs__Knight x8__swarm__x8 | swarm | 8 | 1.688573412753284 | 0 | 0 | 0.0000 | ✅ |
| 327 |  | Armored Orc__vs__Knight x8__swarm__x8 | swarm | 8 | 5.6585421888785765 | 0 | 0 | 0.0000 | ✅ |
| 328 |  | Armored Orc__vs__Knight x8__swarm__x8 | swarm | 8 | 5.854649046122148 | 0 | 0 | 0.0000 | ✅ |
| 329 |  | Armored Orc__vs__Knight x8__swarm__x8 | swarm | 8 | 9.226660613636044 | 0 | 0 | 0.0000 | ✅ |
| 330 |  | Mage__vs__Wyvern x8__swarm__x8 | swarm | 8 | 12.116251223391753 | 0 | 0 | 0.0000 | ✅ |
| 331 |  | Mage__vs__Wyvern x8__swarm__x8 | swarm | 8 | 11.37152410156872 | 0 | 0 | 0.0000 | ✅ |
| 332 |  | Mage__vs__Wyvern x8__swarm__x8 | swarm | 8 | 5.9384844312121166 | 0 | 0 | 0.0000 | ✅ |
| 333 |  | Mage__vs__Wyvern x8__swarm__x8 | swarm | 8 | 5.68397692824934 | 0 | 0 | 0.0000 | ✅ |
| 334 |  | Mage__vs__Wyvern x8__swarm__x8 | swarm | 8 | 5.212517218799157 | 0 | 0 | 0.0000 | ✅ |
| 335 |  | Armored Orc__vs__Goblin x3__swarm__x3 | swarm | 3 | 15.297071406102562 | 0 | 0 | 0.0000 | ✅ |
| 336 |  | Armored Orc__vs__Goblin x3__swarm__x3 | swarm | 3 | 3.7271827756583864 | 0 | 0 | 0.0000 | ✅ |
| 337 |  | Armored Orc__vs__Goblin x3__swarm__x3 | swarm | 3 | 12.329861759528796 | 0 | 0 | 0.0000 | ✅ |
| 338 |  | Armored Orc__vs__Goblin x3__swarm__x3 | swarm | 3 | 9.139988190626537 | 0 | 0 | 0.0000 | ✅ |
| 339 |  | Archer__vs__Dark Shaman__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 340 |  | Archer__vs__Dark Shaman__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 341 |  | Archer__vs__Dark Shaman__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 342 |  | Archer__vs__Dark Shaman__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 343 |  | Archer__vs__Dark Shaman__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 344 |  | Archer__vs__Dark Shaman__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 345 |  | Archer__vs__Dark Shaman__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 346 |  | Archer__vs__Dark Shaman__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 347 |  | Archer__vs__Dark Shaman__duel__x1 | duel | 1 |  | 1 | 0 | 0.0000 | ❌ |
| 348 |  | Archer__vs__Dark Shaman__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 349 |  | Archer__vs__Dark Shaman__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 350 |  | Archer__vs__Dark Shaman__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 351 |  | Goblin__vs__Dark Shaman x8__swarm__x8 | swarm | 8 | 15.697591720006855 | 0 | 0 | 0.0000 | ✅ |
| 352 |  | Goblin__vs__Dark Shaman x8__swarm__x8 | swarm | 8 | 7.129704902199527 | 0 | 0 | 0.0000 | ✅ |
| 353 |  | Goblin__vs__Dark Shaman x8__swarm__x8 | swarm | 8 | 8.257490633105578 | 0 | 0 | 0.0000 | ✅ |
| 354 |  | Runner__vs__AntiAir Tower x8__swarm__x8 | swarm | 8 | 2.927190090685124 | 0 | 0 | 0.0000 | ✅ |
| 355 |  | Runner__vs__AntiAir Tower x8__swarm__x8 | swarm | 8 | 11.414300942593506 | 1 | 0 | 0.0000 | ❌ |
| 356 |  | Runner__vs__AntiAir Tower x8__swarm__x8 | swarm | 8 | 7.318240212045201 | 0 | 0 | 0.0000 | ✅ |
| 357 |  | Runner__vs__AntiAir Tower x8__swarm__x8 | swarm | 8 | 14.302130279419199 | 0 | 0 | 0.0000 | ✅ |
| 358 |  | Runner__vs__AntiAir Tower x8__swarm__x8 | swarm | 8 | 12.071053126068172 | 0 | 0 | 0.0000 | ✅ |
| 359 |  | AntiAir Tower__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 4.306612759308749 | 0 | 0 | 0.0000 | ✅ |
| 360 |  | AntiAir Tower__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 4.717870165495616 | 0 | 0 | 0.0000 | ✅ |
| 361 |  | AntiAir Tower__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 11.202263928623807 | 0 | 0 | 0.0000 | ✅ |
| 362 |  | AntiAir Tower__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 9.90790067278997 | 0 | 0 | 0.0000 | ✅ |
| 363 |  | AntiAir Tower__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 13.846269098295867 | 0 | 0 | 0.0000 | ✅ |
| 364 |  | Goblin__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 365 |  | Goblin__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 366 |  | Goblin__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 367 |  | Goblin__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 368 |  | Goblin__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 369 |  | Goblin__vs__Knight__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 370 |  | Goblin__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 371 |  | Goblin__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 372 |  | Goblin__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 373 |  | Goblin__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 374 |  | Goblin__vs__Knight__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 375 |  | Knight__vs__Goblin x8__swarm__x8 | swarm | 8 | 6.004011082293887 | 0 | 0 | 0.0000 | ✅ |
| 376 |  | Knight__vs__Goblin x8__swarm__x8 | swarm | 8 | 11.31805724656334 | 0 | 0 | 0.0000 | ✅ |
| 377 |  | Knight__vs__Goblin x8__swarm__x8 | swarm | 8 | 10.337485391759031 | 0 | 0 | 0.0000 | ✅ |
| 378 |  | Knight__vs__Goblin x8__swarm__x8 | swarm | 8 | 7.569155171903417 | 0 | 0 | 0.0000 | ✅ |
| 379 |  | Armored Orc__vs__Dark Shaman__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 380 |  | Armored Orc__vs__Dark Shaman__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 381 |  | Armored Orc__vs__Dark Shaman__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 382 |  | Armored Orc__vs__Dark Shaman__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 383 |  | Armored Orc__vs__Dark Shaman__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 384 |  | Armored Orc__vs__Dark Shaman__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 385 |  | Armored Orc__vs__Dark Shaman__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 386 |  | Mage__vs__Tank x3__swarm__x3 | swarm | 3 | 12.222001336544004 | 0 | 0 | 0.0000 | ✅ |
| 387 |  | Mage__vs__Tank x3__swarm__x3 | swarm | 3 | 12.32403856727593 | 0 | 0 | 0.0000 | ✅ |
| 388 |  | Mage__vs__Tank x3__swarm__x3 | swarm | 3 | 6.296431600261274 | 0 | 1 | 1.0000 | ❌ |
| 389 |  | Mage__vs__Tank x3__swarm__x3 | swarm | 3 | 7.619605239396276 | 0 | 0 | 0.0000 | ✅ |
| 390 |  | Mage__vs__Tank x3__swarm__x3 | swarm | 3 | 3.499602965004656 | 0 | 0 | 0.0000 | ✅ |
| 391 |  | Wyvern__vs__Dark Shaman x8__swarm__x8 | swarm | 8 | 5.642689823445103 | 0 | 0 | 0.0000 | ✅ |
| 392 |  | Wyvern__vs__Dark Shaman x8__swarm__x8 | swarm | 8 | 10.015901789122754 | 0 | 0 | 0.0000 | ✅ |
| 393 |  | Wyvern__vs__Dark Shaman x8__swarm__x8 | swarm | 8 | 7.392943837384936 | 0 | 0 | 0.0000 | ✅ |
| 394 |  | Mage__vs__Ogre Boss x5__swarm__x5 | swarm | 5 | 6.5228507716673905 | 0 | 0 | 0.0000 | ✅ |
| 395 |  | Mage__vs__Ogre Boss x5__swarm__x5 | swarm | 5 | 7.895471819738201 | 0 | 0 | 0.0000 | ✅ |
| 396 |  | Mage__vs__Ogre Boss x5__swarm__x5 | swarm | 5 | 11.198967838487407 | 0 | 0 | 0.0000 | ✅ |
| 397 |  | Mage__vs__Ogre Boss x5__swarm__x5 | swarm | 5 | 2.502375467090411 | 0 | 0 | 0.0000 | ✅ |
| 398 |  | Mage__vs__Ogre Boss x5__swarm__x5 | swarm | 5 | 8.626715789602617 | 0 | 0 | 0.0000 | ✅ |
| 399 |  | Knight__vs__Archer x8__swarm__x8 | swarm | 8 | 3.103610201175212 | 0 | 0 | 0.0000 | ✅ |
| 400 |  | Knight__vs__Archer x8__swarm__x8 | swarm | 8 | 5.333052341922096 | 0 | 0 | 0.0000 | ✅ |
| 401 |  | Knight__vs__Archer x8__swarm__x8 | swarm | 8 | 6.407893201767157 | 0 | 0 | 0.0000 | ✅ |
| 402 |  | Knight__vs__Archer x8__swarm__x8 | swarm | 8 | 6.697854080997029 | 0 | 0 | 0.0000 | ✅ |
| 403 |  | Knight__vs__Archer x8__swarm__x8 | swarm | 8 | 10.82203319497443 | 0 | 0 | 0.0000 | ✅ |
| 404 |  | Knight__vs__Archer x8__swarm__x8 | swarm | 8 | 3.966980179406969 | 0 | 0 | 0.0000 | ✅ |
| 405 |  | Armored Orc__vs__Wyvern x5__swarm__x5 | swarm | 5 | 5.948909704248776 | 0 | 0 | 0.0000 | ✅ |
| 406 |  | Armored Orc__vs__Wyvern x5__swarm__x5 | swarm | 5 | 9.23046748451661 | 0 | 0 | 0.0000 | ✅ |
| 407 |  | Armored Orc__vs__Wyvern x5__swarm__x5 | swarm | 5 | 12.033628508454594 | 0 | 0 | 0.0000 | ✅ |
| 408 |  | Armored Orc__vs__Wyvern x5__swarm__x5 | swarm | 5 | 3.445515074401869 | 0 | 0 | 0.0000 | ✅ |
| 409 |  | Armored Orc__vs__Wyvern x5__swarm__x5 | swarm | 5 | 9.395868373882227 | 0 | 0 | 0.0000 | ✅ |
| 410 |  | Runner__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 9.718019332738828 | 0 | 0 | 0.0000 | ✅ |
| 411 |  | Runner__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 14.133022439994301 | 0 | 0 | 0.0000 | ✅ |
| 412 |  | Runner__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 8.13272060584227 | 0 | 0 | 0.0000 | ✅ |
| 413 |  | Runner__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 11.190509630141072 | 0 | 0 | 0.0000 | ✅ |
| 414 |  | Runner__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 8.534839006629221 | 0 | 0 | 0.0000 | ✅ |
| 415 |  | Runner__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 14.532760836305707 | 0 | 0 | 0.0000 | ✅ |
| 416 |  | Runner__vs__Ogre Boss x3__swarm__x3 | swarm | 3 | 8.288250914082866 | 0 | 0 | 0.0000 | ✅ |
| 417 |  | Dark Shaman__vs__Wyvern x5__swarm__x5 | swarm | 5 | 16.537555206790007 | 0 | 0 | 0.0000 | ✅ |
| 418 |  | Dark Shaman__vs__Wyvern x5__swarm__x5 | swarm | 5 | 13.987813074007606 | 0 | 0 | 0.0000 | ✅ |
| 419 |  | Dark Shaman__vs__Wyvern x5__swarm__x5 | swarm | 5 | 13.651009046670232 | 0 | 0 | 0.0000 | ✅ |
| 420 |  | Dark Shaman__vs__Wyvern x5__swarm__x5 | swarm | 5 | 10.145959839846364 | 0 | 0 | 0.0000 | ✅ |
| 421 |  | Dark Shaman__vs__Wyvern x5__swarm__x5 | swarm | 5 | 6.304487981195205 | 0 | 0 | 0.0000 | ✅ |
| 422 |  | Wyvern__vs__Runner x8__swarm__x8 | swarm | 8 | 11.26153603025176 | 0 | 0 | 0.0000 | ✅ |
| 423 |  | Wyvern__vs__Runner x8__swarm__x8 | swarm | 8 | 8.562168746624245 | 0 | 0 | 0.0000 | ✅ |
| 424 |  | Wyvern__vs__Runner x8__swarm__x8 | swarm | 8 | 11.395539811328542 | 0 | 0 | 0.0000 | ✅ |
| 425 |  | Wyvern__vs__Runner x8__swarm__x8 | swarm | 8 | 4.000659157778561 | 0 | 0 | 0.0000 | ✅ |
| 426 |  | Wyvern__vs__Runner x8__swarm__x8 | swarm | 8 | 12.683628610741714 | 0 | 0 | 0.0000 | ✅ |
| 427 |  | Archer__vs__Goblin x5__swarm__x5 | swarm | 5 | 5.0 | 0 | 0 | 0.0000 | ✅ |
| 428 |  | Archer__vs__Goblin x5__swarm__x5 | swarm | 5 | 2.745848309043992 | 0 | 0 | 0.0000 | ✅ |
| 429 |  | Archer__vs__Goblin x5__swarm__x5 | swarm | 5 | 5.83387884308148 | 0 | 0 | 0.0000 | ✅ |
| 430 |  | Dark Shaman__vs__Ogre Boss x5__swarm__x5 | swarm | 5 | 4.311519330737438 | 0 | 0 | 0.0000 | ✅ |
| 431 |  | Dark Shaman__vs__Ogre Boss x5__swarm__x5 | swarm | 5 | 9.801904864591917 | 0 | 0 | 0.0000 | ✅ |
| 432 |  | Dark Shaman__vs__Ogre Boss x5__swarm__x5 | swarm | 5 | 12.74853092455129 | 0 | 0 | 0.0000 | ✅ |
| 433 |  | Dark Shaman__vs__Ogre Boss x5__swarm__x5 | swarm | 5 | 4.2397485406234905 | 0 | 0 | 0.0000 | ✅ |
| 434 |  | Dark Shaman__vs__Ogre Boss x5__swarm__x5 | swarm | 5 | 10.43266951271695 | 0 | 0 | 0.0000 | ✅ |
| 435 |  | Dark Shaman__vs__Ogre Boss x5__swarm__x5 | swarm | 5 | 5.697804920294758 | 0 | 0 | 0.0000 | ✅ |
| 436 |  | Dark Shaman__vs__Ogre Boss x5__swarm__x5 | swarm | 5 | 7.893617837233611 | 0 | 0 | 0.0000 | ✅ |
| 437 |  | Dark Shaman__vs__Ogre Boss x5__swarm__x5 | swarm | 5 | 7.22843674996656 | 0 | 0 | 0.0000 | ✅ |
| 438 |  | AntiAir Tower__vs__Wyvern x8__swarm__x8 | swarm | 8 | 12.420587409197086 | 0 | 0 | 0.0000 | ✅ |
| 439 |  | AntiAir Tower__vs__Wyvern x8__swarm__x8 | swarm | 8 | 10.651075937506674 | 0 | 0 | 0.0000 | ✅ |
| 440 |  | AntiAir Tower__vs__Wyvern x8__swarm__x8 | swarm | 8 | 12.523937723925972 | 0 | 0 | 0.0000 | ✅ |
| 441 |  | Tank__vs__Archer x8__swarm__x8 | swarm | 8 | 2.557292379176208 | 0 | 0 | 0.0000 | ✅ |
| 442 |  | Tank__vs__Archer x8__swarm__x8 | swarm | 8 | 10.391352556128954 | 0 | 0 | 0.0000 | ✅ |
| 443 |  | Tank__vs__Archer x8__swarm__x8 | swarm | 8 | 8.036713662712044 | 0 | 0 | 0.0000 | ✅ |
| 444 |  | Tank__vs__Archer x8__swarm__x8 | swarm | 8 | 11.843757578357978 | 0 | 0 | 0.0000 | ✅ |
| 445 |  | Tank__vs__Archer x8__swarm__x8 | swarm | 8 | 5.485584959155974 | 0 | 0 | 0.0000 | ✅ |
| 446 |  | Tank__vs__Archer x8__swarm__x8 | swarm | 8 | 8.479043574652309 | 0 | 0 | 0.0000 | ✅ |
| 447 |  | Tank__vs__Archer x8__swarm__x8 | swarm | 8 | 3.2009778210862914 | 0 | 0 | 0.0000 | ✅ |
| 448 |  | Armored Orc__vs__Goblin x8__swarm__x8 | swarm | 8 | 3.535889778340564 | 0 | 0 | 0.0000 | ✅ |
| 449 |  | Knight__vs__Dark Shaman x5__swarm__x5 | swarm | 5 | 1.4796756845171388 | 0 | 0 | 0.0000 | ✅ |
| 450 |  | Knight__vs__Dark Shaman x5__swarm__x5 | swarm | 5 | 8.433703847396016 | 0 | 0 | 0.0000 | ✅ |
| 451 |  | Knight__vs__Dark Shaman x5__swarm__x5 | swarm | 5 | 12.543516516449364 | 0 | 0 | 0.0000 | ✅ |
| 452 |  | Knight__vs__Dark Shaman x5__swarm__x5 | swarm | 5 | 9.073618034083175 | 0 | 0 | 0.0000 | ✅ |
| 453 |  | Knight__vs__Dark Shaman x5__swarm__x5 | swarm | 5 | 6.7341479327663265 | 0 | 0 | 0.0000 | ✅ |
| 454 |  | Knight__vs__Dark Shaman x5__swarm__x5 | swarm | 5 | 9.07000551886461 | 0 | 0 | 0.0000 | ✅ |
| 455 |  | Archer__vs__Goblin x8__swarm__x8 | swarm | 8 | 10.689962796559321 | 0 | 0 | 0.0000 | ✅ |
| 456 |  | Archer__vs__Goblin x8__swarm__x8 | swarm | 8 | 12.47524393177599 | 0 | 0 | 0.0000 | ✅ |
| 457 |  | Archer__vs__Goblin x8__swarm__x8 | swarm | 8 | 7.246592934820901 | 0 | 0 | 0.0000 | ✅ |
| 458 |  | Archer__vs__Goblin x8__swarm__x8 | swarm | 8 | 11.255581803423588 | 0 | 0 | 0.0000 | ✅ |
| 459 |  | Archer__vs__Goblin x8__swarm__x8 | swarm | 8 | 11.039065970310354 | 0 | 0 | 0.0000 | ✅ |
| 460 |  | Archer__vs__Goblin x8__swarm__x8 | swarm | 8 | 5.669592972684825 | 0 | 0 | 0.0000 | ✅ |
| 461 |  | Dark Shaman__vs__Mage x8__swarm__x8 | swarm | 8 | 7.248158085356224 | 0 | 0 | 0.0000 | ✅ |
| 462 |  | Dark Shaman__vs__Mage x8__swarm__x8 | swarm | 8 | 3.06955758899058 | 0 | 0 | 0.0000 | ✅ |
| 463 |  | Dark Shaman__vs__Mage x8__swarm__x8 | swarm | 8 | 7.260038943344954 | 0 | 0 | 0.0000 | ✅ |
| 464 |  | Dark Shaman__vs__Mage x8__swarm__x8 | swarm | 8 | 2.4912746376210566 | 0 | 0 | 0.0000 | ✅ |
| 465 |  | Dark Shaman__vs__Mage x8__swarm__x8 | swarm | 8 | 5.586656773061953 | 0 | 0 | 0.0000 | ✅ |
| 466 |  | Dark Shaman__vs__Runner x8__swarm__x8 | swarm | 8 | 5.0 | 0 | 0 | 0.0000 | ✅ |
| 467 |  | Dark Shaman__vs__Runner x8__swarm__x8 | swarm | 8 | 3.9830113385705164 | 0 | 0 | 0.0000 | ✅ |
| 468 |  | Dark Shaman__vs__Runner x8__swarm__x8 | swarm | 8 | 9.88158838983128 | 0 | 0 | 0.0000 | ✅ |
| 469 |  | Dark Shaman__vs__Runner x8__swarm__x8 | swarm | 8 | 13.767921064752882 | 0 | 0 | 0.0000 | ✅ |
| 470 |  | Dark Shaman__vs__Runner x8__swarm__x8 | swarm | 8 | 7.385094229786827 | 0 | 0 | 0.0000 | ✅ |
| 471 |  | Dark Shaman__vs__Runner x8__swarm__x8 | swarm | 8 | 3.7406807929147057 | 0 | 0 | 0.0000 | ✅ |
| 472 |  | Knight__vs__Armored Orc x5__swarm__x5 | swarm | 5 | 15.25576241103098 | 0 | 0 | 0.0000 | ✅ |
| 473 |  | Knight__vs__Armored Orc x5__swarm__x5 | swarm | 5 | 7.142827295812383 | 0 | 0 | 0.0000 | ✅ |
| 474 |  | Knight__vs__Armored Orc x5__swarm__x5 | swarm | 5 | 5.681796470146172 | 0 | 0 | 0.0000 | ✅ |
| 475 |  | Knight__vs__Armored Orc x5__swarm__x5 | swarm | 5 | 15.44129502599279 | 0 | 0 | 0.0000 | ✅ |
| 476 |  | Ogre Boss__vs__AntiAir Tower x8__swarm__x8 | swarm | 8 | 10.71673911985481 | 1 | 1 | 1.0000 | ✅ |
| 477 |  | Ogre Boss__vs__AntiAir Tower x8__swarm__x8 | swarm | 8 | 3.912873459958925 | 0 | 0 | 0.0000 | ✅ |
| 478 |  | Ogre Boss__vs__AntiAir Tower x8__swarm__x8 | swarm | 8 | 8.98814115372109 | 0 | 0 | 0.0000 | ✅ |
| 479 |  | Ogre Boss__vs__AntiAir Tower x8__swarm__x8 | swarm | 8 | 6.340305608073512 | 1 | 1 | 1.0000 | ✅ |
| 480 |  | Ogre Boss__vs__AntiAir Tower x8__swarm__x8 | swarm | 8 | 3.3322041769335184 | 0 | 0 | 0.0000 | ✅ |
| 481 |  | Ogre Boss__vs__Wyvern x3__swarm__x3 | swarm | 3 | 8.596133248896896 | 0 | 0 | 0.0000 | ✅ |
| 482 |  | Ogre Boss__vs__Wyvern x3__swarm__x3 | swarm | 3 | 8.647725729339964 | 0 | 0 | 0.0000 | ✅ |
| 483 |  | Ogre Boss__vs__Wyvern x3__swarm__x3 | swarm | 3 | 10.492613180838388 | 0 | 0 | 0.0000 | ✅ |
| 484 |  | Ogre Boss__vs__Wyvern x3__swarm__x3 | swarm | 3 | 14.658591641874056 | 0 | 0 | 0.0000 | ✅ |
| 485 |  | Knight__vs__Mage x5__swarm__x5 | swarm | 5 | 11.570224645529459 | 0 | 0 | 0.0000 | ✅ |
| 486 |  | Knight__vs__Mage x5__swarm__x5 | swarm | 5 | 6.790448770723671 | 0 | 0 | 0.0000 | ✅ |
| 487 |  | Knight__vs__Mage x5__swarm__x5 | swarm | 5 | 4.948401979440167 | 0 | 0 | 0.0000 | ✅ |
| 488 |  | Knight__vs__Mage x5__swarm__x5 | swarm | 5 | 3.238094841664895 | 0 | 0 | 0.0000 | ✅ |
| 489 |  | Knight__vs__Mage x5__swarm__x5 | swarm | 5 | 14.700485634526098 | 0 | 0 | 0.0000 | ✅ |
| 490 |  | Knight__vs__Mage x5__swarm__x5 | swarm | 5 | 3.9415563377452867 | 0 | 0 | 0.0000 | ✅ |
| 491 |  | Runner__vs__Tank x3__swarm__x3 | swarm | 3 | 1.2609087308627334 | 0 | 0 | 0.0000 | ✅ |
| 492 |  | Runner__vs__Tank x3__swarm__x3 | swarm | 3 | 4.960955029425097 | 0 | 0 | 0.0000 | ✅ |
| 493 |  | Runner__vs__Tank x3__swarm__x3 | swarm | 3 | 12.254560204900619 | 0 | 0 | 0.0000 | ✅ |
| 494 |  | Runner__vs__Tank x3__swarm__x3 | swarm | 3 | 8.820571348458373 | 0 | 0 | 0.0000 | ✅ |
| 495 |  | Runner__vs__Tank x3__swarm__x3 | swarm | 3 | 12.568126921934962 | 0 | 0 | 0.0000 | ✅ |
| 496 |  | Runner__vs__Tank x3__swarm__x3 | swarm | 3 | 5.305457826626303 | 0 | 0 | 0.0000 | ✅ |
| 497 |  | Dark Shaman__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 498 |  | Dark Shaman__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 499 |  | Dark Shaman__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 500 |  | Dark Shaman__vs__Knight__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 501 |  | Dark Shaman__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 502 |  | Dark Shaman__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 503 |  | Dark Shaman__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 504 |  | Dark Shaman__vs__Knight__duel__x1 | duel | 1 |  | 1 | 1 | 1.0000 | ✅ |
| 505 |  | Dark Shaman__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 506 |  | Dark Shaman__vs__Knight__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 507 |  | Runner__vs__Tank x8__swarm__x8 | swarm | 8 | 10.801577376539234 | 0 | 0 | 0.0000 | ✅ |
| 508 |  | Runner__vs__Tank x8__swarm__x8 | swarm | 8 | 4.270054485682124 | 0 | 0 | 0.0000 | ✅ |
| 509 |  | Runner__vs__Tank x8__swarm__x8 | swarm | 8 | 10.25144216884496 | 0 | 0 | 0.0000 | ✅ |
| 510 |  | Runner__vs__Tank x8__swarm__x8 | swarm | 8 | 0.9924322342755796 | 0 | 0 | 0.0000 | ✅ |
| 511 |  | Runner__vs__Tank x8__swarm__x8 | swarm | 8 | 6.0202683119216385 | 0 | 0 | 0.0000 | ✅ |
| 512 |  | Runner__vs__Tank x8__swarm__x8 | swarm | 8 | 14.043755108496907 | 0 | 0 | 0.0000 | ✅ |
| 513 |  | Archer__vs__Wyvern x5__swarm__x5 | swarm | 5 | 5.0 | 0 | 0 | 0.0000 | ✅ |
| 514 |  | Archer__vs__Wyvern x5__swarm__x5 | swarm | 5 | 8.285051606004744 | 0 | 0 | 0.0000 | ✅ |
| 515 |  | Archer__vs__Wyvern x5__swarm__x5 | swarm | 5 | 7.21753378209275 | 0 | 0 | 0.0000 | ✅ |
| 516 |  | Archer__vs__Wyvern x5__swarm__x5 | swarm | 5 | 10.936811341295737 | 0 | 0 | 0.0000 | ✅ |
| 517 |  | Archer__vs__Wyvern x5__swarm__x5 | swarm | 5 | 5.974384261774505 | 0 | 0 | 0.0000 | ✅ |
| 518 |  | Archer__vs__Wyvern x5__swarm__x5 | swarm | 5 | 14.390736377692447 | 0 | 0 | 0.0000 | ✅ |
| 519 |  | Knight__vs__Mage x3__swarm__x3 | swarm | 3 | 9.41524837820104 | 0 | 0 | 0.0000 | ✅ |
| 520 |  | Knight__vs__Mage x3__swarm__x3 | swarm | 3 | 8.672041902013023 | 0 | 0 | 0.0000 | ✅ |
| 521 |  | Knight__vs__Mage x3__swarm__x3 | swarm | 3 | 7.09718813096042 | 0 | 0 | 0.0000 | ✅ |
| 522 |  | Knight__vs__Mage x3__swarm__x3 | swarm | 3 | 3.6532085499025175 | 0 | 0 | 0.0000 | ✅ |
| 523 |  | Knight__vs__Mage x3__swarm__x3 | swarm | 3 | 10.67366880994982 | 0 | 1 | 1.0000 | ❌ |
| 524 |  | Knight__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 525 |  | Knight__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 526 |  | Knight__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 527 |  | Knight__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 528 |  | Knight__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 529 |  | Knight__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 530 |  | Knight__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 531 |  | Knight__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 532 |  | Knight__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 533 |  | Knight__vs__Wyvern__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 534 |  | Knight__vs__Ogre Boss x5__swarm__x5 | swarm | 5 | 10.72217747618977 | 0 | 0 | 0.0000 | ✅ |
| 535 |  | Knight__vs__Ogre Boss x5__swarm__x5 | swarm | 5 | 7.575698950969013 | 0 | 0 | 0.0000 | ✅ |
| 536 |  | Dark Shaman__vs__Ogre Boss__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 537 |  | Dark Shaman__vs__Ogre Boss__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 538 |  | Dark Shaman__vs__Ogre Boss__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 539 |  | Dark Shaman__vs__Ogre Boss__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 540 |  | Dark Shaman__vs__Ogre Boss__duel__x1 | duel | 1 | 5.0 | 0 | 0 | 0.0000 | ✅ |
| 541 |  | Dark Shaman__vs__Ogre Boss__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 542 |  | Dark Shaman__vs__Ogre Boss__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 543 |  | Dark Shaman__vs__Ogre Boss__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 544 |  | Dark Shaman__vs__Ogre Boss__duel__x1 | duel | 1 |  | 0 | 0 | 0.0000 | ✅ |
| 545 |  | Dark Shaman__vs__Ogre Boss__duel__x1 | duel | 1 |  | 0 | 1 | 1.0000 | ❌ |
| 546 |  | Tank__vs__Runner x3__swarm__x3 | swarm | 3 | 8.194493841100664 | 0 | 0 | 0.0000 | ✅ |
| 547 |  | Tank__vs__Runner x3__swarm__x3 | swarm | 3 | 10.828271842285824 | 0 | 0 | 0.0000 | ✅ |
| 548 |  | Tank__vs__Runner x3__swarm__x3 | swarm | 3 | 1.8038109870059174 | 0 | 0 | 0.0000 | ✅ |
| 549 |  | Tank__vs__Runner x3__swarm__x3 | swarm | 3 | 14.968472734721134 | 0 | 0 | 0.0000 | ✅ |
| 550 |  | Tank__vs__Runner x3__swarm__x3 | swarm | 3 | 1.6473009961941438 | 0 | 0 | 0.0000 | ✅ |
| 551 |  | Tank__vs__Runner x3__swarm__x3 | swarm | 3 | 9.5119679620204 | 0 | 0 | 0.0000 | ✅ |
| 552 |  | Tank__vs__Runner x3__swarm__x3 | swarm | 3 | 7.097129381878422 | 0 | 0 | 0.0000 | ✅ |

## Errors only

-  / pair=Wyvern__vs__Mage x8__swarm__x8 y=0 pred=1 p1=1.0
-  / pair=Goblin__vs__Archer__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Goblin__vs__Archer__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Knight__vs__Dark Shaman__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Ogre Boss__vs__AntiAir Tower__duel__x1 y=1 pred=0 p1=0.0
-  / pair=Ogre Boss__vs__AntiAir Tower__duel__x1 y=1 pred=0 p1=0.0
-  / pair=Tank__vs__Wyvern__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Tank__vs__Wyvern__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Tank__vs__Wyvern__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Tank__vs__Wyvern__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Tank__vs__Wyvern__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Tank__vs__Wyvern__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Dark Shaman__vs__AntiAir Tower__duel__x1 y=1 pred=0 p1=0.0
-  / pair=Archer__vs__Knight__duel__x1 y=1 pred=0 p1=0.0
-  / pair=Archer__vs__Knight__duel__x1 y=1 pred=0 p1=0.0
-  / pair=Archer__vs__Knight__duel__x1 y=1 pred=0 p1=0.0
-  / pair=Archer__vs__Knight__duel__x1 y=1 pred=0 p1=0.0
-  / pair=Archer__vs__Runner x8__swarm__x8 y=1 pred=0 p1=0.0
-  / pair=Armored Orc__vs__Archer__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Armored Orc__vs__Archer__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Wyvern__vs__Tank__duel__x1 y=1 pred=0 p1=0.0
-  / pair=Wyvern__vs__Tank__duel__x1 y=1 pred=0 p1=0.0
-  / pair=Wyvern__vs__Tank__duel__x1 y=1 pred=0 p1=0.0
-  / pair=Wyvern__vs__Mage__duel__x1 y=1 pred=0 p1=0.0
-  / pair=Wyvern__vs__Mage__duel__x1 y=1 pred=0 p1=0.0
-  / pair=Wyvern__vs__Mage__duel__x1 y=1 pred=0 p1=0.0
-  / pair=AntiAir Tower__vs__Tank__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Mage__vs__Goblin__duel__x1 y=0 pred=1 p1=1.0
-  / pair=AntiAir Tower__vs__Tank x3__swarm__x3 y=0 pred=1 p1=1.0
-  / pair=Armored Orc__vs__Knight__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Armored Orc__vs__Knight__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Armored Orc__vs__Knight__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Archer__vs__Knight x3__swarm__x3 y=1 pred=0 p1=0.0
-  / pair=Archer__vs__Dark Shaman__duel__x1 y=1 pred=0 p1=0.0
-  / pair=Runner__vs__AntiAir Tower x8__swarm__x8 y=1 pred=0 p1=0.0
-  / pair=Goblin__vs__Knight__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Mage__vs__Tank x3__swarm__x3 y=0 pred=1 p1=1.0
-  / pair=Knight__vs__Mage x3__swarm__x3 y=0 pred=1 p1=1.0
-  / pair=Knight__vs__Wyvern__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Knight__vs__Wyvern__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Knight__vs__Wyvern__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Knight__vs__Wyvern__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Knight__vs__Wyvern__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Knight__vs__Wyvern__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Knight__vs__Wyvern__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Knight__vs__Wyvern__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Knight__vs__Wyvern__duel__x1 y=0 pred=1 p1=1.0
-  / pair=Dark Shaman__vs__Ogre Boss__duel__x1 y=0 pred=1 p1=1.0
