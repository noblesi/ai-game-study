### battle_scenarios_swarm (1vN / swarm)

- **SSOT(단일 진실):** 유닛 스탯은 `units.json`을 사용합니다.
- 이 파일은 스탯을 들고 있지 않고, **유닛 이름 참조 + 전투 메타(duel/swarm, defender_count 등)** 만 가집니다.
- `defender_count`만큼 defender 유닛을 스폰한다고 가정합니다.
- `defender_spread`는 defender 스폰을 분산시키는 힌트 값(예: 반경/간격)으로 사용합니다.

```json
{
  "title": "S1: Knight vs Goblin x4 (swarm)",
  "encounter_type": "swarm",

  "attacker_name": "Knight",
  "defender_name": "Goblin",

  "attacker_level": 1,
  "defender_level": 1,

  "defender_count": 4,
  "defender_spread": 1.5,

  "trials": 200,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [5.0, 0.0],
  "verbose_each": false
}
```
```json
{
  "title": "S2: AntiAir Tower vs Wyvern x3 (swarm)",
  "encounter_type": "swarm",

  "attacker_name": "AntiAir Tower",
  "defender_name": "Wyvern",

  "attacker_level": 1,
  "defender_level": 1,

  "defender_count": 3,
  "defender_spread": 2.0,

  "trials": 200,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [7.0, 0.0],
  "verbose_each": false
}
```
```json
{
  "title": "S3: Mage vs Runner x5 (swarm)",
  "encounter_type": "swarm",

  "attacker_name": "Mage",
  "defender_name": "Runner",

  "attacker_level": 1,
  "defender_level": 1,

  "defender_count": 5,
  "defender_spread": 3.0,

  "trials": 200,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [6.0, 0.0],
  "verbose_each": false
}
```
```json
{
  "title": "S4: Archer vs Goblin x6 (swarm)",
  "encounter_type": "swarm",

  "attacker_name": "Archer",
  "defender_name": "Goblin",

  "attacker_level": 1,
  "defender_level": 1,

  "defender_count": 6,
  "defender_spread": 3.5,

  "trials": 200,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [7.0, 0.0],
  "verbose_each": false
}
```
```json
{
  "title": "S5: Tank vs Goblin x8 (swarm)",
  "encounter_type": "swarm",

  "attacker_name": "Tank",
  "defender_name": "Goblin",

  "attacker_level": 1,
  "defender_level": 1,

  "defender_count": 8,
  "defender_spread": 4.0,

  "trials": 200,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [5.5, 0.0],
  "verbose_each": false
}
```
```json
{
  "title": "S6) Archer vs Goblin Swarm x3",
  "encounter_type": "swarm",
  "attacker_name": "Archer Tower",
  "attacker_level": 1,
  "defender_name": "Goblin",
  "defender_level": 1,
  "defender_count": 3,
  "defender_spread": 2.0,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [7.0, 0.0]
}
```
```json
{
  "title": "S7) Mage vs Goblin Swarm x5",
  "encounter_type": "swarm",
  "attacker_name": "Mage Tower",
  "attacker_level": 1,
  "defender_name": "Goblin",
  "defender_level": 1,
  "defender_count": 5,
  "defender_spread": 2.0,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [7.0, 0.0]
}
```
```json
{
  "title": "S8) Knight vs Runner Swarm x4",
  "encounter_type": "swarm",
  "attacker_name": "Knight Tower",
  "attacker_level": 1,
  "defender_name": "Runner",
  "defender_level": 1,
  "defender_count": 4,
  "defender_spread": 2.5,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [6.0, 0.0]
}
```
```json
{
  "title": "S9) AntiAir vs Wyvern Swarm x3",
  "encounter_type": "swarm",
  "attacker_name": "AntiAir Tower",
  "attacker_level": 1,
  "defender_name": "Wyvern",
  "defender_level": 1,
  "defender_count": 3,
  "defender_spread": 2.0,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [8.0, 0.0]
}
```
```json
{
  "title": "S10) AntiAir vs Goblin Swarm x4 (target mismatch sanity)",
  "encounter_type": "swarm",
  "attacker_name": "AntiAir Tower",
  "attacker_level": 1,
  "defender_name": "Goblin",
  "defender_level": 1,
  "defender_count": 4,
  "defender_spread": 2.0,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [7.0, 0.0]
}
```
```json
{
  "title": "S11) Archer vs Wyvern Swarm x4",
  "encounter_type": "swarm",
  "attacker_name": "Archer Tower",
  "attacker_level": 1,
  "defender_name": "Wyvern",
  "defender_level": 1,
  "defender_count": 4,
  "defender_spread": 2.5,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [9.0, 0.0]
}
```
```json
{
  "title": "S12) Mage vs Wyvern Swarm x2 (target mismatch sanity)",
  "encounter_type": "swarm",
  "attacker_name": "Mage Tower",
  "attacker_level": 1,
  "defender_name": "Wyvern",
  "defender_level": 1,
  "defender_count": 2,
  "defender_spread": 2.0,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [7.0, 0.0]
}
```
```json
{
  "title": "S13) Tank vs Dark Shaman Swarm x2",
  "encounter_type": "swarm",
  "attacker_name": "Tank Tower",
  "attacker_level": 1,
  "defender_name": "Dark Shaman",
  "defender_level": 1,
  "defender_count": 2,
  "defender_spread": 2.0,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [8.0, 0.0]
}
```
```json
{
  "title": "S14) Archer(Lv6) vs Runner(Lv6) Swarm x5",
  "encounter_type": "swarm",
  "attacker_name": "Archer Tower",
  "attacker_level": 6,
  "defender_name": "Runner",
  "defender_level": 6,
  "defender_count": 5,
  "defender_spread": 2.5,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [8.0, 0.0]
}
```
```json
{
  "title": "S15) Mage(Lv10) vs Armored Orc(Lv10) Swarm x3",
  "encounter_type": "swarm",
  "attacker_name": "Mage Tower",
  "attacker_level": 10,
  "defender_name": "Armored Orc",
  "defender_level": 10,
  "defender_count": 3,
  "defender_spread": 2.5,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [9.0, 0.0]
}
