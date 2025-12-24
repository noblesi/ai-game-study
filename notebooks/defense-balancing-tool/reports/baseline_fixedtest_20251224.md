# Fixed Test Evaluation Report

- generated_at: 2025-12-24T21:12:24
- train: datasets/experiments_v1.csv
- test: datasets/scenarios_v1.csv
- train_rows: 498 (usable=498)
- test_rows: 78 (usable=78)
- group_key: pair_key

## Best Model

- best: DT_balanced
- threshold: 0.50

## Metrics

- acc: 1.0000
- bal_acc: 1.0000
- f1_1: 1.0000
- recall_1: 1.0000
- precision_1: 1.0000
- cm: TN=42 FP=0 FN=0 TP=36

## Confusion Matrix

| | pred=0 | pred=1 |
|---|---:|---:|
| true=0 | 42 | 0 |
| true=1 | 0 | 36 |
