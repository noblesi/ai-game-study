### 시나리오 3: Assassin vs Giant 1:1

### 목적
- 고속/저체력 암살자(Assassin) vs 저속/고체력/고공격력(Giant) 상성을 확인
- move_speed/attack_speed/range 상호작용 테스트

### 시나리오 스펙(JSON)
```json
{
  "title": "시나리오 3: Assassin vs Giant 1:1",
  "attacker_spec": {
    "name": "Assassin",
    "level": 1,
    "hp": 80,
    "atk": 35,
    "role": "ground",
    "range": 1,
    "attack_speed": 1.8,
    "move_speed": 1.8,
    "target_type": "ground",
    "attack_type": "melee"
  },
  "defender_spec": {
    "name": "Giant",
    "level": 1,
    "hp": 300,
    "atk": 60,
    "role": "ground",
    "range": 1,
    "attack_speed": 0.6,
    "move_speed": 0.6,
    "target_type": "ground",
    "attack_type": "melee"
  },
  "trials": 100,
  "attacker_pos": [
    0.0,
    0.0
  ],
  "defender_pos": [
    4.0,
    0.0
  ],
  "verbose_each": false
}
```

### 유닛 설정
- 공격자(Attacker)
  - name: Assassin
  - level: 1
  - hp: 80
  - atk: 35
  - role: ground
  - range: 1
  - attack_speed: 1.8
  - move_speed: 1.8
  - target_type: ground
  - attack_type: melee
- 방어자(Defender)
  - name: Giant
  - level: 1
  - hp: 300
  - atk: 60
  - role: ground
  - range: 1
  - attack_speed: 0.6
  - move_speed: 0.6
  - target_type: ground
  - attack_type: melee

### 초기 위치
- attacker_pos: (0.0, 0.0)
- defender_pos: (4.0, 0.0)
- 실험 횟수(trials): 100
- verbose_each: False

### 관심 지표
- Assassin 승률 / Giant 승률
- 평균 전투 시간
- Assassin 평균 남은 HP
- Giant 평균 공격 횟수(적중 횟수)

### 메모
- 목표 예시: Assassin 승률 55~65% 정도면 튜닝 여지
- Giant가 너무 못 이기면 Giant hp/atk 상향 또는 Assassin 스탯 조정
