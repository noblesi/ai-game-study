### 시나리오 4: Knight vs Goblin 1:4 (Swarm)

### 목적
- 1vN(스웜) 상황에서 근접 탱커(Knight)가 다수를 상대로 버티는지 확인
- 이후 perk(광역/관통/실드/넉백 등) 설계/검증을 위한 기본 스웜 기준점 마련

### 시나리오 스펙(JSON)
```json
{
  "title": "시나리오 4: Knight vs Goblin 1:4 (Swarm)",
  "encounter_type": "swarm",
  "defender_count": 4,
  "attacker_spec": {
    "name": "Knight",
    "level": 1,
    "hp": 200,
    "atk": 25,
    "role": "defender",
    "range": 1,
    "attack_speed": 1.0,
    "move_speed": 1.0,
    "target_type": "ground",
    "attack_type": "melee"
  },
  "defender_spec": {
    "name": "Goblin",
    "level": 1,
    "hp": 100,
    "atk": 15,
    "role": "ground",
    "range": 1,
    "attack_speed": 1.2,
    "move_speed": 1.2,
    "target_type": "ground",
    "attack_type": "melee"
  },
  "trials": 100,
  "attacker_pos": [
    0.0,
    0.0
  ],
  "defender_pos": [
    5.0,
    0.0
  ],
  "defender_spread": 1.2,
  "verbose_each": false
}
```

### 메모
- `defender_pos`는 스웜의 기준 위치(중심)으로 쓰고,
  `defender_spread` 반경 안에서 `defender_count`만큼 랜덤 스폰하는 형태를 권장

---

### 시나리오 5: AntiAirTower vs Wyvern 1:3 (Swarm)

### 목적
- 1vN에서 타워(고정) vs 공중 유닛 다수 접근 시나리오를 만들기
- 이후 perk(연쇄/광역/대공 특화 등) 실험 기반 마련

### 시나리오 스펙(JSON)
```json
{
  "title": "시나리오 5: AntiAirTower vs Wyvern 1:3 (Swarm)",
  "encounter_type": "swarm",
  "defender_count": 3,
  "attacker_spec": {
    "name": "AntiAirTower",
    "level": 1,
    "hp": 150,
    "atk": 40,
    "role": "tower",
    "range": 4,
    "attack_speed": 0.8,
    "move_speed": 0.0,
    "target_type": "air",
    "attack_type": "ranged"
  },
  "defender_spec": {
    "name": "Wyvern",
    "level": 1,
    "hp": 180,
    "atk": 30,
    "role": "air_enemy",
    "range": 1,
    "attack_speed": 1.0,
    "move_speed": 1.5,
    "target_type": "tower",
    "attack_type": "melee"
  },
  "trials": 100,
  "attacker_pos": [
    0.0,
    0.0
  ],
  "defender_pos": [
    6.0,
    0.0
  ],
  "defender_spread": 1.5,
  "verbose_each": false
}
```

### 메모
- 스웜에서는 보통 "defender들이 서로 겹치지 않게" 초기 위치 분산이 필요해서 spread 값을 둠
