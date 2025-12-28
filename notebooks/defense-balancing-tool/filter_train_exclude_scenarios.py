import csv

test_path = "datasets/test_scenarios_v1.csv"
train_path = "datasets/train_experiments_v1.csv"
out_path = "datasets/train_experiments_no_scenario_pairs.csv"

# 1) 시나리오 pair_key 수집
scenario_keys = set()
with open(test_path, newline="", encoding="utf-8") as f:
    r = csv.DictReader(f)
    for row in r:
        k = (row.get("pair_key") or "").strip()
        if k:
            scenario_keys.add(k)

print(f"[INFO] scenario pair_keys: {len(scenario_keys)}")

# 2) train에서 해당 pair_key 제거
kept = dropped = 0
with open(train_path, newline="", encoding="utf-8") as f, open(out_path, "w", newline="", encoding="utf-8") as g:
    r = csv.DictReader(f)
    w = csv.DictWriter(g, fieldnames=r.fieldnames)
    w.writeheader()

    for row in r:
        k = (row.get("pair_key") or "").strip()
        if k in scenario_keys:
            dropped += 1
            continue
        w.writerow(row)
        kept += 1

print(f"[OK] wrote: {out_path} (kept={kept}, dropped={dropped})")
