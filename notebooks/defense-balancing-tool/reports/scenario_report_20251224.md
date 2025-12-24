# Scenario Summary Report

- Generated at: 2025-12-24 17:50:02
- Input records: 9 (scenario_preset: 9)
- Schema versions: v1:9

---

## Overview

| Scenario | Runs | Total trials | Attacker win | Defender win | Draw | No result | Avg time (weighted) |
|---|---:|---:|---:|---:|---:|---:|---:|
| D1: Knight vs Goblin (duel) | 1 | 200 | 200 | 0 | 0 | 0 | 6.00 |
| D2: Archer vs Runner (duel) | 1 | 200 | 200 | 0 | 0 | 0 | 1.67 |
| D3: AntiAir Tower vs Wyvern (duel) | 1 | 200 | 200 | 0 | 0 | 0 | 6.00 |
| D4: Mage vs Armored Orc (duel) | 1 | 200 | 200 | 0 | 0 | 0 | 11.11 |
| D5: Tank vs Ogre Boss (duel) | 1 | 200 | 0 | 200 | 0 | 0 | 20.00 |
| S1: Knight vs Goblin x4 (swarm) | 1 | 200 | 0 | 200 | 0 | 0 | 4.62 |
| S2: AntiAir Tower vs Wyvern x3 (swarm) | 1 | 200 | 0 | 200 | 0 | 0 | 6.00 |
| S3: Mage vs Runner x5 (swarm) | 1 | 200 | 0 | 200 | 0 | 0 | 4.00 |
| S4: Archer vs Goblin x6 (swarm) | 1 | 200 | 0 | 200 | 0 | 0 | 4.62 |

---

## Details

### D1: Knight vs Goblin (duel)

- Runs: **1**
- Total trials (sum): **200**
- Win rates (overall): attacker **100.0%**, defender **0.0%**, draw **0.0%**, no_result **0.0%**
- Weighted averages: avg_time **6.00**, avg_attacker_final_hp **80.00**, avg_defender_final_hp **0.00**, avg_attacker_attacks **4.00**, avg_defender_attacks **5.00**

**Recent runs**

| logged_at | schema | engine | run_id | attacker | defender | trials | attacker_win_rate | avg_time |
|---|---|---|---|---|---|---:|---:|---:|
| 2025-12-23T19:50:25 | v1 | run_duel_trials_2d | 864675c4 | Knight | Goblin | 200 | 100.0% | 6.00 |

**Unit snapshot (most recent)**

- Attacker unit: `name=Knight, level=1, hp=120, atk=15, range=1, attack_speed=1.0, move_speed=0.0, target_type=ground, attack_type=melee, role=tower, cost=80`
- Defender unit: `name=Goblin, level=1, hp=60, atk=8, range=1, attack_speed=1.3, move_speed=1.8, target_type=tower, attack_type=melee, role=ground_enemy, cost=40`
- Positions: attacker [0.0, 0.0] / defender [5.0, 0.0]

### D2: Archer vs Runner (duel)

- Runs: **1**
- Total trials (sum): **200**
- Win rates (overall): attacker **100.0%**, defender **0.0%**, draw **0.0%**, no_result **0.0%**
- Weighted averages: avg_time **1.67**, avg_attacker_final_hp **80.00**, avg_defender_final_hp **0.00**, avg_attacker_attacks **2.00**, avg_defender_attacks **0.00**

**Recent runs**

| logged_at | schema | engine | run_id | attacker | defender | trials | attacker_win_rate | avg_time |
|---|---|---|---|---|---|---:|---:|---:|
| 2025-12-23T19:50:30 | v1 | run_duel_trials_2d | a22c1fc2 | Archer | Runner | 200 | 100.0% | 1.67 |

**Unit snapshot (most recent)**

- Attacker unit: `name=Archer, level=1, hp=80, atk=20, range=4, attack_speed=1.2, move_speed=0.0, target_type=both, attack_type=ranged, role=tower, cost=100`
- Defender unit: `name=Runner, level=1, hp=40, atk=6, range=1, attack_speed=1.5, move_speed=2.5, target_type=tower, attack_type=melee, role=ground_enemy, cost=35`
- Positions: attacker [0.0, 0.0] / defender [6.0, 0.0]

### D3: AntiAir Tower vs Wyvern (duel)

- Runs: **1**
- Total trials (sum): **200**
- Win rates (overall): attacker **100.0%**, defender **0.0%**, draw **0.0%**, no_result **0.0%**
- Weighted averages: avg_time **6.00**, avg_attacker_final_hp **62.00**, avg_defender_final_hp **0.00**, avg_attacker_attacks **5.00**, avg_defender_attacks **2.00**

