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
```json
{
  "title": "D6) Archer vs Runner (close start)",
  "encounter_type": "duel",
  "attacker_name": "Archer Tower",
  "attacker_level": 1,
  "defender_name": "Runner",
  "defender_level": 1,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [3.0, 0.0]
}
```
```json
{
  "title": "D7) Archer vs Runner (far start)",
  "encounter_type": "duel",
  "attacker_name": "Archer Tower",
  "attacker_level": 1,
  "defender_name": "Runner",
  "defender_level": 1,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [9.0, 0.0]
}
```
```json
{
  "title": "D8) Archer vs Goblin (mid start)",
  "encounter_type": "duel",
  "attacker_name": "Archer Tower",
  "attacker_level": 1,
  "defender_name": "Goblin",
  "defender_level": 1,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [6.0, 0.0]
}
```
```json
{
  "title": "D9) Mage vs Runner (mid start)",
  "encounter_type": "duel",
  "attacker_name": "Mage Tower",
  "attacker_level": 1,
  "defender_name": "Runner",
  "defender_level": 1,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [6.0, 0.0]
}
```
```json
{
  "title": "D10) Mage vs Runner (very far start)",
  "encounter_type": "duel",
  "attacker_name": "Mage Tower",
  "attacker_level": 1,
  "defender_name": "Runner",
  "defender_level": 1,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [10.0, 0.0]
}
```
```json
{
  "title": "D11) Archer vs Dark Shaman (mid start)",
  "encounter_type": "duel",
  "attacker_name": "Archer Tower",
  "attacker_level": 1,
  "defender_name": "Dark Shaman",
  "defender_level": 1,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [6.0, 0.0]
}
```
```json
{
  "title": "D12) Mage vs Dark Shaman (mid start)",
  "encounter_type": "duel",
  "attacker_name": "Mage Tower",
  "attacker_level": 1,
  "defender_name": "Dark Shaman",
  "defender_level": 1,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [6.0, 0.0]
}
```
```json
{
  "title": "D13) Knight vs Dark Shaman (close start)",
  "encounter_type": "duel",
  "attacker_name": "Knight Tower",
  "attacker_level": 1,
  "defender_name": "Dark Shaman",
  "defender_level": 1,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [3.0, 0.0]
}
```
```json
{
  "title": "D14) AntiAir vs Goblin (target mismatch sanity)",
  "encounter_type": "duel",
  "attacker_name": "AntiAir Tower",
  "attacker_level": 1,
  "defender_name": "Goblin",
  "defender_level": 1,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [6.0, 0.0]
}
```
```json
{
  "title": "D15) Mage vs Wyvern (target mismatch sanity)",
  "encounter_type": "duel",
  "attacker_name": "Mage Tower",
  "attacker_level": 1,
  "defender_name": "Wyvern",
  "defender_level": 1,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [6.0, 0.0]
}
```
```json
{
  "title": "D16) AntiAir vs Dark Shaman (target mismatch sanity)",
  "encounter_type": "duel",
  "attacker_name": "AntiAir Tower",
  "attacker_level": 1,
  "defender_name": "Dark Shaman",
  "defender_level": 1,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [6.0, 0.0]
}
```
```json
{
  "title": "D17) Archer vs Wyvern (both target, far start)",
  "encounter_type": "duel",
  "attacker_name": "Archer Tower",
  "attacker_level": 1,
  "defender_name": "Wyvern",
  "defender_level": 1,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [8.0, 0.0]
}
```
```json
{
  "title": "D18) Archer(Lv3) vs Runner(Lv3)",
  "encounter_type": "duel",
  "attacker_name": "Archer Tower",
  "attacker_level": 3,
  "defender_name": "Runner",
  "defender_level": 3,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [6.0, 0.0]
}
```
```json
{
  "title": "D19) Archer(Lv6) vs Runner(Lv6)",
  "encounter_type": "duel",
  "attacker_name": "Archer Tower",
  "attacker_level": 6,
  "defender_name": "Runner",
  "defender_level": 6,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [6.0, 0.0]
}
```
```json
{
  "title": "D20) Tank(Lv10) vs Ogre Boss(Lv10)",
  "encounter_type": "duel",
  "attacker_name": "Tank Tower",
  "attacker_level": 10,
  "defender_name": "Ogre Boss",
  "defender_level": 10,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [4.0, 0.0]
}
```
```json
{
  "title": "D21) Mage(Lv10) vs Armored Orc(Lv10) (far start)",
  "encounter_type": "duel",
  "attacker_name": "Mage Tower",
  "attacker_level": 10,
  "defender_name": "Armored Orc",
  "defender_level": 10,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [8.0, 0.0]
}
```
```json
{
  "title": "D22) AntiAir(Lv6) vs Wyvern(Lv6) (very far start)",
  "encounter_type": "duel",
  "attacker_name": "AntiAir Tower",
  "attacker_level": 6,
  "defender_name": "Wyvern",
  "defender_level": 6,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [10.0, 0.0]
}
```
```json
{
  "title": "D23) Archer vs Ogre Boss (very far start)",
  "encounter_type": "duel",
  "attacker_name": "Archer Tower",
  "attacker_level": 1,
  "defender_name": "Ogre Boss",
  "defender_level": 1,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [10.0, 0.0]
}
```
```json
{
  "title": "D24) Mage vs Ogre Boss (far start)",
  "encounter_type": "duel",
  "attacker_name": "Mage Tower",
  "attacker_level": 1,
  "defender_name": "Ogre Boss",
  "defender_level": 1,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [8.0, 0.0]
}
```
```json
{
  "title": "D25) Tank vs Dark Shaman (ranged enemy check)",
  "encounter_type": "duel",
  "attacker_name": "Tank Tower",
  "attacker_level": 1,
  "defender_name": "Dark Shaman",
  "defender_level": 1,
  "trials": 300,
  "attacker_pos": [0.0, 0.0],
  "defender_pos": [7.0, 0.0]
}
```