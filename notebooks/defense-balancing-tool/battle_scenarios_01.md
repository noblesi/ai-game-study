### 시나리오 1: Knight vs Goblin 1:1

### 목적
- 근접 탱커(Knight)가 일반 근접 잡몹(Goblin)을 상대로
  압도적으로 이기는지, 간신히 이기는지, 역전도 자주 나는지 확인.
- 기본 근접 전투 밸런스 기준점 잡기.

### 유닛 설정
- 공격자(Attacker)
  - 이름: Knight
  - 레벨: 1
  - hp / atk: 200 / 25
  - role: defender
  - range: 1
  - attack_speed: 1.0   # 초당 1회 공격
  - move_speed: 1.0
  - target_type: ground
  - attack_type: melee
- 방어자(Defender)
  - 이름: Goblin
  - 레벨: 1
  - hp / atk: 100 / 15
  - role: ground
  - range: 1
  - attack_speed: 1.2   # 살짝 더 빠름
  - move_speed: 1.2
  - target_type: ground
  - attack_type: melee

### 시뮬레이션 설정
- 사용 함수: simulate_duel_2d
- 초기 위치:
  - attacker_pos: (0.0, 0.0)
  - defender_pos: (5.0, 0.0)
- 실험 횟수(trials): 100
- verbose_each: False

### 관심 지표
- Knight 승률 / Goblin 승률
- 평균 전투 시간
- Knight 평균 남은 HP

### 메모
- 목표: Knight 승률이 70~80% 정도면 적당하다고 가정.
- 너무 100%면 Goblin이 너무 약한 것, 50% 언저리면 Knight가 약한 것.