**Recent runs**

| logged_at | schema | engine | run_id | attacker | defender | trials | attacker_win_rate | avg_time |
|---|---|---|---|---|---|---:|---:|---:|
| 2025-12-23T19:50:35 | v1 | run_duel_trials_2d | 6f63ba2e | AntiAir Tower | Wyvern | 200 | 100.0% | 6.00 |

**Unit snapshot (most recent)**

- Attacker unit: `name=AntiAir Tower, level=1, hp=90, atk=22, range=5, attack_speed=1.0, move_speed=0.0, target_type=air, attack_type=ranged, role=tower, cost=130`
- Defender unit: `name=Wyvern, level=1, hp=90, atk=14, range=1, attack_speed=1.0, move_speed=2.0, target_type=tower, attack_type=melee, role=air_enemy, cost=110`
- Positions: attacker [0.0, 0.0] / defender [7.0, 0.0]

### D4: Mage vs Armored Orc (duel)

- Runs: **1**
- Total trials (sum): **200**
- Win rates (overall): attacker **100.0%**, defender **0.0%**, draw **0.0%**, no_result **0.0%**
- Weighted averages: avg_time **11.11**, avg_attacker_final_hp **10.00**, avg_defender_final_hp **0.00**, avg_attacker_attacks **8.00**, avg_defender_attacks **5.00**

**Recent runs**

| logged_at | schema | engine | run_id | attacker | defender | trials | attacker_win_rate | avg_time |
|---|---|---|---|---|---|---:|---:|---:|
| 2025-12-23T19:50:41 | v1 | run_duel_trials_2d | 9c4ad10f | Mage | Armored Orc | 200 | 100.0% | 11.11 |

**Unit snapshot (most recent)**

- Attacker unit: `name=Mage, level=1, hp=70, atk=25, range=3, attack_speed=0.9, move_speed=0.0, target_type=ground, attack_type=magic, role=tower, cost=120`
- Defender unit: `name=Armored Orc, level=1, hp=180, atk=12, range=1, attack_speed=0.8, move_speed=1.0, target_type=tower, attack_type=melee, role=ground_enemy, cost=90`
- Positions: attacker [0.0, 0.0] / defender [5.5, 0.0]

### D5: Tank vs Ogre Boss (duel)

- Runs: **1**
- Total trials (sum): **200**
- Win rates (overall): attacker **0.0%**, defender **100.0%**, draw **0.0%**, no_result **0.0%**
- Weighted averages: avg_time **20.00**, avg_attacker_final_hp **0.00**, avg_defender_final_hp **290.00**, avg_attacker_attacks **11.00**, avg_defender_attacks **10.00**

**Recent runs**

| logged_at | schema | engine | run_id | attacker | defender | trials | attacker_win_rate | avg_time |
|---|---|---|---|---|---|---:|---:|---:|
| 2025-12-23T19:50:48 | v1 | run_duel_trials_2d | 26772022 | Tank | Ogre Boss | 200 | 0.0% | 20.00 |

**Unit snapshot (most recent)**

- Attacker unit: `name=Tank, level=1, hp=200, atk=10, range=1, attack_speed=0.7, move_speed=0.0, target_type=ground, attack_type=melee, role=tower, cost=150`
- Defender unit: `name=Ogre Boss, level=1, hp=400, atk=20, range=1, attack_speed=0.6, move_speed=0.8, target_type=tower, attack_type=melee, role=boss_enemy, cost=200`
- Positions: attacker [0.0, 0.0] / defender [4.5, 0.0]

### S1: Knight vs Goblin x4 (swarm)

- Runs: **1**
- Total trials (sum): **200**
- Win rates (overall): attacker **0.0%**, defender **100.0%**, draw **0.0%**, no_result **0.0%**
- Weighted averages: avg_time **4.62**, avg_attacker_final_hp **0.00**, avg_defender_final_hp **210.00**, avg_attacker_attacks **2.00**, avg_defender_attacks **4.00**

**Recent runs**

| logged_at | schema | engine | run_id | attacker | defender | trials | attacker_win_rate | avg_time |
|---|---|---|---|---|---|---:|---:|---:|
| 2025-12-23T19:51:03 | v1 | run_swarm_trials_2d | efa84a21 | Knight | Goblin x4 | 200 | 0.0% | 4.62 |

