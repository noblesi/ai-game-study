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
  [string]$ScenariosLog = "logs/scenarios.jsonl",
  [switch]$AppendExperiments = $false, # 기본은 재현성을 위해 experiments 로그를 매번 리셋

  # (포트폴리오) 모델 산출물 저장
  [switch]$SaveModel = $true,
  [string]$ModelPath = "models/baseline.joblib",
  [string]$ModelMeta = "models/meta.json"
)

$ErrorActionPreference = "Stop"

function Run($cmd) {
  Write-Host ">> $cmd"
  Invoke-Expression $cmd
  if ($LASTEXITCODE -ne 0){
    throw "Command failed (exit=$LASTEXITCODE): $cmd"
  }
}

function Ensure-V1($path){
  Write-Host "[CHECK] validate v1: $path"
  try {
    Run "python validate_logs.py --input `"$path`" --strict-v1"
  } catch {
    Write-Host "[WARN] strict v1 validation failed. Trying migrate -> revalidate: $path"
    Run "python migrate_logs.py --input `"$path`" --inplace"
    Run "python validate_logs.py --input `"$path`" --strict-v1"
  }
}

Write-Host "[STEP 0] ensure dirs"
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
New-Item -ItemType Directory -Force -Path "datasets" | Out-Null
New-Item -ItemType Directory -Force -Path "reports" | Out-Null
New-Item -ItemType Directory -Force -Path "models" | Out-Null

Write-Host "[STEP 1] generate scenario preset log (reset each run)"
Run "python batch_scenarios.py --out `"$ScenariosLog`" --reset"

Write-Host "[STEP 2] experiments log setup"
if (-not $AppendExperiments) {
  if (Test-Path $ExperimentsLog) {
    Write-Host ">> reset: $ExperimentsLog"
    Clear-Content $ExperimentsLog
  }
}

Write-Host "[DEBUG] Seeds=$Seeds BaseSeed=$BaseSeed Trials=$Trials DuelPairs=$DuelPairs SwarmPairs=$SwarmPairs AppendExperiments=$AppendExperiments"
if ($Seeds -le 0) { throw "[FATAL] Seeds must be >= 1 (current: $Seeds). STEP3 will be skipped." }

Write-Host "[STEP 3] append experiments (duel + swarm)"

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

$expLines = (Get-Content "logs/experiments.jsonl" -ErrorAction SilentlyContinue | Measure-Object -Line).Lines
if ($expLines -lt 1) {
    throw "[FATAL] experiments.jsonl is empty. STEP3 did not generate/append experiments."
}

Write-Host "[STEP 4] migrate/validate logs (strict v1)"
Ensure-V1 $ScenariosLog
Ensure-V1 $ExperimentsLog

Write-Host "[STEP 5] generate scenario report"
Run "python analyze_logs.py --input `"$ScenariosLog`" --output reports/scenario_report.md --recent 5 --top 5"

Write-Host "[STEP 6] export train/test datasets"
Run "python export_dataset.py --input `"$ExperimentsLog`" --kinds auto_experiment --output datasets/train_experiments_v1.csv"
Run "python export_dataset.py --input `"$ScenariosLog`"   --kinds scenario_preset --output datasets/test_scenarios_v1.csv"

# (선택) 전체 합본 CSV도 갱신하고 싶으면 주석 해제
# Run "python export_dataset.py --input `"$ScenariosLog`" --input `"$ExperimentsLog`" --kinds scenario_preset,auto_experiment --output datasets/battle_dataset_v1.csv"

Write-Host "[STEP 7] baseline eval (group=pair_key_full + fixed test + RF grid)"
$saveFlags = ""
if ($SaveModel) {
  $saveFlags = "--save-model `"$ModelPath`" --save-meta `"$ModelMeta`" --final-model BEST"
}

Run "python train_baseline.py --train datasets/train_experiments_v1.csv --test datasets/test_scenarios_v1.csv --k 10 --group --group-key pair_key_full --group-stratified --drop-overlap-groups --tune-threshold --rf-grid $saveFlags"

Write-Host "[OK] pipeline done."