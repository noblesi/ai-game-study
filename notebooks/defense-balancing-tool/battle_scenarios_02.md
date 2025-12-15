### 시나리오 2: AntiAirTower vs Wyvern 1:1

### 목적
- 대공 전용 타워(AntiAirTower)가 공중 유닛(Wyvern)을 얼마나 안정적으로 처치하는지 확인
- target_type/attack_type 설정이 의도대로 동작하는지 검증

### 시나리오 스펙(JSON)
```json
{
  "title": "시나리오 2: AntiAirTower vs Wyvern 1:1",
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
  "verbose_each": false
}
```

### 유닛 설정
- 공격자(Attacker)
  - name: AntiAirTower
  - level: 1
  - hp: 150
  - atk: 40
  - role: tower
  - range: 4
  - attack_speed: 0.8
  - move_speed: 0.0
  - target_type: air
  - attack_type: ranged
- 방어자(Defender)
  - name: Wyvern
  - level: 1
  - hp: 180
  - atk: 30
  - role: air_enemy
  - range: 1
  - attack_speed: 1.0
  - move_speed: 1.5
  - target_type: tower
  - attack_type: melee

### 초기 위치
- attacker_pos: (0.0, 0.0)
- defender_pos: (6.0, 0.0)
- 실험 횟수(trials): 100
- verbose_each: False

### 관심 지표
- AntiAirTower 승률
- 평균 전투 시간
- Wyvern이 타워에 닿아서 공격 성공하는 비율(또는 공격 횟수)

### 메모
- 일반 ground-only 타워가 Wyvern을 전혀 못 때리는지도 별도 실험으로 확인 가능