**Unit snapshot (most recent)**

- Attacker unit: `name=Knight, level=1, hp=120, atk=15, range=1, attack_speed=1.0, move_speed=0.0, target_type=ground, attack_type=melee, role=tower, cost=80`
- Defender unit: `name=Goblin x4, level=1, hp=240, atk=32, range=1, attack_speed=1.3, move_speed=1.8, target_type=tower, attack_type=melee, role=ground_enemy, cost=160`
- Positions: attacker [0.0, 0.0] / defender [5.0, 0.0]

### S2: AntiAir Tower vs Wyvern x3 (swarm)

- Runs: **1**
- Total trials (sum): **200**
- Win rates (overall): attacker **0.0%**, defender **100.0%**, draw **0.0%**, no_result **0.0%**
- Weighted averages: avg_time **6.00**, avg_attacker_final_hp **0.00**, avg_defender_final_hp **160.00**, avg_attacker_attacks **5.00**, avg_defender_attacks **3.00**

**Recent runs**

| logged_at | schema | engine | run_id | attacker | defender | trials | attacker_win_rate | avg_time |
|---|---|---|---|---|---|---:|---:|---:|
| 2025-12-23T19:51:15 | v1 | run_swarm_trials_2d | 122a3161 | AntiAir Tower | Wyvern x3 | 200 | 0.0% | 6.00 |

**Unit snapshot (most recent)**

- Attacker unit: `name=AntiAir Tower, level=1, hp=90, atk=22, range=5, attack_speed=1.0, move_speed=0.0, target_type=air, attack_type=ranged, role=tower, cost=130`
- Defender unit: `name=Wyvern x3, level=1, hp=270, atk=42, range=1, attack_speed=1.0, move_speed=2.0, target_type=tower, attack_type=melee, role=air_enemy, cost=330`
- Positions: attacker [0.0, 0.0] / defender [7.0, 0.0]

### S3: Mage vs Runner x5 (swarm)

- Runs: **1**
- Total trials (sum): **200**
- Win rates (overall): attacker **0.0%**, defender **100.0%**, draw **0.0%**, no_result **0.0%**
- Weighted averages: avg_time **4.00**, avg_attacker_final_hp **0.00**, avg_defender_final_hp **150.00**, avg_attacker_attacks **2.00**, avg_defender_attacks **3.00**

**Recent runs**

| logged_at | schema | engine | run_id | attacker | defender | trials | attacker_win_rate | avg_time |
|---|---|---|---|---|---|---:|---:|---:|
| 2025-12-23T19:51:20 | v1 | run_swarm_trials_2d | 0e74d912 | Mage | Runner x5 | 200 | 0.0% | 4.00 |

**Unit snapshot (most recent)**

- Attacker unit: `name=Mage, level=1, hp=70, atk=25, range=3, attack_speed=0.9, move_speed=0.0, target_type=ground, attack_type=magic, role=tower, cost=120`
- Defender unit: `name=Runner x5, level=1, hp=200, atk=30, range=1, attack_speed=1.5, move_speed=2.5, target_type=tower, attack_type=melee, role=ground_enemy, cost=175`
- Positions: attacker [0.0, 0.0] / defender [6.0, 0.0]

### S4: Archer vs Goblin x6 (swarm)

- Runs: **1**
- Total trials (sum): **200**
- Win rates (overall): attacker **0.0%**, defender **100.0%**, draw **0.0%**, no_result **0.0%**
- Weighted averages: avg_time **4.62**, avg_attacker_final_hp **0.00**, avg_defender_final_hp **300.00**, avg_attacker_attacks **3.00**, avg_defender_attacks **2.00**

**Recent runs**

| logged_at | schema | engine | run_id | attacker | defender | trials | attacker_win_rate | avg_time |
|---|---|---|---|---|---|---:|---:|---:|
| 2025-12-23T19:51:27 | v1 | run_swarm_trials_2d | 061303a4 | Archer | Goblin x6 | 200 | 0.0% | 4.62 |

**Unit snapshot (most recent)**

- Attacker unit: `name=Archer, level=1, hp=80, atk=20, range=4, attack_speed=1.2, move_speed=0.0, target_type=both, attack_type=ranged, role=tower, cost=100`
- Defender unit: `name=Goblin x6, level=1, hp=360, atk=48, range=1, attack_speed=1.3, move_speed=1.8, target_type=tower, attack_type=melee, role=ground_enemy, cost=240`
- Positions: attacker [0.0, 0.0] / defender [7.0, 0.0]

