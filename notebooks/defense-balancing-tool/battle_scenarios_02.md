### 시나리오 2: AntiAirTower vs Wyvern 1:1

### 목적
- 대공 전용 타워(AntiAirTower)가 공중 유닛(Wyvern)을 얼마나 안정적으로 처치하는지 확인.
- target_type, attack_type 설정이 잘 작동하는지 검증.

### 유닛 설정
- 공격자(Attacker)
  - 이름: AntiAirTower
  - 레벨: 1
  - hp / atk: 150 / 40
  - role: tower
  - range: 4         # 긴 사거리
  - attack_speed: 0.8
  - move_speed: 0.0  # 고정식 타워
  - target_type: air
  - attack_type: ranged
- 방어자(Defender)
  - 이름: Wyvern
  - 레벨: 1
  - hp / atk: 180 / 30
  - role: air
  - range: 1
  - attack_speed: 1.0
  - move_speed: 1.5
  - target_type: ground
  - attack_type: melee

### 시뮬레이션 설정
- 사용 함수: simulate_duel_2d
- 초기 위치:
  - attacker_pos: (0.0, 0.0)
  - defender_pos: (6.0, 0.0)
- 실험 횟수(trials): 100
- verbose_each: False

### 관심 지표
- AntiAirTower 승률
- 평균 전투 시간
- Wyvern이 타워에 한 번이라도 닿아서 공격하는 비율

### 메모
- 지상 타워가 air만 때리게 설정되어 있다면,
  일반 ground-only 타워는 Wyvern을 전혀 못 때리는지도 별도 실험으로 확인 가능.
