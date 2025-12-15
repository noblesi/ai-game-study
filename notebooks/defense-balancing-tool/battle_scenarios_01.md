### 시나리오 1: Knight vs Goblin 1:1

### 목적
- 근접 탱커(Knight)가 일반 근접 잡몹(Goblin)을 상대로 얼마나 안정적으로 이기는지 확인
- 기본 근접 전투 밸런스 기준점 잡기

### 시나리오 스펙(JSON)
```json
{
  "title": "시나리오 1: Knight vs Goblin 1:1",
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
  "verbose_each": false
}
```

### 유닛 설정
- 공격자(Attacker)
  - name: Knight
  - level: 1
  - hp: 200
  - atk: 25
  - role: defender
  - range: 1
  - attack_speed: 1.0
  - move_speed: 1.0
  - target_type: ground
  - attack_type: melee
- 방어자(Defender)
  - name: Goblin
  - level: 1
  - hp: 100
  - atk: 15
  - role: ground
  - range: 1
  - attack_speed: 1.2
  - move_speed: 1.2
  - target_type: ground
  - attack_type: melee

### 초기 위치
- attacker_pos: (0.0, 0.0)
- defender_pos: (5.0, 0.0)
- 실험 횟수(trials): 100
- verbose_each: False

### 관심 지표
- Knight 승률 / Goblin 승률
- 평균 전투 시간
- Knight 평균 남은 HP

### 메모
- 목표 예시: Knight 승률 70~80%면 적당
- 너무 100%면 Goblin이 너무 약한 것, 50% 언저리면 Knight가 약한 것
