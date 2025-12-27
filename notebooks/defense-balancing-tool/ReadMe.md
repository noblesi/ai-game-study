# Defense Balancing Tool (Python)

전투 시뮬레이션 로그(JSONL v1)를 기반으로 시나리오/실험을 자동 실행하고, 리포트 생성 및 베이스라인 모델로 결과를 검증하는 데이터 파이프라인 툴입니다.

- 목표: **재현 가능한 밸런싱 실험 파이프라인**(로그 → 검증 → 리포트 → 데이터셋 → 베이스라인 모델)
- 실행 환경: **Python 3.10+ 권장 (Windows / PowerShell)**

## Quickstart (Windows / PowerShell)

```powershell
cd notebooks/defense-balancing-tool
python -m pip install -r requirements.txt
.\run_pipeline.ps1
```

옵션 예시:

```powershell
# 실험 양 늘리기
.\run_pipeline.ps1 -Seeds 20 -Trials 120

# experiments 로그를 누적하고 싶을 때(기본은 재현성 위해 reset)
.\run_pipeline.ps1 -AppendExperiments
```

## Outputs (생성물)

- `logs/scenarios.jsonl` : 프리셋 시나리오 실행 로그 (kind=`scenario_preset`)
- `logs/experiments.jsonl` : 랜덤/자동 실험 로그 (kind=`auto_experiment`)
- `reports/scenario_report.md` : 시나리오별 요약 리포트(md)
- `datasets/train_experiments_v1.csv` : 학습용 CSV (experiments)
- `datasets/test_scenarios_v1.csv` : 고정 테스트 CSV (scenarios)
- `reports/baseline_eval_*.md` : baseline 학습/평가 리포트(md)

## Pipeline Overview

```mermaid
flowchart TD
  A[battle_scenarios_duel.md / swarm.md] --> B[batch_scenarios.py]
  B --> C[logs/scenarios.jsonl]

  D[batch_experiments.py] --> E[logs/experiments.jsonl]

  C --> F[validate_logs.py (strict v1)]
  E --> F
  F --> G[analyze_logs.py -> reports/scenario_report.md]
  C --> H[export_dataset.py -> datasets/test_scenarios_v1.csv]
  E --> I[export_dataset.py -> datasets/train_experiments_v1.csv]
  I --> J[train_baseline.py]
  H --> J
  J --> K[reports/baseline_eval_*.md]
```

## JSONL Log Schema (v1)

파이프라인은 기본적으로 `validate_logs.py --strict-v1`를 통과해야 진행됩니다.
만약 legacy 로그가 섞여 있다면, `migrate_logs.py --inplace`로 v1로 보정한 뒤 재검증합니다.

## What this demonstrates (Portfolio)

- 전투 밸런싱을 “재현 가능한 실험”으로 만들기: 시나리오 프리셋 + 자동 실험 로그 축적
- 로그 스키마(v1) 설계 + 검증/마이그레이션 도구로 데이터 품질 가드레일 구축
- 리포트 자동화: 시나리오별 승률/시간 등 요약을 md로 생성
- baseline ML: feature engineering(스탯/파생지표/퍼크 one-hot) + group split + 고정 테스트 평가
```