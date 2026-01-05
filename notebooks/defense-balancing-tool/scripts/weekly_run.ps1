param(
  # -------------------------
  # weekly_run 태그/학습 관련
  # -------------------------
  [string]$Tag = (Get-Date -Format "yyyyMMdd"),

  [string]$Train = "datasets\train_experiments_v1.csv",
  [string]$Test  = "datasets\test_scenarios_v1.csv",

  [int]$K = 30,
  [string]$GroupKey = "pair_key_full",
  [int]$Tries = 300,
  [int]$Repeats = 30,

  [string]$ThresholdMetric = "recall",

  # 승격 기준(Full 모델 기준)
  [double]$RecallDropTol = 0.01,   # current 대비 recall_1이 -0.01p 이내면 허용
  [double]$F1DropTol     = 0.02,   # current 대비 f1_1이 -0.02p 이내면 허용

  [switch]$ForcePromote,           # 조건 무시하고 무조건 승격
  [switch]$SkipPromote,            # 학습만 하고 승격은 안 함

  # 주간 총집합 옵션
  [string]$WeeklyReportsDir = "reports",
  [int]$WeeklyDays = 7,
  [string]$WeeklyOutdir = "",

  # -------------------------
  # run_pipeline 전달용(중요!)
  # -------------------------
  [int]$Seeds = 10,           # 몇 번 반복할지(=실험 데이터 누적량)
  [int]$BaseSeed = 200,       # 시작 seed
  [int]$Trials = 80,          # 조합당 전투 횟수
  [int]$DuelPairs = 80,       # duel에서 생성할 pair 개수
  [int]$SwarmPairs = 160,     # swarm에서 생성할 pair 개수
  [int]$LevelMin = 1,
  [int]$LevelMax = 10,
  [switch]$RandomPos = $true,
  [double]$PosRange = 8.0,
  [string]$DefenderCounts = "3,5,8",
  [string]$ExperimentsLog = "logs/experiments.jsonl",
  [string]$ScenariosLog = "logs/scenarios.jsonl",
  [switch]$AppendExperiments = $false,

  # (파이프라인) baseline 산출물 저장 옵션
  [switch]$PipelineSaveModel = $true,
  [string]$PipelineModelPath = "models/baseline.joblib",
  [string]$PipelineModelMeta = "models/meta.json"
)

# scripts 폴더에서 실행되더라도 프로젝트 루트로 고정
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$ErrorActionPreference = "Stop"

function New-Dir([string]$path) {
  New-Item -ItemType Directory -Force -Path $path | Out-Null
}

function Get-FinalMetricFromReport([string]$path, [string]$key) {
  if (-not (Test-Path $path)) { return $null }

  # "Final Model (fit on FULL train)" 아래의 "test metrics:" 섹션만 대상으로 잡기
  $raw = Get-Content $path -Raw

  $m = [regex]::Match($raw, "Final Model\s*\(fit on FULL train\)(.|\n)*?test metrics:\s*(.|\n)*?(?:\n\s*##|\z)")
  if (-not $m.Success) { return $null }

  $block = $m.Value

  $km = [regex]::Match($block, "\n\s*-\s*${key}:\s*([0-9]*\.?[0-9]+)")
  if ($km.Success) { return [double]$km.Groups[1].Value }

  return $null
}

function Invoke-TrainOne(
  [string]$name,
  [string]$reportName,
  [string]$saveModel,
  [string]$saveMeta,
  [switch]$DropPerk,
  [switch]$DropAdv
) {
  Write-Host "`n[TRAIN] $name -> $reportName"

  $pyArgs = @(
    "train_baseline.py",
    "--train", $Train,
    "--test",  $Test,
    "--k",     "$K",
    "--group", "--group-key", $GroupKey,
    "--group-stratified", "--tries", "$Tries",
    "--drop-overlap-groups",
    "--tune-threshold", "--threshold_metric", $ThresholdMetric,
    "--rf-grid",
    "--repeats", "$Repeats",
    "--save-model", $saveModel,
    "--save-meta",  $saveMeta,
    "--report_name", $reportName
  )

  if ($DropPerk) { $pyArgs += "--drop_perk_features" }
  if ($DropAdv)  { $pyArgs += "--drop_adv_features" }

  python @pyArgs
}

