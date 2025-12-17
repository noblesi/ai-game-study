# Scenario Summary Report

- Generated at: 2025-12-17 23:10:44
- Input records: 3 (scenario_preset: 3)
- Schema versions: legacy:3

---

## Overview

| Scenario | Runs | Total trials | Attacker win | Defender win | Draw | No result | Avg time (weighted) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 시나리오 1: Knight vs Goblin 1:1 | 1 | 100 | 100 | 0 | 0 | 0 | 6.00 |
| 시나리오 2: AntiAirTower vs Wyvern 1:1 | 1 | 100 | 100 | 0 | 0 | 0 | 5.00 |
| 시나리오 3: Assassin vs Giant 1:1 | 1 | 100 | 0 | 100 | 0 | 0 | 3.33 |

---

## Details

### 시나리오 1: Knight vs Goblin 1:1

- Runs: **1**
- Total trials (sum): **100**
- Win rates (overall): attacker **100.0%**, defender **0.0%**, draw **0.0%**, no_result **0.0%**
- Weighted averages: avg_time **6.00**, avg_attacker_final_hp **80.00**, avg_defender_final_hp **0.00**, avg_attacker_attacks **4.00**, avg_defender_attacks **5.00**

**Recent runs**

| logged_at | schema | engine | run_id | attacker | defender | trials | attacker_win_rate | avg_time |
|---|---|---|---|---|---|---:|---:|---:|
| 2025-12-16T22:32:23 | legacy | - | - | Knight | Goblin | 100 | 100.0% | 6.00 |

**Unit snapshot (most recent)**

- Attacker unit: `name=Knight, level=1, hp=120, atk=15, range=1, attack_speed=1.0, move_speed=0.0, target_type=ground, attack_type=melee, role=tower, cost=80`
- Defender unit: `name=Goblin, level=1, hp=60, atk=8, range=1, attack_speed=1.3, move_speed=1.8, target_type=tower, attack_type=melee, role=ground_enemy, cost=40`
- Positions: attacker [0.0, 0.0] / defender [5.0, 0.0]

### 시나리오 2: AntiAirTower vs Wyvern 1:1

- Runs: **1**
- Total trials (sum): **100**
- Win rates (overall): attacker **100.0%**, defender **0.0%**, draw **0.0%**, no_result **0.0%**
- Weighted averages: avg_time **5.00**, avg_attacker_final_hp **62.00**, avg_defender_final_hp **0.00**, avg_attacker_attacks **5.00**, avg_defender_attacks **2.00**

**Recent runs**

| logged_at | schema | engine | run_id | attacker | defender | trials | attacker_win_rate | avg_time |
|---|---|---|---|---|---|---:|---:|---:|
| 2025-12-16T22:46:45 | legacy | - | - | AntiAir Tower | Wyvern | 100 | 100.0% | 5.00 |

**Unit snapshot (most recent)**

- Attacker unit: `name=AntiAir Tower, level=1, hp=90, atk=22, range=5, attack_speed=1.0, move_speed=0.0, target_type=air, attack_type=ranged, role=tower, cost=130`
- Defender unit: `name=Wyvern, level=1, hp=90, atk=14, range=1, attack_speed=1.0, move_speed=2.0, target_type=tower, attack_type=melee, role=air_enemy, cost=110`
- Positions: attacker [0.0, 0.0] / defender [6.0, 0.0]

### 시나리오 3: Assassin vs Giant 1:1

- Runs: **1**
- Total trials (sum): **100**
- Win rates (overall): attacker **0.0%**, defender **100.0%**, draw **0.0%**, no_result **0.0%**
- Weighted averages: avg_time **3.33**, avg_attacker_final_hp **0.00**, avg_defender_final_hp **160.00**, avg_attacker_attacks **4.00**, avg_defender_attacks **2.00**

**Recent runs**

| logged_at | schema | engine | run_id | attacker | defender | trials | attacker_win_rate | avg_time |
|---|---|---|---|---|---|---:|---:|---:|
| 2025-12-16T22:47:00 | legacy | - | - | Assassin | Giant | 100 | 0.0% | 3.33 |

**Unit snapshot (most recent)**

- Attacker unit: `name=Assassin, level=1, hp=80, atk=35, range=1, attack_speed=1.8, move_speed=1.8, target_type=ground, attack_type=melee, role=ground, cost=0`
- Defender unit: `name=Giant, level=1, hp=300, atk=60, range=1, attack_speed=0.6, move_speed=0.6, target_type=ground, attack_type=melee, role=ground, cost=0`
- Positions: attacker [0.0, 0.0] / defender [4.0, 0.0]

