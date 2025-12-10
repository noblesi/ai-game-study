### 시나리오 3: Assassin vs Giant 1:1

### 목적
- 고속/저체력 암살자(Assassin)와
  저속/고체력/고공격력 유닛(Giant)의 상성을 확인.
- move_speed, attack_speed, range의 상호작용을 테스트.

### 유닛 설정
- 공격자(Attacker)
  - 이름: Assassin
  - 레벨: 1
  - hp / atk: 80 / 35
  - role: ground
  - range: 1
  - attack_speed: 1.8   # 매우 빠른 공격 속도
  - move_speed: 1.8     # 빠른 이동
  - target_type: ground
  - attack_type: melee
- 방어자(Defender)
  - 이름: Giant
  - 레벨: 1
  - hp / atk: 300 / 60
  - role: ground
  - range: 1
  - attack_speed: 0.6   # 느린 공격 속도
  - move_speed: 0.6
  - target_type: ground
  - attack_type: melee

### 시뮬레이션 설정
- 사용 함수: simulate_duel_2d
- 초기 위치:
  - attacker_pos: (0.0, 0.0)
  - defender_pos: (4.0, 0.0)
- 실험 횟수(trials): 100
- verbose_each: False

### 관심 지표
- Assassin 승률 / Giant 승률
- 평균 전투 시간
- Assassin 평균 남은 HP
- Giant가 공격을 몇 번이나 적중시키는지 (평균 공격 횟수)

### 메모
- 목표 예시: Assassin 승률 55~65% 정도를 목표로 파라미터 튜닝 가능.
- Giant가 너무 못 이기면 Giant hp/atk 상향, 또는 Assassin hp/atk/속도 조정.
