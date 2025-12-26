from __future__ import annotations

import argparse
import csv
import os
import random
from collections import defaultdict, Counter
from typing import Dict, List, Tuple


def _to_int01(v) -> int | None:
    if v is None:
        return None
    s = str(v).strip()
    if s == "":
        return None
    try:
        x = int(float(s))
        if x in (0, 1):
            return x
        return 1 if x > 0 else 0
    except Exception:
        return None


def _bin_idx(pos_rate: float, bins: int) -> int:
    if bins <= 1:
        return 0
    b = int(pos_rate * bins)
    if b >= bins:
        b = bins - 1
    if b < 0:
        b = 0
    return b


def read_csv(path: str) -> Tuple[List[str], List[Dict[str, str]]]:
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        rows = list(r)
        if not r.fieldnames:
            raise ValueError("CSV header not found.")
        return list(r.fieldnames), rows


def write_csv(path: str, fieldnames: List[str], rows: List[Dict[str, str]]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            # strict하게 쓰고 싶으면 그대로 row를 쓰면 되지만,
            # 여기선 안전하게 헤더 기준으로만 출력
            w.writerow({k: row.get(k, "") for k in fieldnames})


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="source CSV (e.g., datasets/train_experiments_v1.csv)")
    p.add_argument("--group-key", default="pair_key", help="group key column name")
    p.add_argument("--label-key", default="label_attacker_better", help="label column name (0/1)")
    p.add_argument("--test-ratio", type=float, default=0.2)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--bins", type=int, default=5, help="stratify bins by group pos-rate")
    p.add_argument("--out-train", required=True)
    p.add_argument("--out-test", required=True)
    args = p.parse_args()

    fieldnames, rows = read_csv(args.input)

    gkey = args.group_key
    lkey = args.label_key

    groups: Dict[str, List[int]] = defaultdict(list)
    labels: List[int] = []
    usable_idx: List[int] = []

    for i, row in enumerate(rows):
        g = (row.get(gkey) or "").strip()
        y = _to_int01(row.get(lkey))
        if not g or y is None:
            continue
        groups[g].append(i)
        labels.append(y)
        usable_idx.append(i)

    if not groups:
        raise ValueError(f"No usable groups found. Check group key column: {gkey}")

    # group-level pos rate
    group_pos_rate: Dict[str, float] = {}
    group_has_pos: Dict[str, bool] = {}
    group_has_neg: Dict[str, bool] = {}

    for g, idxs in groups.items():
        ys = [_to_int01(rows[i].get(lkey)) for i in idxs]
        ys = [y for y in ys if y is not None]
        if not ys:
            continue
        pr = sum(ys) / len(ys)
        group_pos_rate[g] = pr
        group_has_pos[g] = any(y == 1 for y in ys)
        group_has_neg[g] = any(y == 0 for y in ys)

    # stratified sampling by pos-rate bins
    bins = max(1, int(args.bins))
    bin_to_groups: Dict[int, List[str]] = defaultdict(list)
    for g, pr in group_pos_rate.items():
        bin_to_groups[_bin_idx(pr, bins)].append(g)

    rnd = random.Random(args.seed)
    test_groups = set()

    for b, glist in bin_to_groups.items():
        rnd.shuffle(glist)
        n = int(round(len(glist) * args.test_ratio))
        if n <= 0 and len(glist) > 0 and args.test_ratio > 0:
            n = 1
        test_groups.update(glist[:n])

    # ensure both classes exist in test (very important!)
    def build_rows_by_groups(gset: set[str]) -> List[Dict[str, str]]:
        out = []
        for g in gset:
            for i in groups[g]:
                out.append(rows[i])
        return out

    def label_dist(rs: List[Dict[str, str]]) -> Counter:
        c = Counter()
        for row in rs:
            y = _to_int01(row.get(lkey))
            if y is not None:
                c[y] += 1
        return c

    test_rows = build_rows_by_groups(test_groups)
    dist = label_dist(test_rows)

    if dist.get(1, 0) == 0:
        # bring one positive-containing group from train
        cand = [g for g in group_pos_rate.keys() if g not in test_groups and group_has_pos.get(g, False)]
        cand.sort(key=lambda g: group_pos_rate[g], reverse=True)
        if cand:
            test_groups.add(cand[0])

    test_rows = build_rows_by_groups(test_groups)
    dist = label_dist(test_rows)

    if dist.get(0, 0) == 0:
        # bring one negative-containing group from train
        cand = [g for g in group_pos_rate.keys() if g not in test_groups and group_has_neg.get(g, False)]
        cand.sort(key=lambda g: group_pos_rate[g])
        if cand:
            test_groups.add(cand[0])

    # finalize split
    test_rows = build_rows_by_groups(test_groups)
    train_groups = [g for g in group_pos_rate.keys() if g not in test_groups]
    train_rows = build_rows_by_groups(set(train_groups))

    # summary
    train_dist = label_dist(train_rows)
    test_dist = label_dist(test_rows)

    print(f"[INFO] input rows: {len(rows)}")
    print(f"[INFO] usable groups: {len(group_pos_rate)} (group_key={gkey})")
    print(f"[INFO] split groups: train={len(train_groups)} test={len(test_groups)} ratio≈{len(test_groups)/max(1,len(group_pos_rate)):.3f}")
    print(f"[INFO] TRAIN label dist: {dict(train_dist)}  pos_rate={(train_dist.get(1,0)/max(1,(train_dist.get(0,0)+train_dist.get(1,0)))):.4f}")
    print(f"[INFO] TEST  label dist: {dict(test_dist)}   pos_rate={(test_dist.get(1,0)/max(1,(test_dist.get(0,0)+test_dist.get(1,0)))):.4f}")

    write_csv(args.out_train, fieldnames, train_rows)
    write_csv(args.out_test, fieldnames, test_rows)
    print(f"[OK] wrote: {args.out_train}")
    print(f"[OK] wrote: {args.out_test}")


if __name__ == "__main__":
    main()
