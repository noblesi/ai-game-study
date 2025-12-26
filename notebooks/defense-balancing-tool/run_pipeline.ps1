param(
  [int]$Seeds = 10,           # 몇 번 반복할지(=실험 데이터 누적량)
  [int]$BaseSeed = 200,       # 시작 seed
  [int]$Trials = 80,          # 조합당 전투 횟수
  [int]$DuelPairs = 80,       # duel에서 생성할 pair 개수(유닛 수에 따라 자동으로 상한 적용됨)
  [int]$SwarmPairs = 160,     # swarm에서 생성할 pair 개수(유닛 수/defender-counts에 따라 상한 적용)
  [int]$LevelMin = 1,
  [int]$LevelMax = 10,
  [switch]$RandomPos = $true,
  [double]$PosRange = 8.0,
  [string]$DefenderCounts = "3,5,8",
  [string]$ExperimentsLog = "logs/experiments.jsonl",
  [string]$ScenariosLog = "logs/scenarios.jsonl"
)

$ErrorActionPreference = "Stop"

function Run($cmd) {
  Write-Host ">> $cmd"
  Invoke-Expression $cmd
}

Write-Host "[STEP 0] ensure dirs"
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
New-Item -ItemType Directory -Force -Path "datasets" | Out-Null
New-Item -ItemType Directory -Force -Path "reports" | Out-Null

Write-Host "[STEP 1] append experiments (duel + swarm)"
for ($i = 0; $i -lt $Seeds; $i++) {
  $seed = $BaseSeed + $i
  $perkSeed = 10000 + $seed

  $posFlags = ""
  if ($RandomPos) { $posFlags = "--random-pos --pos-range $PosRange" }

  # duel (2D)
  Run "python batch_experiments.py --encounter duel --mode 2 --pairs $DuelPairs --trials $Trials --seed $seed --out `"$ExperimentsLog`" $posFlags --auto-perks --perk-seed $perkSeed --perk-overwrite --level-min $LevelMin --level-max $LevelMax"

  # swarm (2D)
  Run "python batch_experiments.py --encounter swarm --mode 2 --pairs $SwarmPairs --trials $Trials --seed $seed --out `"$ExperimentsLog`" $posFlags --defender-counts `"$DefenderCounts`" --auto-perks --perk-seed $($perkSeed+1) --perk-overwrite --level-min $LevelMin --level-max $LevelMax"
}

Write-Host "[STEP 2] export train/test datasets"
Run "python export_dataset.py --input `"$ExperimentsLog`" --kinds auto_experiment --output datasets/train_experiments_v1.csv"
Run "python export_dataset.py --input `"$ScenariosLog`"   --kinds scenario_preset --output datasets/test_scenarios_v1.csv"

# (선택) 전체 합본 CSV도 갱신하고 싶으면 주석 해제
# Run "python export_dataset.py --input `"$ScenariosLog`" --input `"$ExperimentsLog`" --kinds scenario_preset,auto_experiment --output datasets/battle_dataset_v1.csv"

Write-Host "[STEP 3] baseline eval (group=pair_key_full + fixed test + RF grid)"
Run "python train_baseline.py --train datasets/train_experiments_v1.csv --test datasets/test_scenarios_v1.csv --k 10 --group --group-key pair_key_full --group-stratified --drop-overlap-groups --tune-threshold --rf-grid"

Write-Host "[OK] pipeline done."