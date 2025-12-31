from __future__ import annotations

import argparse
import re
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


DATE_RE = re.compile(r"portfolio_(\d{8})$")  # reports/portfolio_YYYYMMDD


def parse_date_from_folder(p: Path) -> str | None:
    m = DATE_RE.search(p.name)
    if not m:
        return None
    return m.group(1)  # YYYYMMDD


def load_one_day(portfolio_dir: Path) -> pd.DataFrame | None:
    date = parse_date_from_folder(portfolio_dir)
    if date is None:
        return None
    csv_path = portfolio_dir / "metrics_summary.csv"
    if not csv_path.exists():
        return None

    df = pd.read_csv(csv_path)
    # expected columns: name,label,thr,acc,bal_acc,f1_1,recall_1,prec_1,ap,roc_auc
    df.insert(0, "date", date)
    return df


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def plot_lines(df: pd.DataFrame, metric: str, out_png: Path, title: str):
    # df: date, label, metric
    df = df.sort_values("date")
    labels = df["label"].unique().tolist()

    plt.figure()
    for lab in labels:
        dfi = df[df["label"] == lab]
        x = [datetime.strptime(d, "%Y%m%d") for d in dfi["date"].tolist()]
        y = dfi[metric].to_numpy(dtype=float)
        plt.plot(x, y, marker="o", label=lab)

    plt.ylim(0.0, 1.05)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel(metric)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=160)
    plt.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reports-dir", default="reports", help="reports 폴더 경로")
    ap.add_argument("--days", type=int, default=7, help="최근 N일")
    ap.add_argument("--outdir", default="", help="출력 폴더(비우면 자동 생성)")
    args = ap.parse_args()

    reports_dir = Path(args.reports_dir)
    # portfolio_YYYYMMDD 폴더들 수집
    portfolios = []
    for p in reports_dir.iterdir():
        if p.is_dir() and DATE_RE.search(p.name):
            portfolios.append(p)

    # 날짜 내림차순 정렬 후 최근 N일
    portfolios = sorted(portfolios, key=lambda x: x.name, reverse=True)[: args.days]
    portfolios = sorted(portfolios, key=lambda x: x.name)  # 다시 오름차순

    rows = []
    for p in portfolios:
        df = load_one_day(p)
        if df is not None:
            rows.append(df)

    if not rows:
        raise SystemExit("유효한 portfolio_YYYYMMDD/metrics_summary.csv 를 찾지 못했습니다.")

    all_df = pd.concat(rows, ignore_index=True)

    # outdir 자동 생성
    if args.outdir.strip():
        outdir = Path(args.outdir)
    else:
        start = all_df["date"].min()
        end = all_df["date"].max()
        outdir = reports_dir / f"portfolio_week_{start}_{end}"
    ensure_dir(outdir)

    # 1) 원본 집계 저장
    all_df.to_csv(outdir / "weekly_metrics_long.csv", index=False, encoding="utf-8-sig")

    # 2) 날짜x실험 피벗(표 보기 좋게)
    pivot = all_df.pivot_table(index="date", columns="label", values=["recall_1", "prec_1", "f1_1", "bal_acc", "acc"])
    pivot.to_csv(outdir / "weekly_metrics_pivot.csv", encoding="utf-8-sig")

    # 3) 주간 요약(평균/표준편차)
    summary = all_df.groupby("label")[["recall_1", "prec_1", "f1_1", "bal_acc", "acc", "ap", "roc_auc", "thr"]].agg(["mean", "std"])
    summary.to_csv(outdir / "weekly_metrics_summary.csv", encoding="utf-8-sig")

    # 4) 라인차트 생성
    for metric in ["recall_1", "prec_1", "f1_1", "bal_acc"]:
        plot_lines(all_df, metric, outdir / f"trend_{metric}.png", f"Weekly Trend: {metric}")

    # 5) README.md (포트폴리오 붙이기용)
    start = all_df["date"].min()
    end = all_df["date"].max()
    readme = f"""# Weekly Portfolio Report ({start} ~ {end})

## What this shows
- Daily baseline snapshots aggregated into a weekly trend report
- Compare ablations across time: Full / No Perk / No Adv
- Focus on recall-tuned threshold setting

## Key Trend Plots
![](trend_recall_1.png)
![](trend_prec_1.png)
![](trend_f1_1.png)
![](trend_bal_acc.png)

## CSV Artifacts
- `weekly_metrics_long.csv` : raw concatenation (date, run, metrics)
- `weekly_metrics_pivot.csv`: pivot table (date x run)
- `weekly_metrics_summary.csv`: mean/std by run
"""
    (outdir / "README.md").write_text(readme, encoding="utf-8")

    print("[OK] weekly report saved to:", outdir)


if __name__ == "__main__":
    main()