function Invoke-RunPipeline {
  Write-Host "`n[STEP] run_pipeline (Seeds=$Seeds, Trials=$Trials, DuelPairs=$DuelPairs, SwarmPairs=$SwarmPairs)"

  # run_pipeline 위치 결정: scripts 쪽을 우선(중복 파일 있으면 혼선 방지)
  $pipePath = $null
  if (Test-Path ".\scripts\run_pipeline.ps1") {
    $pipePath = ".\scripts\run_pipeline.ps1"
  } elseif (Test-Path ".\run_pipeline.ps1") {
    $pipePath = ".\run_pipeline.ps1"
  } else {
    throw "[weekly_run] run_pipeline.ps1 not found."
  }

  # ✅ 백틱으로 여러 줄 인자 나열하지 말고, splatting으로 안전하게 전달
  $pipeArgs = @{
    Seeds            = [int]$Seeds
    BaseSeed         = [int]$BaseSeed
    Trials           = [int]$Trials
    DuelPairs        = [int]$DuelPairs
    SwarmPairs       = [int]$SwarmPairs
    LevelMin         = [int]$LevelMin
    LevelMax         = [int]$LevelMax

    # switch는 bool로 넘겨도 PowerShell이 -Switch:$false 형태로 처리해줌
    RandomPos        = [bool]$RandomPos
    PosRange         = [double]$PosRange

    DefenderCounts   = $DefenderCounts
    ExperimentsLog   = $ExperimentsLog
    ScenariosLog     = $ScenariosLog
    AppendExperiments= [bool]$AppendExperiments

    SaveModel        = [bool]$PipelineSaveModel
    ModelPath        = $PipelineModelPath
    ModelMeta        = $PipelineModelMeta
  }

  Write-Host ("[WEEKLY DEBUG] calling {0} with Seeds={1}" -f $pipePath, $pipeArgs.Seeds)

  # call operator로 스크립트 실행 (dot-sourcing 금지)
  & $pipePath @pipeArgs
}


# -------------------------
# 0) 기본 폴더 준비
# -------------------------
New-Dir "scripts"
New-Dir "reports"
New-Dir "models"

$portfolioDir = "reports\portfolio_$Tag"
New-Dir $portfolioDir

# current config 없으면 생성(한 번만)
$currentCfg = "configs\portfolio_runs_current.json"
if (-not (Test-Path $currentCfg)) {
  New-Dir "configs"
  @'
[
  {"name":"full","label":"Full (60)","model":"models/rf_full_current.joblib","meta":"models/rf_full_current.json"},
  {"name":"no_perk","label":"No Perk (27)","model":"models/rf_no_perk_current.joblib","meta":"models/rf_no_perk_current.json"},
  {"name":"no_adv","label":"No Adv (42)","model":"models/rf_no_adv_current.joblib","meta":"models/rf_no_adv_current.json"}
]
'@ | Set-Content $currentCfg -Encoding UTF8
  Write-Host "[INFO] created: $currentCfg"
}

# -------------------------
# 1) 파이프라인(로그/데이터셋/기본 리포트) 실행  ✅(패치)
# -------------------------
Invoke-RunPipeline

# -------------------------
# 2) 모델 후보 3종 학습 (tag 고정 파일로 저장)
#    - 리포트명은 기존 규칙과 맞춤
# -------------------------
Invoke-TrainOne "FULL" `
  "baseline_eval_${Tag}_${ThresholdMetric}_k${K}.md" `
  "models\rf_full_${Tag}.joblib" `
  "models\rf_full_${Tag}.json"

Invoke-TrainOne "NO_PERK" `
  "baseline_eval_${Tag}_${ThresholdMetric}_k${K}_no_perk.md" `
  "models\rf_no_perk_${Tag}.joblib" `
  "models\rf_no_perk_${Tag}.json" `
  -DropPerk

Invoke-TrainOne "NO_ADV" `
  "baseline_eval_${Tag}_${ThresholdMetric}_k${K}_no_adv.md" `
  "models\rf_no_adv_${Tag}.joblib" `
  "models\rf_no_adv_${Tag}.json" `
  -DropAdv

# -------------------------
# 3) 승격 판단(Full 모델 기준) → promote_models.ps1 호출
# -------------------------
$doPromote = $false

if ($SkipPromote) {
  Write-Host "`n[STEP] SkipPromote enabled -> no promotion."
} elseif ($ForcePromote) {
  Write-Host "`n[STEP] ForcePromote enabled -> promote."
  $doPromote = $true
} else {
  $currentTagPath = "models\current_tag.txt"
  $currentTag = $null
  if (Test-Path $currentTagPath) {
    $currentTag = (Get-Content $currentTagPath -Raw).Trim()
  }

  $candReport = "reports\baseline_eval_${Tag}_${ThresholdMetric}_k${K}.md"

  if (-not $currentTag) {
    Write-Host "`n[STEP] no current_tag.txt -> first-time promote."
    $doPromote = $true
  } else {
    $currReport = "reports\baseline_eval_${currentTag}_${ThresholdMetric}_k${K}.md"

    $candRecall = Get-FinalMetricFromReport $candReport "recall_1"
    $candF1     = Get-FinalMetricFromReport $candReport "f1_1"

    $currRecall = Get-FinalMetricFromReport $currReport "recall_1"
    $currF1     = Get-FinalMetricFromReport $currReport "f1_1"

    if ($null -eq $candRecall -or $null -eq $candF1) {
      Write-Host "[WARN] cannot parse candidate metrics -> promote skipped (use -ForcePromote to override)."
    } elseif ($null -eq $currRecall -or $null -eq $currF1) {
      Write-Host "[WARN] cannot parse current metrics -> promote candidate."
      $doPromote = $true
    } else {
      $recOk = ($candRecall -ge ($currRecall - $RecallDropTol))
      $f1Ok  = ($candF1     -ge ($currF1     - $F1DropTol))

      Write-Host "`n[COMPARE] current(tag=$currentTag) vs candidate(tag=$Tag)"
      Write-Host (" - recall_1: {0} -> {1}" -f $currRecall, $candRecall)
      Write-Host (" - f1_1    : {0} -> {1}" -f $currF1, $candF1)

      if ($recOk -and $f1Ok) {
        Write-Host "[OK] candidate within tolerance -> promote."
        $doPromote = $true
      } else {
        Write-Host "[NO] candidate worse than tolerance -> keep current."
      }
    }
  }
}

