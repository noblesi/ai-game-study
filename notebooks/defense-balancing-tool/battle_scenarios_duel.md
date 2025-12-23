### battle_scenarios_duel (1v1 / duel)

- **SSOT(단일 진실):** 유닛 스탯은 `units.json`을 사용합니다.
- 이 파일은 스탯을 들고 있지 않고, **유닛 이름 참조 + 전투 메타(duel/swarm, trials, 위치 등)** 만 가집니다.
- 향후 유닛/Perk가 추가되어도, 이 파일은 보통 **새 프리셋(매치업)만 추가**하면 됩니다.

```json
{
  "title": "D1: Knight vs Goblin (duel)",
  "encounter_type": "duel",
  "defender_count": 1,

  "attacker_name": "Knight",
  "defender_name": "Goblin",

  "attacker_level": 1,
  "defender_level": 1,

  "trials": 200,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [5.0, 0.0],
  "verbose_each": false
}
```
```json
{
  "title": "D2: Archer vs Runner (duel)",
  "encounter_type": "duel",
  "defender_count": 1,

  "attacker_name": "Archer",
  "defender_name": "Runner",

  "attacker_level": 1,
  "defender_level": 1,

  "trials": 200,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [6.0, 0.0],
  "verbose_each": false
}
```
```json
{
  "title": "D3: AntiAir Tower vs Wyvern (duel)",
  "encounter_type": "duel",
  "defender_count": 1,

  "attacker_name": "AntiAir Tower",
  "defender_name": "Wyvern",

  "attacker_level": 1,
  "defender_level": 1,

  "trials": 200,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [7.0, 0.0],
  "verbose_each": false
}
```
```json
{
  "title": "D4: Mage vs Armored Orc (duel)",
  "encounter_type": "duel",
  "defender_count": 1,

  "attacker_name": "Mage",
  "defender_name": "Armored Orc",

  "attacker_level": 1,
  "defender_level": 1,

  "trials": 200,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [5.5, 0.0],
  "verbose_each": false
}
```
```json
{
  "title": "D5: Tank vs Ogre Boss (duel)",
  "encounter_type": "duel",
  "defender_count": 1,

  "attacker_name": "Tank",
  "defender_name": "Ogre Boss",

  "attacker_level": 1,
  "defender_level": 1,

  "trials": 200,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [4.5, 0.0],
  "verbose_each": false
}
```