if ($doPromote) {
  Write-Host "`n[STEP] promote models"
  if (Test-Path ".\scripts\promote_models.ps1") {
    .\scripts\promote_models.ps1 -Tag $Tag
  } else {
    throw "[weekly_run] scripts\promote_models.ps1 not found"
  }
}

# -------------------------
# 4) 오늘 포트폴리오팩 생성 (current config 사용)
# -------------------------
if (Test-Path ".\make_portfolio_pack.py") {
  Write-Host "`n[STEP] make_portfolio_pack -> $portfolioDir"
  python make_portfolio_pack.py `
    --config $currentCfg `
    --test $Test `
    --outdir $portfolioDir `
    --label-col label `
    --top-errors 15
} else {
  Write-Host "[WARN] make_portfolio_pack.py not found. skip."
}

# 실행 커맨드 기록(참고용)
@"
# run_pipeline (weekly_run에서 전달)
.\run_pipeline.ps1 -Seeds $Seeds -Trials $Trials -DuelPairs $DuelPairs -SwarmPairs $SwarmPairs -BaseSeed $BaseSeed -LevelMin $LevelMin -LevelMax $LevelMax -RandomPos:$RandomPos -PosRange $PosRange -DefenderCounts "$DefenderCounts" -AppendExperiments:$AppendExperiments

python train_baseline.py `
  --train $Train `
  --test  $Test `
  --k $K `
  --group --group-key $GroupKey --group-stratified --tries $Tries `
  --drop-overlap-groups `
  --tune-threshold --threshold_metric $ThresholdMetric `
  --rf-grid `
  --repeats $Repeats `
  --save-model models\rf_full_$Tag.joblib --save-meta models\rf_full_$Tag.json `
  --report_name baseline_eval_${Tag}_${ThresholdMetric}_k${K}.md

python make_portfolio_pack.py `
  --config $currentCfg `
  --test $Test `
  --outdir $portfolioDir `
  --label-col label `
  --top-errors 15
"@ | Set-Content (Join-Path $portfolioDir "run_commands.txt") -Encoding UTF8

# 현재 모델 태그도 같이 저장
if (Test-Path "models\current_tag.txt") {
  Copy-Item "models\current_tag.txt" (Join-Path $portfolioDir "current_tag.txt") -Force
}

# -------------------------
# 5) 주간 총집합 리포트 생성
#    - make_weekly_portfolio.py CLI에 맞춰 인자 전달
# -------------------------
if (Test-Path ".\make_weekly_portfolio.py") {
  Write-Host "`n[STEP] make_weekly_portfolio"

  # outdir 비우면 자동 생성이지만, 주간 폴더를 일정하게 남기고 싶으면 고정값 추천
  $weeklyOut = $WeeklyOutdir
  if ([string]::IsNullOrWhiteSpace($weeklyOut)) {
    $weeklyOut = "reports\portfolio_week_$Tag"
  }

  try {
    python make_weekly_portfolio.py `
      --reports-dir $WeeklyReportsDir `
      --days $WeeklyDays `
      --outdir $weeklyOut
    Write-Host "[OK] weekly portfolio -> $weeklyOut"
  } catch {
    Write-Host "[WARN] make_weekly_portfolio failed: $($_.Exception.Message)"
  }
} else {
  Write-Host "[WARN] make_weekly_portfolio.py not found. skip."
}
